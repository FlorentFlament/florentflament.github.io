Title: Broken DHCP forwarding with dd-wrt
Date: 2020-09-23
Updated: 2020-09-25
Tags: dd-wrt, linksys, wrt54gl, dhcp, dhcp-forwarding, networking

Lately, I've been playing with a (15 years old) [Linksys WRT54GL][4]
router (which still has decent hardware), running [dd-wrt][2] instead
of the factory firmware. dd-wrt is open source ([dd-wrt source
code][3]) and provides more features (like SSH access!) than Linksys'
factory software. Although, [dd-wrt documentation][5] is IMO a little
bit light. [OpenWrt][6] would have been an alternative if the latest
releases fitted into a 15 years old router (which is not the case).

In order to train my network skills (and also for fun), I wanted to
setup 2 internal networks, in addition to the link with my Internet
Access Provider, interconnected through the dd-wrt box. The 2 internal
networks would be as follows:

- A services network, running services like DHCP;
- A users network, where usual desktops and laptops would live.

The idea was to filter the access from the users network to my
internal services. So here's a diagram of the target setup:

                               +------+
                               | ISP  |
                               +---+--+
                                   |
                              +----+---+
    ---------------+----------+ dd-wrt +
    192.168.X.0/24 +          +----+---+
    (services)     |               |
          +--------+----+          | 192.168.Y.0/24
          | DHCP server |          | (users)
          | 192.168.X.2 |          |
          +-------------+

A nice feature of dd-wrt is the ability to setup a "DHCP Forwarder" on
the router, that would forward every DHCP request to an external DHCP
service. I like the idea of centralizing the DHCP configuration and
managing it with a configuration management software (like
ansible). Also it avoids running a DHCP service on the router, which
matters when it has 16MB of RAM.


# dd-wrt Setup

The dd-wrt version I am currently running is: "dd-wrt v3.0-r40559 mini
(08/06/19)". Yes it's more than 1 year old, but the code that I'm
interested in hasn't been updated for the last 20 months. But yes,
I'll update my firmware soon.

Here's dd-wrt setup performed through the web UI:

## Basic Setup

### WAN Setup

WAN Connection Type: Automatic Configuration - DHCP

### Network Setup

Router IP:

- Local IP Address: 192.168.Y.1
- Subnet Mask: 255.255.255.0

Network Address Server Settings (DHCP):

- DHCP Type: DHCP Forwarder
- DHCP Server: 192.168.X.2

## Switch Config

- vlan0: Ports 1, 2 assigned to bridge LAN
- vlan1: Ports W
- vlan2: Ports 3, 4
- Wireless: LAN

So the external DHCP server is plugged on `vlan2` (port 3 or 4), our
"services" network. And hosts relying on the DHCP service are living
on `vlan0` (port 1, 2) and the wireless lan, our "users" network, as
well as `vlan2`. What's being called "LAN" in the UI is actually the
`br0` bridge aggregating `vlan0` and the wireless lan `eth1`. A nice
drawing explain the [default WRT54GL interfaces setup][8].

## Networking

Network Configuration vlan2:

- Bridge Assignment: Unbridged
- IP Address: 192.168.X.1
- Subnet Mask: 255.255.255.0


# DHCP server with dnsmasq

I've setup a `dnsmasq` DHCP service on a machine (Raspberry Pi). The
nice thing about `dnsmasq` is that it provides DNS resolution for the
names advertised by the hosts during their DHCP negotiation. Here's
the bit of configuration that allows serving 2 distinct networks:

    # services network
    - dhcp-range=set:services,192.168.X.10,192.168.X.254
    - dhcp-option=tag:services,option:netmask,255.255.255.0
    - dhcp-option=tag:services,option:router,192.168.X.1

    # users network (via relay)
    - dhcp-range=set:users,192.168.Y.10,192.168.Y.254
    - dhcp-option=tag:users,option:netmask,255.255.255.0
    - dhcp-option=tag:users,option:router,192.168.Y.1

It all works, because `dnsmasq` knows which network the DHCP request
comes from depending on whether it comes from the relay or not. Then
we use tags to set dhcp options properly.


# The issue

Obviously, if that worked as expected that would be too easy. Hosts on
the same network than the DHCP server do obtain an IP address without
issue. However, hosts on the "users" network fail to obtain an IP
address.

