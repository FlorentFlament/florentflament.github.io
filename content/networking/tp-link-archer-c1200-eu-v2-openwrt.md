Title: OpenWrt and tp-link Archer C1200 EU v2
Date: 2020-09-28
Tags: networking, tp-link, archer c1200, openwrt, firmware

Subtitled "How to brick a tp-link Archer C1200 EU v2"

As I figured out that my good old [Linksys WRT54GL][17] was a bit old
and couldn't even run the latest and greatest OpenWrt firmware, I
decided to buy a new (faster) router [supported by OpenWrt][1]. So I
went to my local retailer (Darty) and (what a luck) found a *tp-link
Archer C5 AC1200 v2* for 40 bucks ! Though once at home, I noticed
that it was actually a *tp-link Archer C1200 v2* .. The 4 character
'C5 A' were actually missing ! Nonetheless, I decided to try and see
how far I could go with the installation of an alternative firmware.

A first glance at [OpenWrt supported devices][1] let us understand
that the *tp-link Archer C1200* is not officially supported by
OpenWrt.. But sometimes perseverance pays off !


# Resources

Some interesting forum threads:

* [Build for TP-Link Archer C1200-AC1200][2]
* [Unable to install at TP-LINK Archer C1200 v2][3]

Hardware information:

* [TP-Link Archer C1200 2 OpenWrt page][4] (early draft)
* [TP-LINK Archer C1200 v2.x on Wireless CAT][5]

What tp-link provides:

* [official firmware updates][9]
* [GPL code used in the router][10]

## Hardware

A quick look inside the router's case let us see the following chips:

* Broadcom BCM43217TKMLG
* Broadcom BCM53125SKMMLG
* At least one additional chip is hidden in a metal case with a
  radiator fixed over it

This is consistent with the [data available on Wireless CAT][5]:

* Broadcom BCM47189: CPU + Wifi 802.11 an+ac
* Broadcom BCM43217: Wifi 802.11 bgn
* Broadcom BCM53125: Switch 1G

According to Wireless CAT, as well as OpenWrt pages, this is (almost?)
the same hardware as the *tp-link Archer C1200 v1*, as well as the
*Tenda AC9*. See:

* [TP-LINK Archer C1200 v1.x on Wireless CAT][6]
* [Tenda AC9 on Wireless CAT][7]
* [Techdata: Tenda AC9 OpenWrt page][8]


# Serial port connection

When opening the Archer C1200 case, [we can see 4 holes][11]. These are
connected to (one of) the SoC UART (i.e serial port), and can be used
to get a console on the device from a computer, through a USB to TTL
adapter (for a few dollars on ebay). There's an OpenWrt page on [how
to use the serial console][12].

Here's what signals the holes correspond to:

      o   o   o   o
    3.3V GND  RX  TX  router signals
    3.3V GND  TX  RX  PC signals

