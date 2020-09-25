Title: OpenWrt on Linksys WRT54GL
Date: 2020-09-25
Tags: openwrt, ddwrt, linksys, wrt54gl, router, networking

I recently wrote about a basic network setup than I tried to configure
using [dd-wrt][1] and [my struggles to have DHCP requests forwarded to
an external DHCP server][2]. I eventually found out that dd-wrt custom
service management binary `rc` overwrote `dhcp-fwd` configuration file
each time the service was (re)started.. Though I proposed a patch to
fix this specific issue, I wanted to have a look at alternative
software for my router.

I used to install [OpenWrt][4] on this router 10-15 years ago. But as
of September 2020, [the latest release of OpenWrt requires at the very
least 32 MB of RAM][3]. And 64 to 128 MB are recommended to avoid
"repeated crashes". I eventually read [OpenWrt's page dedicated to the
Linksys WRT54G line of routers][5], which contains a tremendous amount
of information. It mentions an OpenWrt "backfire" image (released in
2011) that is working on this hardware. So why not test it and see it
that can do the job ?

Latest stable binary for Linksys WRT54GL ([as documented][7]):

* URL: https://archive.openwrt.org/backfire/10.03.1/brcm-2.4/openwrt-wrt54g-squashfs.bin
* MD5sum: 1bd7980df25a27e1687ad2781a16bb73
* Size: 2372.0 KB
* Date: Wed Dec 21 03:34:20 2011

[libreCMC][6] looks an interesting alternative as well, but it seems
to support only Atheros based routers. My guess is that other
manufacturers (like Broadcom) are providing OpenWrt with some
(proprietary) binary blobs, which aren't included into libreCMC, which
focuses on providing full open source software.


# Flashing the router

The [OpenWrt WRT54G Install section][7] mentions several approaches to
flash the router:

* through the web UI,
* using commands on the CLI,
* using TFTP network protocol,
* via a JTAG cable

I have a preference for methods independent of the software deployed
on the router. So if I deploy a broken image, I am still able to flash
the router with another image. In that regard, the JTAG cable is the
best approach. However, this method requires a bit of hacking and
soldering, since there is no pluggable JTAG connector on these devices
(there are holes on the PCB that can be used for that purpose). See
[the hardware section][8] for details.

The TFTP approach is in my opinion a good compromise. It allows having
an image flashed by the bootloader, before the OS is actually started
(so we don't need to have a working OS). Also since everything is
happening through the network, there is no need to solder anything on
the PCB (not even opening the case).

## Enabling WRT54GL TFTP server

By default, the TFTP server isn't enabled; we need a shell on the
router to enable it. So we need to flash an initial image (OpenWrt or
dd-wrt) with another method (i.e through the Web UI of the factory
firmware), providing us with the shell access that we need.

Once having a shell, the following commands instruct WRT54GL
bootloader to wait 10 seconds for a TFTP connection during the boot
sequence ([source][7]):

    $ nvram set boot_wait=on
    $ nvram set wait_time=10
    $ nvram commit && reboot

Note that the following values were set before running the commands
mentioned above:

* `boot_wait` = `on`
* `wait_time` = `5`

5 seconds wait time was too low for my laptop network interface to
turn up on time to send the image during the router's boot
sequence. So 10 seconds is a value that works for me.

## Flashing the router using TFTP

After rebooting the router (by issuing a `reboot` command or
unplugging and replugging the cable), the power led blinks. The router
sets its factory IP address `192.168.1.1` reachable from any of the
lan ports. At that point (and roughly for the `wait_time` duration),
the router answers to ping with a `ttl=100`:

    $ ping 192.168.1.1
    64 bytes from 192.168.1.1 icmp_seq=1 ttl=100 time=3.85 ms
    64 bytes from 192.168.1.1 icmp_seq=2 ttl=100 time=1.74 ms
    64 bytes from 192.168.1.1 icmp_seq=3 ttl=100 time=2.11 ms
    64 bytes from 192.168.1.1 icmp_seq=4 ttl=100 time=1.40 ms
    64 bytes from 192.168.1.1 icmp_seq=5 ttl=100 time=1.70 ms

During that time frame, one can upload the image that is to be flashed
by the boot loader. The [Installing OpenWrt via TFTP][9] page
describes several options. My favorite one is using `atftp` which
allows initiating the file transfer with a single command (the other
tools require some sort of interaction).

Besides, the [Linksys official support documentation][10] provides us
with:

* the router’s default IP Address: *192.168.1.1*
* the default TFTP password: *admin*

Using that information, we are able to build our `atftp` command with
its arguments. We can run it during the appropriate boot sequence time
frame (as described above) from a computer connected to one of the
lan's router ports with an ethernet cable:

    $ atftp \
      --trace \
      --option "timeout 60" \
      --option "mode octet" \
      --password admin \
      --put --local-file /tmp/openwrt-wrt54g-squashfs.bin \
      192.168.1.1

    Trace mode on.
    Option timeout = 60
    Option mode = octet
    Option password = admin
    sent WRQ <file: /tmp/openwrt-wrt54g-squashfs.bin, mode: octet <timeout: 60, password: admin>>
    received ACK <block: 0>
    sent DATA <block: 1, size: 512>
    received ACK <block: 1>
    sent DATA <block: 2, size: 512>
    received ACK <block: 2>
    ...
    sent DATA <block: 4744, size: 512>
    received ACK <block: 4744>
    sent DATA <block: 4745, size: 32>
    received ACK <block: 4745>

Once `atftp` finishes uploading the firmware, the power led continues
to blink for a few seconds, then the DMZ led turns on. After a few
minutes, the DMZ led turns off and the power led stops blinking. The
router has been flashed successfully, and a ping to the router's ip
returns with a `ttl=64`. Once done, one can log on the UI at the
following URL: http://192.168.1.1

After a fresh OpenWrt firmware flash, any password works to log in the
UI. We are then led to set a new password.


# OpenWrt vs dd-wrt

I copied there the target network setup [I failed to put in place with
dd-wrt][2]:

                               +------+
                               | ISP  |
                               +---+--+
                                   |
                              +----+----+
    ---------------+----------+ WRT54GL +
    192.168.X.0/24 +          +----+----+
    (services)     |               |
          +--------+----+          | 192.168.Y.0/24
          | DHCP server |          | (users)
          | 192.168.X.2 |          |
          +-------------+

OpenWrt allowed me to deploy my target network setup (including DHCP
forwarding to an external DHCP server) in a couple of hours without
going into much troubles. It is more flexible than dd-wrt in that it
allows to setup several internal networks with customizable firewall
rules quite easily. Also it comes with `opkg`, a package manager that
allows installing a lot of additional software on the router,
including `dhcp-forwarder`. The configuration files live on the
router's persistent storage and can be updated without any issue.

On the other hand. OpenWrt is not maintained anymore (no more security
patches) for routers with less than 64 MB RAM..

[1]: https://dd-wrt.com/site/
[2]: http://www.florentflament.com/blog/broken-dhcp-forwarding-with-dd-wrt.html
[3]: https://openwrt.org/supported_devices/432_warning
[4]: https://openwrt.org
[5]: https://openwrt.org/toh/linksys/wrt54g
[6]: https://librecmc.org/
[7]: https://openwrt.org/toh/linksys/wrt54g#installing_openwrt
[8]: https://openwrt.org/toh/linksys/wrt54g#hardware
[9]: https://openwrt.org/docs/guide-user/installation/generic.flashing.tftp#linuxbsd
[10]: https://www.linksys.com/us/support-article?articleNum=137928
