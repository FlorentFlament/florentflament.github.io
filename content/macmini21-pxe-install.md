Title: Macmini 2,1 PXE install
Date: 2020-12-15
Tags: Macmini, Linux, Ubuntu, PXE

I recently bought 3 GB of used DDR2 SDRAM (for 8 bucks) for my 2009
[Macmini 2,1][2], to use it as a [ceph][18] monitor running
GNU/Linux. The machine's CPU is a 64 bits core 2 duo, which is more
than enough for my use case. Here's a [video showing how to change the
RAM][1].

That said, it has become more and more difficult to find a
distribution that can be installed on the machine. There's an
[interesting post][8] that provides us with some hints about
why. Here's briefly what it says:

* Booting via USB doesn't work;
* Mac mini does not handle EFI bootable disks gracefully, only ISOs
  without EFI can boot (which means that most recent distributions'
  installation CDs can't boot).

If we can't boot on a USB device and can't run a GNU/Linux
installation CD on the Macmini then how can we install our favorite
distribution ? Can we use [PXE][9] (Preboot Execution Environment), to
start an installation over the network (as I talked a bit in a [post 7
years ago][19]) ? The Macmini doesn't allow to boot over the network
by default, but it is possible to have it boot on a CDROM, which would
then boot an image downloaded from a TFTP server (either to install an
operating system on the local disk, or to boot an OS directly over the
network).

gPXE
----

The [gPXE Etherboot project][10] is exactly about that. The [source
code][11] allows building a floppy disk image, a usb key image and a
cdrom image that allow booting over PXE (there's also an official
[github mirror][12]). Well, it used to compile 10 years ago, but it
doesn't on current 64 bits operating systems with currently supported
versions of gcc. Pre-built images were available on the
rom-o-matic.net web site, which has been down for a long time.

I recently [forked the gPXE repository][13], to which I added a
Vagrantfile that allows spawning a 32 bits virtual machine running the
Ubuntu Precise GNU/Linux distribution with all the tools required to
build gPXE. I also built and published the following [gPXE v1.0.1
images][14] with every network adapter driver available:

* The floppy disk image: [gpxe.dsk][15]
* Thu USB key image: [gpxe.usb][16]
* The CDROM ISO image: [gpxe.iso][17]

By booting the Macmini on the gPXE ISO image burnt on a CDROM, we can
basically install any GNU/Linux distribution from a DHCP/TFTP server.

Installing a DHCP/TFTP server
-----------------------------

I adapted these [instructions to setup a tftp server][20], so that I
could have it provided by dnsmasq (as I already use it). This can be
achieved by populating the `/tftp` directory (or any other directory),
and configuring `dnsmasq` to serve these files via the TFTP protocol.

First, we need to populate the `/tftp` directory with the following
startup files from the `pxelinux` package (on Ubuntu 20.04):

  * `/usr/lib/PXELINUX/pxelinux.0`
  * `/usr/lib/syslinux/modules/bios/ldlinux.c32`
  * `/usr/lib/syslinux/modules/bios/libcom32.c32`
  * `/usr/lib/syslinux/modules/bios/libutil.c32`
  * `/usr/lib/syslinux/modules/bios/vesamenu.c32`

Then, we need to add a `vmlinuz` Linux kernel and an `initrd` RAM disk
image to allow PXE clients to bootstrap a GNU/Linux operating system,
which may then start the installation of an OS on a local disk. These
files can be extracted from a GNU/Linux distribution ISO image (for
instance in the `/casper` directory of the
`ubuntu-20.04-live-server-amd64.iso` image)

We also need a pxelinux menu configuration file
`/tftp/pxelinux.cfg/default`, which should look like this:

    DEFAULT vesamenu.c32
    TIMEOUT 600
    ONTIMEOUT focal-live-install
    PROMPT 0
    NOESCAPE 1
    LABEL focal-live-install
            MENU DEFAULT
            MENU label Ubuntu Focal install
            KERNEL vmlinuz
            INITRD initrd
            APPEND root=/dev/ram0 ramdisk_size=1500000 ip=dhcp url=<URL_OF>/ubuntu-20.04.1-live-server-amd64.iso

Eventually, `dnsmasq` needs to be instructed to start a TFTP service,
exposing the files from the `/tftp` directory, and telling devices
booting over PXE to download and run the file `pxelinux.0`. This can
be achieved by adding the following options to `dnsmasq` configuration
file:

    enable-tftp
    tftp-root=/tftp
    dhcp-boot=pxelinux.0

Ubuntu Focal installation
-------------------------

At this point, we should be able to have the Macmini boot on the gPXE
CDROM, by holding the F2 key while the machine starts (after the Mac
characteristic startup sound). It should then load the boot image from
the TFTP server, then download the installation ISO image and start
it.

By default the installer will create a GPT partition table. But this
will not work with the Macini 2,1. The machine will end up with a
blinking folder at startup instead of booting the Operating
System. Therefore, we need to manually create a DOS partition
table. To do that, we can switch to a new tty by pressing Alt-F2, when
we see the Ubuntu installer interactive menu, and launch `fdisk`
(Beware! the following commands will wipe out any data on the disk):

    $ sudo fdisk /dev/sda

The the following `fdisk` commands will destroy any data on the disk,
and create a DOS partition table with a single bootable partition
using the whole disk:

* 'o' to create a new empty DOS partition table
* 'n' to add a new partition table (the size of the whole disk)
* 'a' to make it bootable
* 'w' to write the partition table and exit

Then we can start the installation process, by answering to the
questions asked as usual. At the "Guided storage configuration" step,
we need to select the "Custom storage layout" option, then have the
only partition created formatted as ext4 and mounted as '/'.

Once the installation is over, we can reboot the machine. By holding
the F12 key during the boot sequence, it will eject the CDROM and boot
the locally installed GNU/Linux operating system.

[1]: https://www.youtube.com/watch?v=PTKKWTau-Pc
[2]: https://en.wikipedia.org/wiki/Mac_Mini#Specifications
[8]: https://help.ubuntu.com/community/Mac_mini2-1
[9]: https://en.wikipedia.org/wiki/Preboot_Execution_Environment
[10]: http://etherboot.org/wiki/
[11]: http://git.etherboot.org/gpxe.git/
[12]: https://github.com/etherboot/gpxe
[13]: https://github.com/FlorentFlament/gpxe
[14]: https://github.com/FlorentFlament/gpxe/releases/tag/v1.0.1
[15]: https://github.com/FlorentFlament/gpxe/releases/download/v1.0.1/gpxe.dsk
[16]: https://github.com/FlorentFlament/gpxe/releases/download/v1.0.1/gpxe.usb
[17]: https://github.com/FlorentFlament/gpxe/releases/download/v1.0.1/gpxe.iso
[18]: https://ceph.io/
[19]: http://www.florentflament.com/blog/macmini21-linux-dual-boot.html
[20]: https://askubuntu.com/questions/1238070/deploy-ubuntu-20-04-on-bare-metal-or-virtualbox-vm-by-pxelinux-cloud-init-doesn/1240068#1240068