A look a `dnsmasq` logs tells us that it receives "DHCP discover"
queries, and sends back "DHCP offer" responses. However, it keeps
receiving the same queries, as if the querying host never received the
DHCP offers.

    $ sudo journalctl -u dnsmasq -f | grep dnsmasq-dhcp
    Sep 23 18:16:25 dnspi dnsmasq-dhcp[24208]: DHCPDISCOVER(eth0) aa:bb:cc:dd:ee:ff
    Sep 23 18:16:25 dnspi dnsmasq-dhcp[24208]: DHCPOFFER(eth0) 192.168.Y.Z aa:bb:cc:dd:ee:ff
    Sep 23 18:16:25 dnspi dnsmasq-dhcp[24208]: DHCPDISCOVER(eth0) aa:bb:cc:dd:ee:ff
    Sep 23 18:16:25 dnspi dnsmasq-dhcp[24208]: DHCPOFFER(eth0) 192.168.Y.Z aa:bb:cc:dd:ee:ff
    Sep 23 18:16:25 dnspi dnsmasq-dhcp[24208]: DHCPDISCOVER(eth0) aa:bb:cc:dd:ee:ff
    Sep 23 18:16:25 dnspi dnsmasq-dhcp[24208]: DHCPOFFER(eth0) 192.168.Y.Z aa:bb:cc:dd:ee:ff
    Sep 23 18:16:29 dnspi dnsmasq-dhcp[24208]: DHCPDISCOVER(eth0) aa:bb:cc:dd:ee:ff
    Sep 23 18:16:29 dnspi dnsmasq-dhcp[24208]: DHCPOFFER(eth0) 192.168.Y.Z aa:bb:cc:dd:ee:ff
    Sep 23 18:16:37 dnspi dnsmasq-dhcp[24208]: DHCPDISCOVER(eth0) aa:bb:cc:dd:ee:ff
    Sep 23 18:16:37 dnspi dnsmasq-dhcp[24208]: DHCPOFFER(eth0) 192.168.Y.Z aa:bb:cc:dd:ee:ff
    ...

On the side of the host asking for an IP address using DHCP, `tcpdump`
reveals us that the host is sending DHCP requests, but doesn't receive
any answer:

    $ sudo tcpdump -n -s 1500 '(port 67 or port 68)'
    18:24:07.561023 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    18:24:08.803149 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    18:24:11.533673 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    18:24:16.112067 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    18:24:24.438831 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    18:24:33.279271 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    18:24:41.868362 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    18:24:50.329420 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    18:24:59.224705 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    18:25:07.708588 IP 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from aa:bb:cc:dd:ee:ff, length 300
    ...

This means that somewhere between the host and the DHCP server,
something (i.e dd-wrt router) isn't forwarding the DHCP offers as it
should:

    +-------------+  Request  +--------+  Request  +------+
    |             |-----<-----|        |-----<-----|      |
    | DHCP Server |           | dd-wrt |           | host |
    |             |----->-----|        |           |      |
    +-------------+  Offer    +--------+           +------+


# dd-wrt's dhcpfwd service

Now let's have a look at what happens on the dd-wrt box. The dd-wrt
setup described above starts a `dhcpfwd` service that is supposed to
forward DHCP requests from the hosts living in the "users" network to
the DHCP server at `192.168.X.2` (i.e on the "services" network), and
provide the replies back to the requesting hosts.

    # ps | grep dhcpfwd
     4973 root       696 S    dhcpfwd -c /tmp/dhcp-fwd/dhcp-fwd.conf
 
 Here's the `dhcpfwd` configuration file that has been generated by
 dd-wrt:
     
    # cat /tmp/dhcp-fwd/dhcp-fwd.conf
    user		root
    group		root
    chroot		/var/run/dhcp-fwd
    logfile		/tmp/dhcp-fwd.log
    loglevel	1
    pidfile		/var/run/dhcp-fwd.pid
    ulimit core	0
    ulimit stack	64K
    ulimit data	32K
    ulimit rss	200K
    ulimit nproc	0
    ulimit nofile	0
    ulimit as	0
    if	br0	true	false	true
    if	vlan1	false	true	true
    name	br0	ws-c
    server	ip	192.168.X.2