And a command to open a console on the Archer C1200 from a Linux
terminal (once the PC has been connected to the router's serial port):

    $ minicom -D /dev/ttyUSB0 -b 115200


## Factory firmware boot log

Here's a dump of the factory firmware boot log, copied from the
console opened on the router:

    Decompressing...done


    CFE version 9.10.178.50 (r635252) based on BBP 1.0.37 for BCM947XX (32bit,SP,)
    Build Date: Thu Sep  8 14:49:19 CST 2016 (seal@seal-pc)
    Copyright (C) 2000-2008 Broadcom Corporation.

    Init Arena
    Init Devs.
    Boot partition size = 262144(0x40000)
    DDR Clock: 533 MHz
    Info: DDR frequency set from clkfreq=900,*533*
    No GPIO defined for BBSI interface
    No BBSI device
    bcm_robo_enable_switch: EEE is disabled
    et0: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    CPU type 0x0: 900MHz
    Tot mem: 131072 KBytes

    CFE mem:    0x00F00000 - 0x02FB912C (34312492)
    Data:       0x00F6B754 - 0x00F70C04 (21680)
    BSS:        0x00F70C10 - 0x00FB712C (288028)
    Heap:       0x00FB712C - 0x02FB712C (33554432)
    Stack:      0x02FB712C - 0x02FB912C (8192)
    Text:       0x00F00000 - 0x00F5F4F4 (390388)

    Device eth0:  hwaddr AA-BB-CC-DD-EE-00, ipaddr 192.168.0.1, mask 255.255.255.0
            gateway not set, nameserver not set
    Reading Partition Table from NVRAM ... OK
    Parsing Partition Table ... OK
    factory boot check integer ok.
    factory boot load fs fs boot len 262144 to addr 0x3f00000.
    Decompressing...done


    CFE version 9.10.178.50 (r635252) based on BBP 1.0.37 for BCM947XX (32bit,SP,)
    Build Date: Thu Sep  8 14:48:53 CST 2016 (seal@seal-pc)
    Copyright (C) 2000-2008 Broadcom Corporation.

    Init Arena
    Init Devs.
    Boot partition size = 262144(0x40000)
    DDR Clock: 533 MHz
    Info: DDR frequency set from clkfreq=900,*533*
    No GPIO defined for BBSI interface
    No BBSI device
    bcm_robo_enable_switch: EEE is disabled
    et0: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    CPU type 0x0: 900MHz
    Tot mem: 131072 KBytes

    CFE mem:    0x00F00000 - 0x02FB1ACC (34282188)
    Data:       0x00F6933C - 0x00F69AD8 (1948)
    BSS:        0x00F69AE8 - 0x00FAFACC (286692)
    Heap:       0x00FAFACC - 0x02FAFACC (33554432)
    Stack:      0x02FAFACC - 0x02FB1ACC (8192)
    Text:       0x00F00000 - 0x00F5D4EC (382188)

    Device eth0:  hwaddr AA-BB-CC-DD-EE-00, ipaddr 192.168.0.1, mask 255.255.255.0
            gateway not set, nameserver not set
    Loader:raw Filesys:raw Dev:flash0.os File: Options:(null)
    Loading: .... 4674528 bytes read
    Entry at 0x00008000
    Closing network.
    Starting program at 0x00008000
    console [ttyS0] enabled, bootconsole disabled
    brd: module loaded
    loop: module loaded
    pflash: found no supported devices
    bcmsflash: squash filesystem found at block 40
    Creating 6 MTD partitions on "bcmsflash":
    0x000000000000-0x000000080000 : "boot"
    0x000000080000-0x000000ff0000 : "linux"
    0x000000280000-0x000000ff0000 : "rootfs"
    0x000000fb0000-0x000000fc0000 : "usb-config"
    0x000000fc0000-0x000000fe0000 : "log"
    0x000000ff0000-0x000001000000 : "nvram"
    flash_chrdev :  flash_chrdev_init
    nflash: found no supported devices
    PPP generic driver version 2.4.2
    usbmon: debugfs is not available
    Initializing USB Mass Storage driver...
    usbcore: registered new interface driver usb-storage
    USB Mass Storage support registered.
    Registered led device: blue:lan1
    Registered led device: blue:lan2
    Registered led device: blue:lan3
    Registered led device: blue:lan4
    Registered led device: blue:usb_1
    Registered led device: blue:wps
    Registered led device: blue:wan
    Registered led device: orange:wan
    Registered led device: blue:status
    Registered led device: blue:wlan_2g
    Registered led device: blue:wlan_5g
    u32 classifier
        Actions configured
    Netfilter messages via NETLINK v0.30.
    nf_conntrack version 0.5.0 (1954 buckets, 7816 max)
    ctnetlink v0.93: registering with nfnetlink.
    xt_time: kernel timezone is -0000
    ip_tables: (C) 2000-2006 Netfilter Core Team
    TCP cubic registered
    NET: Registered protocol family 10
    lo: Disabled Privacy Extensions
    ip6_tables: (C) 2000-2006 Netfilter Core Team
    IPv6 over IPv4 tunneling driver
    sit0: Disabled Privacy Extensions
    NET: Registered protocol family 17
    Bridge firewalling registered
    802.1Q VLAN Support v1.8 Ben Greear <greearb@candelatech.com>
    All bugs added by David S. Miller <davem@redhat.com>
    Northstar brcmnand NAND Flash Controller driver, Version 0.1 (c) Broadcom Inc. 2012
    brcmnand: found no supported devices
    VFS: Mounted root (squashfs filesystem) readonly on device 31:2.
    devtmpfs: mounted
    Freeing init memory: 208K
    ctf: module license 'Proprietary' taints kernel.
    Disabling lock debugging due to kernel taint
    ctf 22127 0 - Live 0x7f000000 (P)
    et_module_init: passivemode set to 0x0
    et_module_init: txworkq set to 0x0
    et_module_init: et_txq_thresh set to 0x400
    et_module_init: et_rxlazy_timeout set to 0x3e8
    et_module_init: et_rxlazy_framecnt set to 0x20
    bcm_robo_enable_switch: EEE is disabled
    eth0: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    eth1: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    et 71774 0 - Live 0x7f00e000 (P)
    et 71774 0 - Live 0x7f00e000 (P)
    emf 17251 0 - Live 0x7f02a000 (P)
    igs 13399 0 - Live 0x7f037000 (P)
    dpsta 4559 0 - Live 0x7f043000 (P)
    ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
    ehci_hcd 0000:00:04.1: EHCI Host Controller
    ehci_hcd 0000:00:04.1: new USB bus registered, assigned bus number 1
    ehci_hcd 0000:00:04.1: irq 36, io mem 0x18004000
    ehci_hcd 0000:00:04.1: USB 0.0 started, EHCI 1.00
    hub 1-0:1.0: USB hub found
    hub 1-0:1.0: 2 ports detected
    hotplug detected product:  1d6b/2/206
    hotplug detected product:  1d6b/2/206
    ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
    ohci_hcd 0000:00:04.0: OHCI Host Controller
    ohci_hcd 0000:00:04.0: new USB bus registered, assigned bus number 2
    ohci_hcd 0000:00:04.0: irq 36, io mem 0x1800d000
    hub 2-0:1.0: USB hub found
    hub 2-0:1.0: 2 ports detected
    hotplug detected product:  1d6b/1/206
    hotplug detected product:  1d6b/1/206
    NTFS driver 2.1.29 [Flags: R/O MODULE].
    fuse init (API version 7.15)
    jffs2 not ready yet; using ramdisk

    Please press Enter to activate this console. button cycle succeed
    tun: Universal TUN/TAP device driver, 1.6
    tun: (C) 1999-2004 Max Krasnyansky <maxk@qualcomm.com>
    PPP MPPE Compression module registered
    ip6tnl0: Disabled Privacy Extensions
    L2TP core driver, V2.0
    L2TP netlink interface
    gre: GRE over IPv4 demultiplexor driver
    GRE over IPv4 tunneling driver
    bonding: Ethernet Channel Bonding Driver: v3.7.0 (June 2, 2010)
    bonding: Warning: either miimon or arp_interval and arp_ip_target module parameters must be specified, otherwise bonding will not detect link.
    NET: Registered protocol family 24
    PPPoL2TP kernel driver, V2.0
    PPTP driver version 0.8.3
    nf_conntrack_rtsp v0.7 loading
    nf_nat_rtsp v0.7 loading
    reloadconfig() begin:
    reloadconfig() end:
    reload_profile() begin:
    reload_profile() end:
    GMT-01:00
    device eth0.1 entered promiscuous mode
    device eth0 entered promiscuous mode
    br-lan: port 1(eth0.1) entering learning state
    br-lan: port 1(eth0.1) entering learning state
    ADDRCONF(NETDEV_CHANGE): eth0.1: link becomes ready
    br-lan: port 1(eth0.1) entering forwarding state
    Lan Domain: tplinklogin.net
    Lan Domain: www.tplinklogin.net
    br-lan: no IPv6 routers present
    eth0: no IPv6 routers present
    eth1: no IPv6 routers present
    eth1.4094: no IPv6 routers present
    wl_module_init: passivemode set to 0x0
    wl_module_init: txworkq set to 0x0
    eth2: Broadcom BCM43c8 802.11 Wireless Controller 9.10.178.50 (r635252 WLTEST)
    PCI: Enabling device 0001:01:00.0 (0140 -> 0142)
    eth3: Broadcom BCM43227 802.11 Wireless Controller 9.10.178.50 (r635252 WLTEST)
    device eth3 entered promiscuous mode
    br-lan: port 2(eth3) entering learning state
    br-lan: port 2(eth3) entering learning state
    br-lan: port 2(eth3) entering forwarding state
    usbshare boot start
    usbshare boot end
    device eth0 left promiscuous mode
    br-lan: port 1(eth0.1) entering forwarding state
    device eth0.1 left promiscuous mode
    br-lan: port 1(eth0.1) entering disabled state
    device eth0.1 entered promiscuous mode
    device eth0 entered promiscuous mode
    br-lan: port 1(eth0.1) entering learning state
    br-lan: port 1(eth0.1) entering learning state
    device eth0.2 entered promiscuous mode
    br-lan: port 3(eth0.2) entering learning state
    br-lan: port 3(eth0.2) entering learning state
    [smartip_read_cfg 69] lan_mask is 255.255.255.0

    [smartip_read_cfg 79] lan_type is 1

    [smartip_read_cfg 64] lan_ip is 192.168.0.254

    =====>>>>> wireless setting is finished
    br-lan: port 1(eth0.1) entering forwarding state
    br-lan: port 3(eth0.2) entering forwarding state
    [smartip_create_ibus_thread 41] create ibus thread successfully

    [smartip_start_process 504] smartipd start udhcpc..........

    [smartip_ibus_handle_dhcp_event 1634] smartip: udhcpc detect no dhcp server

## Getting a shell

The serial console provides a root shell by pressing Enter:

    BusyBox v1.19.4 (2018-01-18 10:20:44 CST) built-in shell (ash)
    Enter 'help' for a list of built-in commands.

         MM           NM                    MMMMMMM          M       M
       $MMMMM        MMMMM                MMMMMMMMMMM      MMM     MMM
      MMMMMMMM     MM MMMMM.              MMMMM:MMMMMM:   MMMM   MMMMM
    MMMM= MMMMMM  MMM   MMMM       MMMMM   MMMM  MMMMMM   MMMM  MMMMM'
    MMMM=  MMMMM MMMM    MM       MMMMM    MMMM    MMMM   MMMMNMMMMM
    MMMM=   MMMM  MMMMM          MMMMM     MMMM    MMMM   MMMMMMMM
    MMMM=   MMMM   MMMMMM       MMMMM      MMMM    MMMM   MMMMMMMMM
    MMMM=   MMMM     MMMMM,    NMMMMMMMM   MMMM    MMMM   MMMMMMMMMMM
    MMMM=   MMMM      MMMMMM   MMMMMMMM    MMMM    MMMM   MMMM  MMMMMM
    MMMM=   MMMM   MM    MMMM    MMMM      MMMM    MMMM   MMMM    MMMM
    MMMM$ ,MMMMM  MMMMM  MMMM    MMM       MMMM   MMMMM   MMMM    MMMM
      MMMMMMM:      MMMMMMM     M         MMMMMMMMMMMM  MMMMMMM MMMMMMM
        MMMMMM       MMMMN     M           MMMMMMMMM      MMMM    MMMM
         MMMM          M                    MMMMMMM        M       M
           M
     ---------------------------------------------------------------
       For those about to rock... (Attitude Adjustment, r12067)
     ---------------------------------------------------------------
    root@Akronite:/#


# Bootloader CLI

We can obtain a CLI on the CFE bootloader by repeatedly typing Ctrl-C
during the boot sequence ([source][13]):

    Decompressing...done


    CFE version 9.10.178.50 (r635252) based on BBP 1.0.37 for BCM947XX (32bit,SP,)
    Build Date: Thu Sep  8 14:49:19 CST 2016 (seal@seal-pc)
    Copyright (C) 2000-2008 Broadcom Corporation.

    Init Arena
    Init Devs.
    Boot partition size = 262144(0x40000)
    DDR Clock: 533 MHz
    Info: DDR frequency set from clkfreq=900,*533*
    No GPIO defined for BBSI interface
    No BBSI device
    bcm_robo_enable_switch: EEE is disabled
    et0: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    CPU type 0x0: 900MHz
    Tot mem: 131072 KBytes

    CFE mem:    0x00F00000 - 0x02FB912C (34312492)
    Data:       0x00F6B754 - 0x00F70C04 (21680)
    BSS:        0x00F70C10 - 0x00FB712C (288028)
    Heap:       0x00FB712C - 0x02FB712C (33554432)
    Stack:      0x02FB712C - 0x02FB912C (8192)
    Text:       0x00F00000 - 0x00F5F4F4 (390388)

    Device eth0:  hwaddr AA-BB-CC-DD-EE-00, ipaddr 192.168.0.1, mask 255.255.255.0
            gateway not set, nameserver not set
    Startup canceled
    CFE> ^C
    CFE> ^C
    CFE> ^C
    CFE> help
    Available commands:

    bbsi                Broadcom BBSI interface utility.
    nvram               NVRAM utility.
    reboot              Reboot.
    md                  Dump content on memory in hex format.
    fdump               Dump content on flash device in hex format.
    flash               Update a flash memory device
    batch               Load a batch file into memory and execute it
    go                  Start a previously loaded program.
    boot                Load an executable file into memory and execute it
    load                Load an executable file into memory without executing it
    save                Save a region of memory to a remote file via TFTP
    ping                Ping a remote IP host.
    arp                 Display or modify the ARP Table
    ifconfig            Configure the Ethernet interface
    show clocks         Show current values of the clocks.
    show devices        Display information about the installed devices.
    unsetenv            Delete an environment variable.
    printenv            Display the environment variables
    setenv              Set an environment variable.
    help                Obtain help for CFE commands

    For more information about a command, enter 'help command-name'
    *** command status = 0
    CFE>

Many commands are available on the CFE CLI. Some of them (flash, boot,
load, save) can connect to a TFTP server to get or put some data.


# Flashing the firmware

## Setting up a TFTP server

In order to exchange files with the router (for instance to flash a
firmware), I had to setup a TFTP service on my laptop and connect it
to one of the Archer router's (yellow) LAN ports with an ethernet
cable.

Here's how to install such a TFTP service (on Ubuntu 20.04):

    $ sudo apt install tftpd
    $ cat >/etc/xinetd.d/tftp <<EOF
    > {
    >         disable                 = no
    >         socket_type             = dgram
    >         protocol                = udp
    >         wait                    = yes
    >         flags                   = IPv4
    >         port                    = 69
    >         user                    = root
    >         server                  = /usr/sbin/in.tftpd
    >         server_args             = -s /tftpboot
    > }
    > EOF
    $ sudo mkdir /tftpboot
    $ sudo systemctl restart xinetd

Then I put some firmware files to be used (downloaded) by the router
in the `/tftpboot` directory. I also created some empty files with
write access to everybody (`chmod a+x`) in that directory, for the
router's TFTP client to be able to upload files. I mostly copied the
xinetd tftp config from [this article][14].

## Backing up the factory firmware

In order to be able to restore the factory firmware, one should
*always* start with a backup of their device's firmware! This is where
I failed.. Here's what the `help` command says about the CFE `save`
command:

    CFE> help
    ...
    save                Save a region of memory to a remote file via TFTP
    ...

I mistakenly believed that I could use the `save` command to backup
the firmware to my pc through TFTP. This command actually saves a
*region of memory*, not to be mistaken for a *region of the flash
device* ! So I basically backed up garbage instead of the router's
factory firmware, and I subsequently bricked the router when I tried
to restore its factory firmware (as we will see later).

## Flashing OpenWrt Tenda AC9 firmware

As we have seen before, both *tp-link Archer C1200 v1* and *Tenda AC9*
seem to have the same hardware than the *tp-link Archer C1200 v2*. And
the *Tenda AC9* is marked as supported in the [OpenWrt supported
devices][7] page. So I decided to give it a try, as I thought I would
be able to flash the factory firmware back to the Archer C1200.

    CFE> show devices
    Device Name          Description
    -------------------  ---------------------------------------------------------
    uart0                NS16550 UART at 0x18000300
    flash0               ST Compatible Serial flash size 16384KB
    flash0.boot          ST Compatible Serial flash offset 00000000 size 256KB
    flash0.boot2         ST Compatible Serial flash offset 00040000 size 256KB
    flash0.trx           ST Compatible Serial flash offset 00080000 size 1KB
    flash0.os            ST Compatible Serial flash offset 0008001C size 15808KB
    flash0.nvram         ST Compatible Serial flash offset 00FF0000 size 64KB
    flash1.boot          ST Compatible Serial flash offset 00000000 size 256KB
    flash1.boot2         ST Compatible Serial flash offset 00040000 size 256KB
    flash1.trx           ST Compatible Serial flash offset 00080000 size 15808KB
    flash1.nvram         ST Compatible Serial flash offset 00FF0000 size 64KB
    eth0                 Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller
    *** command status = 0
    CFE>
    CFE> flash -noheader 192.168.0.20:openwrt-19.07.4-bcm53xx-tenda-ac9-squashfs.trx flash0.trx
    Reading 192.168.0.20:openwrt-19.07.4-bcm53xx-tenda-ac9-squashfs.trx: Done. 4657152 bytes read
    Programming...done. 4657152 bytes written
    *** command status = 0
    CFE>

The good news is that Tenda AC9 firmware successfully boot (the first
time):

    CFE> reboot
    Decompressing...done


    CFE version 9.10.178.50 (r635252) based on BBP 1.0.37 for BCM947XX (32bit,SP,)
    Build Date: Thu Sep  8 14:49:19 CST 2016 (seal@seal-pc)
    Copyright (C) 2000-2008 Broadcom Corporation.

    Init Arena
    Init Devs.
    Boot partition size = 262144(0x40000)
    DDR Clock: 533 MHz
    Info: DDR frequency set from clkfreq=900,*533*
    No GPIO defined for BBSI interface
    No BBSI device
    bcm_robo_enable_switch: EEE is disabled
    et0: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    CPU type 0x0: 900MHz
    Tot mem: 131072 KBytes

    CFE mem:    0x00F00000 - 0x02FB912C (34312492)
    Data:       0x00F6B754 - 0x00F70C04 (21680)
    BSS:        0x00F70C10 - 0x00FB712C (288028)
    Heap:       0x00FB712C - 0x02FB712C (33554432)
    Stack:      0x02FB712C - 0x02FB912C (8192)
    Text:       0x00F00000 - 0x00F5F4F4 (390388)

    Device eth0:  hwaddr AA-BB-CC-DD-EE-00, ipaddr 192.168.0.1, mask 255.255.255.0
            gateway not set, nameserver not set
    Reading Partition Table from NVRAM ... OK
    Parsing Partition Table ... OK
    factory boot check integer ok.
    factory boot load fs fs boot len 262144 to addr 0x3f00000.
    Decompressing...done


    CFE version 9.10.178.50 (r635252) based on BBP 1.0.37 for BCM947XX (32bit,SP,)
    Build Date: Thu Sep  8 14:48:53 CST 2016 (seal@seal-pc)
    Copyright (C) 2000-2008 Broadcom Corporation.

    Init Arena
    Init Devs.
    Boot partition size = 262144(0x40000)
    DDR Clock: 533 MHz
    Info: DDR frequency set from clkfreq=900,*533*
    No GPIO defined for BBSI interface
    No BBSI device
    bcm_robo_enable_switch: EEE is disabled
    et0: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    CPU type 0x0: 900MHz
    Tot mem: 131072 KBytes

    CFE mem:    0x00F00000 - 0x02FB1ACC (34282188)
    Data:       0x00F6933C - 0x00F69AD8 (1948)
    BSS:        0x00F69AE8 - 0x00FAFACC (286692)
    Heap:       0x00FAFACC - 0x02FAFACC (33554432)
    Stack:      0x02FAFACC - 0x02FB1ACC (8192)
    Text:       0x00F00000 - 0x00F5D4EC (382188)

    Device eth0:  hwaddr AA-BB-CC-DD-EE-00, ipaddr 192.168.0.1, mask 255.255.255.0
            gateway not set, nameserver not set
    Loader:raw Filesys:raw Dev:flash0.os File: Options:(null)
    Loading: ... 1796697 bytes read
    Entry at 0x00008000
    Closing network.
    Starting program at 0x00008000
    Uncompressing Linux... done, booting the kernel.
    [    0.000000] Booting Linux on physical CPU 0x0
    [    0.000000] Linux version 4.14.195 (builder@buildhost) (gcc version 7.5.0 (OpenWrt GCC 7.5.0 r11208-ce6496d796)) #0 SMP Sun Sep 6 16:19:390
    [    0.000000] CPU: ARMv7 Processor [410fc075] revision 5 (ARMv7), cr=10c5387d
    [    0.000000] CPU: div instructions available: patching division code
    [    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
    [    0.000000] OF: fdt: Machine model: Tenda AC9
    [    0.000000] earlycon: ns16550a0 at MMIO 0x18000300 (options '115200n8')
    [    0.000000] bootconsole [ns16550a0] enabled
    [    0.000000] Memory policy: Data cache writealloc
    [    0.000000] Hit pending asynchronous external abort (FSR=0x00000c06) during first unmask, this is most likely caused by a firmware/bootloa.
    [    0.000000] random: get_random_bytes called from 0xc06009a8 with crng_init=0
    [    0.000000] percpu: Embedded 14 pages/cpu s26444 r8192 d22708 u57344
    [    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 32512
    [    0.000000] Kernel command line: console=ttyS0,115200 earlycon
    [    0.000000] PID hash table entries: 512 (order: -1, 2048 bytes)
    [    0.000000] Dentry cache hash table entries: 16384 (order: 4, 65536 bytes)
    [    0.000000] Inode-cache hash table entries: 8192 (order: 3, 32768 bytes)
    [    0.000000] Memory: 123252K/131072K available (4217K kernel code, 121K rwdata, 572K rodata, 1024K init, 288K bss, 7820K reserved, 0K cma-r)
    [    0.000000] Virtual kernel memory layout:
    [    0.000000]     vector  : 0xffff0000 - 0xffff1000   (   4 kB)
    [    0.000000]     fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
    [    0.000000]     vmalloc : 0xc8800000 - 0xff800000   ( 880 MB)
    [    0.000000]     lowmem  : 0xc0000000 - 0xc8000000   ( 128 MB)
    [    0.000000]     pkmap   : 0xbfe00000 - 0xc0000000   (   2 MB)
    [    0.000000]     modules : 0xbf000000 - 0xbfe00000   (  14 MB)
    [    0.000000]       .text : 0xc0008000 - 0xc051e500   (5210 kB)
    [    0.000000]       .init : 0xc0600000 - 0xc0700000   (1024 kB)
    [    0.000000]       .data : 0xc0700000 - 0xc071e6c0   ( 122 kB)
    [    0.000000]        .bss : 0xc071e6c0 - 0xc0766888   ( 289 kB)
    [    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=1, Nodes=1
    [    0.000000] Hierarchical RCU implementation.
    [    0.000000]  RCU restricting CPUs from NR_CPUS=2 to nr_cpu_ids=1.
    [    0.000000] RCU: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=1
    [    0.000000] NR_IRQS: 16, nr_irqs: 16, preallocated irqs: 16
    [    0.000000] arch_timer: cp15 timer(s) running at 0.03MHz (virt).
    [    0.000000] clocksource: arch_sys_counter: mask: 0xffffffffffffff max_cycles: 0x105b97d64, max_idle_ns: 56421785873582 ns
    [    0.000000] sched_clock: 56 bits at 34kHz, resolution 28875ns, wraps every 70368744172677ns
    [    0.008749] Ignoring delay timer 0xc071f228, which has insufficient resolution of 28875ns
    [    0.017469] Calibrating delay loop... 1790.77 BogoMIPS (lpj=8953856)
    [    0.084084] pid_max: default: 32768 minimum: 301
    [    0.089108] Mount-cache hash table entries: 1024 (order: 0, 4096 bytes)
    [    0.096038] Mountpoint-cache hash table entries: 1024 (order: 0, 4096 bytes)
    [    0.104181] CPU: Testing write buffer coherency: ok
    [    0.109696] /cpus/cpu@0 missing clock-frequency property
    [    0.115355] CPU0: thread -1, cpu 0, socket 0, mpidr 80000000
    [    0.121881] Setting up static identity map for 0x100000 - 0x10003c
    [    0.128667] Hierarchical SRCU implementation.
    [    0.133922] smp: Bringing up secondary CPUs ...
    [    0.138744] smp: Brought up 1 node, 1 CPU
    [    0.142931] SMP: Total of 1 processors activated (1790.77 BogoMIPS).
    [    0.149630] CPU: All CPU(s) started in SVC mode.
    [    0.156271] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
    [    0.166666] futex hash table entries: 256 (order: 2, 16384 bytes)
    [    0.173192] pinctrl core: initialized pinctrl subsystem
    [    0.179978] NET: Registered protocol family 16
    [    0.184944] DMA: preallocated 256 KiB pool for atomic coherent allocations
    [    0.211682] clocksource: Switched to clocksource arch_sys_counter
    [    0.219392] NET: Registered protocol family 2
    [    0.224763] TCP established hash table entries: 1024 (order: 0, 4096 bytes)
    [    0.232184] TCP bind hash table entries: 1024 (order: 1, 8192 bytes)
    [    0.238854] TCP: Hash tables configured (established 1024 bind 1024)
    [    0.245697] UDP hash table entries: 256 (order: 1, 8192 bytes)
    [    0.251848] UDP-Lite hash table entries: 256 (order: 1, 8192 bytes)
    [    0.258662] NET: Registered protocol family 1
    [    0.267036] Crashlog allocated RAM at address 0x3f00000
    [    0.274803] workingset: timestamp_bits=30 max_order=15 bucket_order=0
    [    0.285371] squashfs: version 4.0 (2009/01/31) Phillip Lougher
    [    0.291551] jffs2: version 2.2 (NAND) (SUMMARY) (LZMA) (RTIME) (CMODE_PRIORITY) (c) 2001-2006 Red Hat, Inc.
    [    0.312832] io scheduler noop registered
    [    0.316961] io scheduler deadline registered (default)
    [    0.323746] Serial: 8250/16550 driver, 16 ports, IRQ sharing enabled
    [    0.338357] libphy: Fixed MDIO Bus: probed
    [    0.342862] bgmac_bcma: Broadcom 47xx GBit MAC driver loaded
    [    0.349070] bcma-host-soc 18000000.axi: bus0: Found chip with id 53573, rev 0x03 and package 0x01
    [    0.358627] bcma-host-soc 18000000.axi: bus0: Core 0 found: ChipCommon (manuf 0x4BF, id 0x800, rev 0x36, class 0x0)
    [    0.369802] bcma-host-soc 18000000.axi: bus0: Core 1 found: IEEE 802.11 (manuf 0x4BF, id 0x812, rev 0x38, class 0x0)
    [    0.381006] bcma-host-soc 18000000.axi: bus0: Core 2 found: PCIe Gen 2 (manuf 0x4BF, id 0x501, rev 0x05, class 0x0)
    [    0.392122] bcma-host-soc 18000000.axi: bus0: Core 3 found: ARM CA7 (manuf 0x4BF, id 0x847, rev 0x00, class 0x0)
    [    0.402979] bcma-host-soc 18000000.axi: bus0: Core 4 found: USB 2.0 Host (manuf 0x4BF, id 0x819, rev 0x05, class 0x0)
    [    0.414327] bcma-host-soc 18000000.axi: bus0: Core 5 found: GBit MAC (manuf 0x4BF, id 0x82D, rev 0x08, class 0x0)
    [    0.425242] bcma-host-soc 18000000.axi: bus0: Core 6 found: I2S (manuf 0x4BF, id 0x834, rev 0x06, class 0x0)
    [    0.435695] bcma-host-soc 18000000.axi: bus0: Core 7 found: CNDS DDR2/3 memory controller (manuf 0x4BF, id 0x846, rev 0x00, class 0x0)
    [    0.448486] bcma-host-soc 18000000.axi: bus0: Core 8 found: NAND flash controller (manuf 0x4BF, id 0x509, rev 0x01, class 0x0)
    [    0.460643] bcma-host-soc 18000000.axi: bus0: Core 9 found: IEEE 802.11 (manuf 0x4BF, id 0x812, rev 0x38, class 0x0)
    [    0.471904] bcma-host-soc 18000000.axi: bus0: Core 10 found: GBit MAC (manuf 0x4BF, id 0x82D, rev 0x08, class 0x0)
    [    0.482905] bcma-host-soc 18000000.axi: bus0: Core 11 found: I2S (manuf 0x4BF, id 0x834, rev 0x06, class 0x0)
    [    0.493416] bcma-host-soc 18000000.axi: bus0: Core 12 found: GCI (manuf 0x4BF, id 0x840, rev 0x08, class 0x0)
    [    0.503955] bcma-host-soc 18000000.axi: bus0: Core 13 found: PMU (manuf 0x4BF, id 0x827, rev 0x1C, class 0x0)
    [    0.514437] bcma-host-soc 18000000.axi: bus0: Found M25FL128 serial flash (size: 16384KiB, blocksize: 0x10000, blocks: 256)
    [    0.526882] console [ttyS0] disabled
    [    0.530694] 18000300.serial: ttyS0 at MMIO 0x18000300 (irq = 20, base_baud = 2500000) is a 16550A
    [    0.540107] console [ttyS0] enabled
    [    0.540107] console [ttyS0] enabled
    [    0.547326] bootconsole [ns16550a0] disabled
    [    0.547326] bootconsole [ns16550a0] disabled
    [    0.642902] 4 bcm47xxpart partitions found on MTD device bcm47xxsflash
    [    0.649543] Creating 4 MTD partitions on "bcm47xxsflash":
    [    0.655058] 0x000000000000-0x000000040000 : "boot"
    [    0.660776] 0x000000040000-0x000000080000 : "boot"
    [    0.666435] 0x000000080000-0x000000ff0000 : "firmware"
    [    0.672528] 2 trx partitions found on MTD device firmware
    [    0.678014] Creating 2 MTD partitions on "firmware":
    [    0.683125] 0x00000000001c-0x0000001ba400 : "linux"
    [    0.688813] 0x0000001ba400-0x000000f70000 : "rootfs"
    [    0.694646] mtd: device 4 (rootfs) set to be root filesystem
    [    0.700421] 1 squashfs-split partitions found on MTD device rootfs
    [    0.706745] 0x000000430000-0x000000f70000 : "rootfs_data"
    [    0.713011] 0x000000ff0000-0x000001000000 : "nvram"
    [    0.861515] pcie_iproc_bcma bcma0:2: link: UP
    [    0.866193] pcie_iproc_bcma bcma0:2: PCI host bridge to bus 0000:00
    [    0.872632] pci_bus 0000:00: root bus resource [mem 0x10000000-0x17ffffff]
    [    0.879591] pci_bus 0000:00: No busn resource found for root bus, will use [bus 00-ff]
    [    0.887733] pci_bus 0000:00: 2-byte config write to 0000:00:00.0 offset 0x4 may corrupt adjacent RW1C bits
    [    0.897551] pci_bus 0000:00: 2-byte config write to 0000:00:00.0 offset 0x4 may corrupt adjacent RW1C bits
    [    0.907455] pci_bus 0000:00: 2-byte config write to 0000:00:00.0 offset 0x4c may corrupt adjacent RW1C bits
    [    0.917590] pci_bus 0000:00: 2-byte config write to 0000:00:00.0 offset 0x3e may corrupt adjacent RW1C bits
    [    0.927523] pci_bus 0000:00: 2-byte config write to 0000:00:00.0 offset 0x4 may corrupt adjacent RW1C bits
    [    0.937341] pci_bus 0000:00: 1-byte config write to 0000:00:00.0 offset 0xc may corrupt adjacent RW1C bits
    [    0.947158] PCI: bus0: Fast back to back transfers disabled
    [    0.952818] pci_bus 0000:00: 2-byte config write to 0000:00:00.0 offset 0x3e may corrupt adjacent RW1C bits
    [    0.962722] pci_bus 0000:00: 2-byte config write to 0000:00:00.0 offset 0xc8 may corrupt adjacent RW1C bits
    [    0.972886] pci_bus 0000:01: 2-byte config write to 0000:01:00.0 offset 0x4 may corrupt adjacent RW1C bits
    [    0.982732] pci_bus 0000:01: 2-byte config write to 0000:01:00.0 offset 0x4 may corrupt adjacent RW1C bits
    [    0.992636] pci 0000:01:00.0: enabling Extended Tags
    [    0.997978] PCI: bus1: Fast back to back transfers disabled
    [    1.003753] pci 0000:00:00.0: BAR 8: assigned [mem 0x10000000-0x100fffff]
    [    1.010654] pci 0000:01:00.0: BAR 0: assigned [mem 0x10000000-0x10007fff 64bit]
    [    1.018133] pci 0000:00:00.0: PCI bridge to [bus 01]
    [    1.023186] pci 0000:00:00.0:   bridge window [mem 0x10000000-0x100fffff]
    [    1.030549] bgmac_bcma bcma0:5: Found PHY addr: 30 (NOREGS)
    [    1.039096] Broadcom B53 (2) bcma_mdio-0-0:1e: failed to register switch: -517
    [    1.046604] libphy: bcma_mdio mii bus: probed
    [    1.051022] bgmac_bcma bcma0:5: Support for Roboswitch not implemented
    [    1.058760] bgmac_bcma bcma0:5: Timeout waiting for reg 0x1E0
    [    1.066585] bgmac_bcma bcma0:10: Found PHY addr: 30 (NOREGS)
    [    1.072418] bgmac_bcma bcma0:10: Support for Roboswitch not implemented
    [    1.080185] bgmac_bcma bcma0:10: Timeout waiting for reg 0x1E0
    [    1.089916] bcm47xx-wdt bcm47xx-wdt.0: BCM47xx Watchdog Timer enabled (30 seconds)
    [    1.097770] bcma-host-soc 18000000.axi: bus0: Bus registered
    [    1.103834] pci 0000:00:00.0: enabling device (0140 -> 0142)
    [    1.109580] bcma-pci-bridge 0000:01:00.0: enabling device (0140 -> 0142)
    [    1.116510] bcma-pci-bridge 0000:01:00.0: bus1: Found chip with id 43217, rev 0x01 and package 0x09
    [    1.125808] bcma-pci-bridge 0000:01:00.0: bus1: Core 0 found: ChipCommon (manuf 0x4BF, id 0x800, rev 0x27, class 0x0)
    [    1.136694] bcma-pci-bridge 0000:01:00.0: bus1: Core 1 found: IEEE 802.11 (manuf 0x4BF, id 0x812, rev 0x1E, class 0x0)
    [    1.147666] bcma-pci-bridge 0000:01:00.0: bus1: Core 2 found: PCIe (manuf 0x4BF, id 0x820, rev 0x14, class 0x0)
    [    1.182634] can not parse nvram name 0:ag2(null) with value 0xFF got -34
    [    1.189420] can not parse nvram name 0:ag3(null) with value 0xFF got -34
    [    1.262012] bcma-pci-bridge 0000:01:00.0: bus1: Bus registered
    [    1.268768] NET: Registered protocol family 10
    [    1.276478] Segment Routing with IPv6
    [    1.280289] NET: Registered protocol family 17
    [    1.284996] bridge: filtering via arp/ip/ip6tables is no longer available by default. Update your scripts to load br_netfilter if you need.
    [    1.298163] 8021q: 802.1Q VLAN Support v1.8
    [    1.302523] Registering SWP/SWPB emulation handler
    [    1.316152] VFS: Mounted root (squashfs filesystem) readonly on device 31:4.
    [    1.324959] Freeing unused kernel memory: 1024K
    [    1.813611] init: Console is alive
    [    1.817423] init: - watchdog -
    [    2.434338] kmodloader: loading kernel modules from /etc/modules-boot.d/*
    [    2.668485] usbcore: registered new interface driver usbfs
    [    2.674289] usbcore: registered new interface driver hub
    [    2.679804] usbcore: registered new device driver usb
    [    2.691181] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
    [    2.699526] ehci-platform: EHCI generic platform driver
    [    2.705243] ehci-platform 18004000.ehci: EHCI Host Controller
    [    2.711105] ehci-platform 18004000.ehci: new USB bus registered, assigned bus number 1
    [    2.719392] ehci-platform 18004000.ehci: irq 23, io mem 0x18004000
    [    2.751761] ehci-platform 18004000.ehci: USB 2.0 started, EHCI 1.00
    [    2.759211] hub 1-0:1.0: USB hub found
    [    2.763571] hub 1-0:1.0: 2 ports detected
    [    2.772002] ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
    [    2.779856] ohci-platform: OHCI generic platform driver
    [    2.785545] ohci-platform 1800d000.ohci: Generic Platform OHCI controller
    [    2.792561] ohci-platform 1800d000.ohci: new USB bus registered, assigned bus number 2
    [    2.800733] ohci-platform 1800d000.ohci: irq 23, io mem 0x1800d000
    [    2.876848] hub 2-0:1.0: USB hub found
    [    2.881092] hub 2-0:1.0: 2 ports detected
    [    2.889986] kmodloader: done loading kernel modules from /etc/modules-boot.d/*
    [    2.922008] init: - preinit -
    [    3.595836] random: jshn: uninitialized urandom read (4 bytes read)
    [    3.652402] random: jshn: uninitialized urandom read (4 bytes read)
    [    3.965638] random: jshn: uninitialized urandom read (4 bytes read)
    Failed to connect to the switch. Use the "list" command to see which switches are available.
    Failed to connect to the switch. Use the "list" command to see which switches are available.
    Failed to connect to the switch. Use the "list" command to see which switches are available.
    Failed to connect to the switch. Use the "list" command to see which switches are available.
    [    4.328309] bgmac_bcma bcma0:5: Timeout waiting for reg 0x1E0
    [    4.335036] bcma-host-soc 18000000.axi: bus0: No bus clock specified for D145 device, pmu rev. 28, using default 80000000 Hz
    [    4.346817] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready
    [    4.352939] IPv6: ADDRCONF(NETDEV_UP): eth0.1: link is not ready
    Press the [f] key and hit [enter] to enter failsafe mode
    Press the [1], [2], [3] or [4] key and hit [enter] to select the debug level
    [    7.736688] mount_root: jffs2 not ready yet, using temporary tmpfs overlay
    [    7.764033] urandom-seed: Seed file not found (/etc/urandom.seed)
    [    7.847626] bgmac_bcma bcma0:5: Timeout waiting for reg 0x1E0
    [    7.901218] procd: - early -
    [    7.905174] procd: - watchdog -
    [    8.551686] procd: - watchdog -
    [    8.572100] procd: - ubus -
    [    8.619513] urandom_read: 3 callbacks suppressed
    [    8.619513] random: ubusd: uninitialized urandom read (4 bytes read)
    [    8.668225] random: ubusd: uninitialized urandom read (4 bytes read)
    [    8.675386] random: ubusd: uninitialized urandom read (4 bytes read)
    [    8.683616] procd: - init -
    Please press Enter to activate this console.
    [    9.180440] urngd: jent-rng init failed, err: 2
    [    9.301224] kmodloader: loading kernel modules from /etc/modules.d/*
    [    9.314708] ip6_tables: (C) 2000-2006 Netfilter Core Team
    [    9.331947] Loading modules backported from Linux version v4.19.137-0-gc076c79e03c6
    [    9.339714] Backport generated by backports.git v4.19.137-1-0-g60c3a249
    [    9.349763] ip_tables: (C) 2000-2006 Netfilter Core Team
    [    9.363190] nf_conntrack version 0.5.0 (2048 buckets, 8192 max)
    [    9.428101] xt_time: kernel timezone is -0000
    [    9.470287] PPP generic driver version 2.4.2
    [    9.477650] NET: Registered protocol family 24
    [    9.487525] b43-phy0: Broadcom 43217 WLAN found (core revision 30)
    [    9.501674] b43-phy0: Found PHY: Analog 9, Type 4 (N), Revision 17
    [    9.507969] b43-phy0: Found Radio: Manuf 0x17F, ID 0x2057, Revision 14, Version 0
    [    9.521858] Broadcom 43xx driver loaded [ Features: PNL ]
    [    9.532859] kmodloader: done loading kernel modules from /etc/modules.d/*
    [   27.785198] bgmac_bcma bcma0:5: Timeout waiting for reg 0x1E0
    [   27.791926] bcma-host-soc 18000000.axi: bus0: No bus clock specified for D145 device, pmu rev. 28, using default 80000000 Hz
    [   27.803649] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready
    [   27.873180] br-lan: port 1(eth0.1) entered blocking state
    [   27.878667] br-lan: port 1(eth0.1) entered disabled state
    [   27.884673] device eth0.1 entered promiscuous mode
    [   27.889524] device eth0 entered promiscuous mode
    [   27.973492] IPv6: ADDRCONF(NETDEV_UP): br-lan: link is not ready
    [   28.040915] bgmac_bcma bcma0:10: Timeout waiting for reg 0x1E0
    [   28.047441] bcma-host-soc 18000000.axi: bus0: No bus clock specified for D145 device, pmu rev. 28, using default 80000000 Hz
    [   28.059309] IPv6: ADDRCONF(NETDEV_UP): eth1: link is not ready
    [   28.202067] device eth1 entered promiscuous mode
    [   28.206976] IPv6: ADDRCONF(NETDEV_UP): eth1.2: link is not ready
    [   29.081802] bgmac_bcma bcma0:10 eth1: Link is Up - 1Gbps/Full - flow control off
    [   29.089339] IPv6: ADDRCONF(NETDEV_CHANGE): eth1: link becomes ready
    [   29.139553] IPv6: ADDRCONF(NETDEV_CHANGE): eth1.2: link becomes ready
    [   30.027142] jffs2_scan_eraseblock(): End of filesystem marker found at 0x0
    [   30.066874] jffs2_build_filesystem(): unlocking the mtd device...
    [   30.066903] done.



    BusyBox v1.30.1 () built-in shell (ash)

      _______                     ________        __
     |       |.-----.-----.-----.|  |  |  |.----.|  |_
     |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|
     |_______||   __|_____|__|__||________||__|  |____|
              |__| W I R E L E S S   F R E E D O M
     -----------------------------------------------------
     OpenWrt 19.07.4, r11208-ce6496d796
     -----------------------------------------------------
    === WARNING! =====================================
    There is no root password defined on this device!
    Use the "passwd" command to set up a new password
    in order to prevent unauthorized SSH logins.
    --------------------------------------------------
    root@OpenWrt:/# cat /proc/cpuinfo
    processor       : 0
    model name      : ARMv7 Processor rev 5 (v7l)
    BogoMIPS        : 1790.77
    Features        : half thumb fastmult edsp tls idiva idivt lpae evtstrm
    CPU implementer : 0x41
    CPU architecture: 7
    CPU variant     : 0x0
    CPU part        : 0xc07
    CPU revision    : 5

    Hardware        : Generic DT based system
    Revision        : 0000
    Serial          : 0000000000000000
    root@OpenWrt:/# top
    Mem: 22092K used, 102184K free, 108K shrd, 2064K buff, 6604K cached
    CPU:   0% usr   0% sys   0% nic  99% idle   0% io   0% irq   0% sirq
    Load average: 0.88 0.38 0.14 1/46 1554
      PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
     1554   569 root     R     1120   1%   0% top
      927     1 root     S     1876   2%   0% /sbin/rpcd -s /var/run/ubus.sock -t 30
     1084     1 root     S     1528   1%   0% /sbin/netifd
        1     0 root     S     1400   1%   0% /sbin/procd
     1121     1 root     S     1288   1%   0% /usr/sbin/odhcpd
      990     1 dnsmasq  S     1216   1%   0% /usr/sbin/dnsmasq -C /var/etc/dnsmasq.
     1540     1 root     S     1192   1%   0% /bin/sh /sbin/urandom_seed
     1177     1 root     S     1148   1%   0% /usr/sbin/uhttpd -f -h /www -r OpenWrt
      569     1 root     S     1128   1%   0% /bin/ash --login
     1399  1084 root     S     1120   1%   0% udhcpc -p /var/run/udhcpc-eth1.2.pid -
     1523     1 root     S<    1120   1%   0% /usr/sbin/ntpd -n -N -S /usr/sbin/ntpd
      896     1 root     S     1072   1%   0% /sbin/logd -S 64
      568     1 root     S     1040   1%   0% /sbin/ubusd
     1396  1084 root     S      880   1%   0% odhcp6c -s /lib/netifd/dhcpv6.script -
     1027     1 root     S      880   1%   0% /usr/sbin/dropbear -F -P /var/run/drop
     1552  1540 root     S      812   1%   0% getrandom 512
      116     2 root     IW       0   0%   0% [kworker/0:1]
        8     2 root     IW       0   0%   0% [rcu_sched]
       12     2 root     IW       0   0%   0% [kworker/u2:1]
    ^X^C7     2 root     SW       0   0%   0% [ksoftirqd/0]
    root@OpenWrt:/# df
    Filesystem           1K-blocks      Used Available Use% Mounted on
    /dev/root                 2560      2560         0 100% /rom
    tmpfs                    62136        56     62080   0% /tmp
    tmpfs                    62136        56     62080   0% /tmp/root
    tmpfs                      512         0       512   0% /dev
    root@OpenWrt:/#

But after rebooting, the bootloader complains about an `invalid
partition-index-file para id`. And rebooting again or reflashing the
same firmware produces the same outcome.

    root@OpenWrt:/# reboot
    root@OpenWrt:/# [  125.151940] device eth0.1 left promiscuous mode
    [  125.156560] device eth0 left promiscuous mode
    [  125.161209] br-lan: port 1(eth0.1) entered disabled state
    [  125.182288] IPv6: ADDRCONF(NETDEV_UP): eth0.1: link is not ready
    [  125.223896] bgmac_bcma bcma0:5: Timeout waiting for reg 0x1E0
    [  125.514062] device eth1 left promiscuous mode
    [  125.553361] bgmac_bcma bcma0:10: Timeout waiting for reg 0x1E0
    [  129.642469] reboot: Restarting system
    Decompressing...done


    CFE version 9.10.178.50 (r635252) based on BBP 1.0.37 for BCM947XX (32bit,SP,)
    Build Date: Thu Sep  8 14:49:19 CST 2016 (seal@seal-pc)
    Copyright (C) 2000-2008 Broadcom Corporation.

    Init Arena
    Init Devs.
    Boot partition size = 262144(0x40000)
    DDR Clock: 533 MHz
    Info: DDR frequency set from clkfreq=900,*533*
    No GPIO defined for BBSI interface
    No BBSI device
    bcm_robo_enable_switch: EEE is disabled
    et0: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    CPU type 0x0: 900MHz
    Tot mem: 131072 KBytes

    CFE mem:    0x00F00000 - 0x02FB912C (34312492)
    Data:       0x00F6B754 - 0x00F70C04 (21680)
    BSS:        0x00F70C10 - 0x00FB712C (288028)
    Heap:       0x00FB712C - 0x02FB712C (33554432)
    Stack:      0x02FB712C - 0x02FB912C (8192)
    Text:       0x00F00000 - 0x00F5F4F4 (390388)

    Device eth0:  hwaddr AA-BB-CC-DD-EE-00, ipaddr 192.168.0.1, mask 255.255.255.0
            gateway not set, nameserver not set
    Reading Partition Table from NVRAM ... OK
    Parsing Partition Table ... [NM_Error](nm_lib_parsePtnIndexFile) 00548: invalid partition-index-file para id.
    FAILED
    factory boot check integer partition init fail.
    Device eth0:  hwaddr AA-BB-CC-DD-EE-00, ipaddr 192.168.0.1, mask 255.255.255.0
            gateway not set, nameserver not set
    CFE>


# (Failing to) restore factory firmware

As we have seen before I mistakenly backed up 16 MB of garbage instead
of the device's factory firmware. I also did a dump skipping the first
512 KB, so that I could avoid reflashing the boot devices (that at
least saved me from nucking the boot loader). So here's what happened
when I flashed garbage on the whole flash (including the NVRAM
partition), except the `flash0.boot` and `flash.boot2` devices.

    CFE> show devices
    Device Name          Description
    -------------------  ---------------------------------------------------------
    uart0                NS16550 UART at 0x18000300
    flash0               ST Compatible Serial flash size 16384KB
    flash0.boot          ST Compatible Serial flash offset 00000000 size 256KB
    flash0.boot2         ST Compatible Serial flash offset 00040000 size 256KB
    flash0.trx           ST Compatible Serial flash offset 00080000 size 1KB
    flash0.os            ST Compatible Serial flash offset 0008001C size 15808KB
    flash0.nvram         ST Compatible Serial flash offset 00FF0000 size 64KB
    flash1.boot          ST Compatible Serial flash offset 00000000 size 256KB
    flash1.boot2         ST Compatible Serial flash offset 00040000 size 256KB
    flash1.trx           ST Compatible Serial flash offset 00080000 size 15808KB
    flash1.nvram         ST Compatible Serial flash offset 00FF0000 size 64KB
    eth0                 Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller
    *** command status = 0
    CFE>
    CFE> flash -noheader 192.168.0.20:archer-c1200.trx flash0.trx
    Reading 192.168.0.20:archer-c1200.trx: Done. 16252928 bytes read
    Programming...done. 16252928 bytes written
    *** command status = 0
    CFE>
    CFE> reboot
    Decompressing...done


    CFE version 9.10.178.50 (r635252) based on BBP 1.0.37 for BCM947XX (32bit,SP,)
    Build Date: Thu Sep  8 14:49:19 CST 2016 (seal@seal-pc)
    Copyright (C) 2000-2008 Broadcom Corporation.

    Init Arena
    Init Devs.
    Boot partition size = 262144(0x40000)
    DDR Clock: 533 MHz
    Info: DDR frequency set from clkfreq=900,*533*
    No GPIO defined for BBSI interface
    No BBSI device
    bcm_robo_enable_switch: EEE is disabled
    et0: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    CPU type 0x0: 900MHz
    Tot mem: 131072 KBytes

    CFE mem:    0x00F00000 - 0x02FB912C (34312492)
    Data:       0x00F6B754 - 0x00F70C04 (21680)
    BSS:        0x00F70C10 - 0x00FB712C (288028)
    Heap:       0x00FB712C - 0x02FB712C (33554432)
    Stack:      0x02FB712C - 0x02FB912C (8192)
    Text:       0x00F00000 - 0x00F5F4F4 (390388)

    Committing NVRAM...done
    �Decompressing...doneton release...done


    CFE version 9.10.178.50 (r635252) based on BBP 1.0.37 for BCM947XX (32bit,SP,)
    Build Date: Thu Sep  8 14:49:19 CST 2016 (seal@seal-pc)
    Copyright (C) 2000-2008 Broadcom Corporation.

    Init Arena
    Init Devs.
    Boot partition size = 262144(0x40000)
    DDR Clock: 533 MHz
    Info: DDR frequency set from clkfreq=900,*533*
    No GPIO defined for BBSI interface
    No BBSI device
    bcm_robo_enable_switch: EEE is disabled
    et0: Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller 9.10.178.50 (r635252)
    CPU type 0x0: 900MHz
    Tot mem: 131072 KBytes

    CFE mem:    0x00F00000 - 0x02FB912C (34312492)
    Data:       0x00F6B754 - 0x00F70C04 (21680)
    BSS:        0x00F70C10 - 0x00FB712C (288028)
    Heap:       0x00FB712C - 0x02FB712C (33554432)
    Stack:      0x02FB712C - 0x02FB912C (8192)
    Text:       0x00F00000 - 0x00F5F4F4 (390388)

    Device eth0:  hwaddr AA-BB-CC-DD-EE-00, ipaddr 192.168.1.1, mask 255.255.255.0
            gateway not set, nameserver not set
    Reading Partition Table from NVRAM ... OK
    Parsing Partition Table ... OK
    [NM_Error](nm_api_readPtnFromNvram) 00134: partition name not found.

    factory boot check integer read flag partition fail.
    Device eth0:  hwaddr AA-BB-CC-DD-EE-00, ipaddr 192.168.0.1, mask 255.255.255.0
            gateway not set, nameserver not set
    CFE>

If you look carefully, you will notice that the router rebooted
twice. The first reboot ended up with a `Committing NVRAM...done`,
which I believe corresponds to the bootloader repopulating the NVRAM
that I mistakenly erased.

So here it is. The partition table has apparently been fixed by the
bootloader repopulating the NVRAM (at least the bootloader says
`OK`). But now it fails one line further saying `partition name not
found`. Since then, I haven't been able to fix this error. I tried the
flash the images built by [\_NewAge][16] for the *Archer C1200 V1*
(available on its [Google Drive][15]):

* `openwrt-bcm53xx-tplink-archer-c1200-v1-initramfs.trx`
* `openwrt-bcm53xx-tplink-archer-c1200-v1-squashfs.trx`

Also I tried to flash the stock firmware downloaded from [tp-link
official firmware page][9], by using the web UI exposed by the
bootloader (on http://192.168.0.1), selecting the 'C1200v2_eu-up-2.0.2
Build 20180118 rel.38979.bin' image, and clicking the 'Upgrade'
button. The process stops at '40%' with the following message:

    Upgrade failed. The firmware version is not compatible with
    the Archer C1200 router.

Also on the console I get the following messages (written by the
bootloader while I was trying to flash the stock firmware from the web
UI):

    CFE> Firmware process id 2.
    Httpd Firmware Recovery file length : 15193161
    [NM_Error](nm_api_readPtnFromNvram) 00134: partition name not found.

    [Error]sysmgr_cfg_getProductInfoFromNvram():00744 @ ucm_nvram_proInfoRead() failed.
    [Error]sysmgr_cfg_checkSupportList():00921 @ productName Archer C1200 NOT Match.
    [Error]sysmgr_cfg_checkSupportList():00921 @ productName Archer C1200 NOT Match.
    Firmwave not supports, check failed.
    [NM_Error](nm_checkUpdateContent) 01110: the firmware is not for this model
    [NM_Error](nm_buildUpgradeStruct) 01210: checkUpdateContent failed.
    [NM_Error](nm_tpHttpdFirmwareCheck) 01322: check firmware error!

    Firmware check error!

I also tried to erase the NVRAM one more time with 64 KB of zeros,
which led to the NVRAM being repopulated by the bootloader and the
same error coming back. Note that the NVRAM looks ok (though I am not
able to compare with the factory state):

    CFE> nvram show
    0:ag1=0x2
    0:ag2=0xFF
    0:cck2gpo=0x2222
    0:ag3=0xFF
    0:rssismf2g=0x0
    boardrev=0x1201
    sb/1/olpc_thresh5g=7
    sb/1/rxgains5ghtrisoa0=5
    sb/1/rxgains5ghtrisoa1=5
    et0macaddr=AA:BB:CC:DD:EE:00
    sb/1/mcsbw205glpo=0xfecb9752
    sb/1/sb40and80lr5gmpo=0
    0:ledbh0=11
    0:ledbh1=11
    boot_wait=off
    watchdog=3000
    devpath0=pci/1/1/
    0:ledbh2=11
    sb/1/temps_period=5
    0:ledbh3=11
    sb/1/dot11agduplrpo=0
    et0mdcport=0
    sb/1/gainctrlsph=0
    sb/1/mcsbw805gmpo=0xfeda9742
    0:venid=0x14e4
    0:aa2g=3
    sb/1/pdgain5g=0
    sb/1/mcsbw205ghpo=0xfecb9752
    pmon_ver=CFE 9.10.178.50 (r635252)
    0:rxpo2g=0x0
    0:pdetrange2g=2
    vlan2ports=0 5u
    sb/1/sb20in80and160lr5glpo=0
    need_firmware=1
    sb/1/swctrlmapext_2g=0x00000000,0x00000000,0x00000000,0x000000,0x000
    sb/1/sromrev=11
    sb/1/rxgains5gmelnagaina0=4
    sb/1/rxgains5gmelnagaina1=4
    0:pa2gw1a0=0x17f6
    sb/1/rssi_delta_5gml_c0=-4,0,-5,0,-5,0
    0:elna2g=0
    0:pa2gw1a1=0x1811
    gpio2=robo_reset
    sb/1/rssi_delta_5gml_c1=-4,0,-5,0,-5,0
    sb/1/sb20in80and160lr5ghpo=0
    sb/1/rssi_delta_2g_c0=4,5,4,5
    sb/1/rssi_delta_2g_c1=2,3,2,3
    gpio6=usbport2
    sb/1/rpcal5gb0=36
    sb/1/rpcal5gb1=124
    gpio8=usbport1
    sb/1/rpcal5gb2=227
    gpio9=wps_button
    sb/1/rpcal5gb3=22
    sb/1/sb40and80hr5gmpo=0
    sb/1/tempthresh=120
    sb/1/rpcal2g=80
    sromrev=11
    boardtype=0x0782
    et1macaddr=AA:BB:CC:DD:EE:01
    sb/1/mcsbw405gmpo=0xfedb9752
    lan_netmask=255.255.255.0
    sb/1/sb20in80and160hr5glpo=0
    sb/1/regrev=0
    0:rxchain=3
    sb/1/aga0=0
    sb/1/aga1=0
    sb/1/aga2=0
    sb/1/sb20in80and160hr5ghpo=0
    sb/1/rxgains5ghelnagaina0=4
    0:tempthresh=120
    sb/1/rxgains5ghelnagaina1=4
    sb/1/rxgains5gmtrelnabypa0=1
    sb/1/rxgains5gmtrelnabypa1=1
    sb/1/sb40and80lr5glpo=0
    vlan2hwname=et1
    sb/1/pdoffset80ma0=0
    sb/1/mcsbw805glpo=0xfeda9742
    sb/1/pdoffset80ma1=0x1111
    xtalfreq=40000
    sb/1/sb40and80lr5ghpo=0
    miniweb_ipaddr=192.168.0.1
    sb/1/rxgains5ghtrelnabypa0=1
    sb/1/rxgains5ghtrelnabypa1=1
    nvram_space=65536
    boardflags2=0x0
    boardflags3=0x40000182
    sb/1/aa2g=0
    sb/1/txchain=3
    sb/1/mcsbw805ghpo=0xfeda9742
    sb/1/dot11agduphrpo=0
    0:regrev=0
    0:pa2gw0a0=0xfe71
    0:pa2gw0a1=0xfe67
    wait_time=3
    sb/1/rssi_delta_5gmu_c0=-4,0,-5,0,-5,0
    0:leddc=0xFFFF
    sb/1/rssi_delta_5gmu_c1=-4,0,-5,0,-5,0
    0:triso2g=0x4
    sb/1/rpcal_phase=127
    0:sromrev=8
    sb/1/sb40and80hr5glpo=0
    sb/1/sb20in40lrpo=0
    sb/1/boardflags2=0x0
    sb/1/mcslr5gmpo=0
    sb/1/boardflags3=0x40000182
    sb/1/swctrlmap_2g=0x00000808,0x30300000,0x10100000,0x000000,0x3ff
    sb/1/papdcap5g=0
    sb/1/pdoffset40ma0=0x2333
    sb/1/pdoffset40ma1=0x4444
    sb/1/mcsbw405glpo=0xfedb9752
    sb/1/swctrlmapext_5g=0x00000000,0x00000000,0x00000000,0x000000,0x000
    sb/1/sb40and80hr5ghpo=0
    0:stbcpo=0x0
    0:itt2ga0=0x20
    0:ccode=US
    0:itt2ga1=0x20
    sb/1/mcsbw405ghpo=0xfedb9752
    sb/1/rssi_delta_5gl_c0=-3,0,-5,0,-5,0
    sb/1/rssi_delta_5gl_c1=-3,0,-5,0,-5,0
    sb/1/femctrl=15
    sb/1/boardflags=0x10000110
    0:boardvendor=0x14e4
    sb/1/leddc=0xFFFF
    0:tssipos2g=1
    sb/1/tempoffset=0
    0:devid=0x43a9
    clkfreq=900,533
    lan_ipaddr=192.168.1.1
    vlan1hwname=et0
    0:extpagain2g=2
    0:maxp2ga0=0x64
    0:temps_hysteresis=5
    sdram_config=0x01c7
    0:maxp2ga1=0x64
    sb/1/fdss_level_2g=0,0
    vlan1ports=1 2 3 4 8*
    sb/1/temps_hysteresis=5
    sb/1/pa5ga0=0xff12,0x1af1,0xfca1,-231,6773,-837,-232,6692,-828,0xff1d,0x1d12,0xfc70
    sb/1/pa5ga1=0xff22,0x1e5d,0xfc4f,-231,6720,-829,-234,6623,-820,0xff1b,0x1d97,0xfc5d
    sb/1/macaddr=AA:BB:CC:DD:EE:02
    sb/1/mcsbw1605gmpo=0
    0:boardflags=0x00000200
    sb/1/olpc_thresh2g=7
    sb/1/ccode=US
    0:opo=0x0
    sb/1/maxp5ga0=0x5e,0x5e,0x5e,0x5e
    0:tempoffset=0
    boardflags=0x10000110
    sb/1/maxp5ga1=0x5e,0x5e,0x5e,0x5e
    wandevs=et1
    0:antswitch=0
    sdram_refresh=0x0000
    sb/1/paparambwver=3
    0:bwduppo=0x0
    0:txchain=3
    0:phycal_tempdelta=0
    0:ofdm2gpo=0xba754222
    sdram_ncdl=0x00000000
    sb/1/phycal_tempdelta=15
    sb/1/mcslr5glpo=0
    sb/1/subband5gver=4
    sb/1/aa5g=3
    sb/1/devid=0x43C8
    0:mcs2gpo0=0x5422
    0:boardflags2=0x00008800
    0:mcs2gpo1=0xeba7
    sb/1/tworangetssi5g=0
    0:mcs2gpo2=0x5422
    0:mcs2gpo3=0xeba7
    0:mcs2gpo4=0x7533
    0:tri2g=0x0
    0:mcs2gpo5=0xfca8
    gpio10=wps_led
    sb/1/mcslr5ghpo=0
    0:mcs2gpo6=0x7533
    0:mcs2gpo7=0xfca8
    sb/1/sb20in40hrpo=0
    sb/1/ledbh11=11
    0:cddpo=0x0
    sb/1/mcsbw205gmpo=0xfecb9752
    0:rssismc2g=0x0
    et0phyaddr=30
    sb/1/epagain5g=0
    sb/1/rxgains5gtrelnabypa0=1
    sb/1/rxgains5gtrisoa0=5
    sb/1/rxgains5gtrelnabypa1=1
    sb/1/rxgains5gtrisoa1=5
    sb/1/pa5gbw4080a0=0xff14,0x1aff,0xfca4,-235,6594,-817,-236,6557,-814,0xff1e,0x1ca5,0xfc82
    0:rssisav2g=0x0
    sb/1/pa5gbw4080a1=0xff21,0x1dcf,0xfc62,-235,6570,-814,-235,6565,-813,0xff19,0x1c23,0xfc8a
    landevs=vlan1 wl0 wl1
    sb/1/swctrlmap_5g=0x00000101,0x06060000,0x02020000,0x000000,0x3ff
    sb/1/sb20in80and160lr5gmpo=0
    sb/1/rssi_delta_5gh_c0=-4,0,-6,0,-5,0
    sb/1/rssi_delta_5gh_c1=-4,0,-6,0,-5,0
    sb/1/tssiposslope5g=1
    sdram_init=0x0000
    sb/1/rxgains5gmtrisoa0=5
    0:pa2gw2a0=0xfa27
    0:bw40po=0x0
    sb/1/AvVmid_c0=2,135,2,135,2,135,2,135,2,135
    sb/1/rxgains5gmtrisoa1=5
    0:pa2gw2a1=0xfa14
    sb/1/AvVmid_c1=2,145,2,145,2,145,2,145,2,145
    sb/1/rxgains5gelnagaina0=4
    sb/1/rxgains5gelnagaina1=4
    fr_gpio=7
    sb/1/pdoffset5gsubbanda0=0x0000
    sb/1/pdoffset5gsubbanda1=0x0000
    0:xtalfreq=20000
    sb/1/ledbh0=11
    sb/1/mcsbw1605glpo=0
    sb/1/ledbh1=11
    sb/1/ledbh2=11
    sb/1/ledbh3=11
    sb/1/rxchain=3
    0:bxa2g=0x0
    et1phyaddr=30
    miniweb_netmask=255.255.255.0
    boardnum=001
    sb/1/mcsbw1605ghpo=0
    sb/1/antswitch=0
    0:temps_period=5
    0:macaddr=AA:BB:CC:DD:EE:03
    bootflags=0
    0:antswctl2g=0
    sb/1/sb20in80and160hr5gmpo=0
    sb/1/fdss_level_5g=0,0
    0:ag0=0x2
    size: 5213 bytes (60323 left)
    *** command status = 0

One last observation. If you ask `show devices` to the CFE bootloader,
you will notice `flash0` prefixed devices and `flash1`. As far as I
can tell, they seem to point to the exact same region of the flash
(just 2 different names). See:

    CFE> show devices
    Device Name          Description
    -------------------  ---------------------------------------------------------
    uart0                NS16550 UART at 0x18000300
    flash0               ST Compatible Serial flash size 16384KB
    flash0.boot          ST Compatible Serial flash offset 00000000 size 256KB
    flash0.boot2         ST Compatible Serial flash offset 00040000 size 256KB
    flash0.trx           ST Compatible Serial flash offset 00080000 size 1KB
    flash0.os            ST Compatible Serial flash offset 0008001C size 15808KB
    flash0.nvram         ST Compatible Serial flash offset 00FF0000 size 64KB
    flash1.boot          ST Compatible Serial flash offset 00000000 size 256KB
    flash1.boot2         ST Compatible Serial flash offset 00040000 size 256KB
    flash1.trx           ST Compatible Serial flash offset 00080000 size 15808KB
    flash1.nvram         ST Compatible Serial flash offset 00FF0000 size 64KB
    eth0                 Broadcom BCM47XX 10/100/1000 Mbps Ethernet Controller
    *** command status = 0
    CFE> help fdump

      SUMMARY

         Dump content on flash device in hex format.

      USAGE

         fdump [options] [flashdevice]

         If flashdevice is not specified, it will be set to flash0 by default.

      OPTIONS

         -offset=*    Begin dumping at this offset in the flash device
         -size=*      Dumping size.

    *** command status = 0
    CFE> fdump -offset=1024 -size=128 flash0.trx
    00000400  26 9f b4 20 93 4b 11 48  81 25 33 35 c7 f6 cd 2b  |&....K.H.%35...+|
    00000410  78 a9 a5 c1 28 34 0a e5  28 e5 b6 95 da eb 65 ce  |x...(4..(.....e.|
    00000420  2c 32 6e ea 26 f9 84 c0  f9 31 0e c5 68 b5 46 5b  |,2n.&....1..h.F[|
    00000430  47 13 da ca fc 6e 60 08  00 fd ca e5 5a 6e 05 72  |G....n`.....Zn.r|
    00000440  fb 37 be 73 b4 79 67 04  f7 50 e4 39 2a 99 7d 69  |.7.s.yg..P.9*.}i|
    00000450  11 04 2d 21 81 06 ea fb  3c e8 cd 55 f3 b0 32 0e  |..-!....<..U..2.|
    00000460  db 28 41 c8 55 cc 33 3d  24 d9 0b e0 01 d0 66 d1  |.(A.U.3=$.....f.|
    00000470  d8 7b 6a ee aa a5 24 e8  48 aa 0c 57 45 4d 1b 8a  |.{j...$.H..WEM..|
    *** command status = 0
    CFE> fdump -offset=1024 -size=128 flash1.trx
    00000400  26 9f b4 20 93 4b 11 48  81 25 33 35 c7 f6 cd 2b  |&....K.H.%35...+|
    00000410  78 a9 a5 c1 28 34 0a e5  28 e5 b6 95 da eb 65 ce  |x...(4..(.....e.|
    00000420  2c 32 6e ea 26 f9 84 c0  f9 31 0e c5 68 b5 46 5b  |,2n.&....1..h.F[|
    00000430  47 13 da ca fc 6e 60 08  00 fd ca e5 5a 6e 05 72  |G....n`.....Zn.r|
    00000440  fb 37 be 73 b4 79 67 04  f7 50 e4 39 2a 99 7d 69  |.7.s.yg..P.9*.}i|
    00000450  11 04 2d 21 81 06 ea fb  3c e8 cd 55 f3 b0 32 0e  |..-!....<..U..2.|
    00000460  db 28 41 c8 55 cc 33 3d  24 d9 0b e0 01 d0 66 d1  |.(A.U.3=$.....f.|
    00000470  d8 7b 6a ee aa a5 24 e8  48 aa 0c 57 45 4d 1b 8a  |.{j...$.H..WEM..|
    *** command status = 0
    CFE>


# Final word

Bricking this tp-link Archer C1200 EU V2 router was actually good fun
(well I'm glad it was cheap). If by chance someone happens to be able
to dump their factory firmware or knows how to extract the trx binary
from the firmware available on tp-link official page or has any other
idea, I'd be happy to try to unblock my router.

Note that all the dumps are raw copies from the router's console,
except the MAC addresses that have been masked for privacy reason ; )
Who knows, maybe some day I'll be able to unbrick the device !



[1]: https://openwrt.org/toh/start
[2]: https://forum.openwrt.org/t/build-for-tp-link-archer-c1200-ac1200/2547
[3]: https://forum.openwrt.org/t/unable-to-install-at-tp-link-archer-c1200-v2/49211
[4]: https://openwrt.org/toh/tp-link/tp-link_archer_c1200_2
[5]: https://wikidevi.wi-cat.ru/TP-LINK_Archer_C1200_v2.x
[6]: https://wikidevi.wi-cat.ru/TP-LINK_Archer_C1200_v1.x
[7]: https://wikidevi.wi-cat.ru/Tenda_AC9
[8]: https://openwrt.org/toh/hwdata/tenda/tenda_ac9
[9]: https://www.tp-link.com/en/support/download/archer-c1200/v2/#Firmware
[10]: https://www.tp-link.com/en/support/gpl-code/
[11]: https://openwrt.org/toh/tp-link/tp-link_archer_c1200_2#opening_the_case
[12]: https://openwrt.org/docs/techref/hardware/port.serial
[13]: https://openwrt.org/docs/techref/bootloader/cfe
[14]: https://www.golinuxhub.com/2016/09/how-to-configure-tftp-server-in-linux/
[15]: https://drive.google.com/drive/folders/15XtmQpSJUCN3zmvnZBdqsOpcW6iYSxSk
[16]: https://forum.openwrt.org/t/build-for-tp-link-archer-c1200-ac1200/2547/17
[17]: http://www.florentflament.com/blog/openwrt-on-linksys-wrt54gl.html