The [dhcp-fwd manpage][7] tells us that the 2 `if` lines respectively
configure on which interface `dhcp-fwd` expects to receive DHCP
requests and on the other side, DHCP replies (or offers).

    # if ifname has_clients has_servers allow_bcast
    if   br0    true        false       true
    if   vlan1  false       true        true

Now if you recall how we configured our dd-wrt switch:

- `br0` (`vlan0` and `eth1`) is the interface connected to our "users"
  network
- `vlan1` is connected to our ISP
- `vlan2` is connected our "services" network

This means that `dhcp-fwd` expects to receive DHCP request from our
"users" network (`br0`), and DHCP replies from our ISP (`vlan1`). This
is not what we want, since our DHCP server is plugged on our
"services" network (`vlan2`).

So we can update the `/tmp/dhcp-fwd/dhcp-fwd.conf` file by replacing
`vlan1` with `vlan2`, and run:

    $ stopservice dhcpfwd
    $ dhcpfwd -c /tmp/dhcp-fwd/dhcp-fwd.conf -n
    
The `-n` option prevents `dhcp-fwd` from forking the process in the
background. It works! `dhcp-fwd` forwards the request forth then back
as it is expected to do. We found how to fix our issue!

Wait wait, if we restart the process with `startservice dhcpfwd` or
`restart dhcpfwd` (or even reboot the router), then the configuration
file gets overwritten with the previous values. And `dhcp-fwd` doesn't
listen for DHCP replies on from the "services" network (i.e the
`vlan2` interface). And so far I couldn't find any decent solution to
update `dhcp-fwd` configuration file across reboots without patching
dd-wrt codebase.


## The Code (and the fix)

Here's the [code that starts dhcpfwd][1]

It actually (re)generates `dhcp-fwd` configuration file whenever the
service is (re)started. The `wan_proto` variable is tested against
several possible values: `pppoe`, `3g`, `pptp`, ... but in the end, in
the most basic scenario where the router is connected to an Internet
Service Provider, who provides us with connectivity through DHCP or a
given fixed IP, `dhcp-fwd` will be setup to only accept DHCP replies
from the WAN interface `wan_ifname`.

See:

    } else if (strcmp(wan_proto, "dhcp") == 0 || strcmp(wan_proto, "static") == 0 || strcmp(wan_proto, "dhcp_auth") == 0) {
            fprintf(fp, "if %s      false   true    true\n", wan_ifname);
    }
    ...
    else {
            fprintf(fp, "if %s      false   true    true\n", wan_ifname);
    }

A reasonable fix would be to introduce an additional nvram variable,
let's say `dhcpfwd_ifname`, that one could set to explicitly specify
the interface on which `dhcp-fwd` should expect DHCP replies:

    char* dhcpfwd_ifname = nvram_safe_get("dhcpfwd_ifname");
    ...
    if (dhcpfwd_ifname != "") {
        fprintf(fp, "if %s      false   true    true\n", dhcpfwd_ifname);
    }
    ...
    
Setting the `dhcpfwd_ifname` to `vlan2` would then have the
`start_dhcpfwd` code generate the *good* `dhcp-fwd` configuration file
for this use case. So next step would probably be to propose that
change to dd-wrt maintainers and see what happens..

# Update of 25-09-2020

I created a [ticket][10] on the project's tracker, and the maintainer
*brainslayer* already [implemented the fix][9] in dd-wrt's
codebase. Thanks!

[1]: https://svn.dd-wrt.com/browser/src/router/services/services/dhcpforward.c#L38
[2]: https://dd-wrt.com/site/
[3]: https://svn.dd-wrt.com/browser
[4]: https://en.wikipedia.org/wiki/Linksys_WRT54G_series#WRT54GL
[5]: https://forum.dd-wrt.com/wiki/index.php/Main_Page
[6]: https://openwrt.org/
[7]: https://www.mankier.com/1/dhcp-fwd
[8]: https://openwrt.org/toh/linksys/wrt54g#internal_architecture_-_wrt54g_v4_wrt54gs_v3
[9]: https://svn.dd-wrt.com/changeset/44468
[10]: https://svn.dd-wrt.com/ticket/7241
