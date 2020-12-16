Title: Macmini2,1 Linux dual boot
Date: 2013-11-03
Modified: 2020-12-16
Tags: Apple, Linux

While online resources provide documentation about [how to install
Linux on a Mac Mini][0], this guide focuses on the Apple Macmini2,1
and its peculiarities. Please refer to [these tables][1] to properly
identify your hardware.

2020-12-16 update
-----------------

I wrote an update about [how to install a GNU/Linux OS on the Macmini
using PXE][8].

About Macmini2,1
----------------

Apple provides [firmware updates][2] for most of its hardware. Most
Mac Minis do have an EFI Boot ROM update available there, but
Macmini2,1 doesn't. The good news is that what is stated on this page
is true, Macmini2,1 doesn't need any firmware update to be able to
boot non MacOS OSes.

Macmini2,1 is powered by an Intel Core 2 Duo, which is a [64-bit
processor][3]. However, when trying to install a 64 bits Linux
distribution from a CDROM (by pressing the C key during boot sequence,
right after the startup sound), the installer hangs up on a text
screen, while seemingly starting to display a grub menu (I experienced
this with amd64 ISOs of Debian Wheezy, Debian Jessie and Xubuntu
Precise). With i386 images of these same distributions, the installer
starts in graphic mode without issue.

However, I could find a way to install a 64 bits OS on the machine, by
booting the machine on a [CDROM launching a PXE installation][7] over
the network. By using this mechanism, I succeeded in installing an
amd64 Ubuntu Precise Linux distribution. Note that I've been
unsuccessful in starting the computer from a USB key, or directly over
PXE.

Setting dual boot
-----------------

On original Max OS X installations, the whole hard disk is occupied by
a unique partition. Therefore, we need to free some space for our new
OS, by resizing the partition. The `diskutil` command allows us to do
that. In a shell, we have to launch the following command (where 20G
means that we want to let 20 Gigabytes to our OS X partition. One may
split the disk capacity according to its requirements):

    ::::bash
    $ sudo diskutil resizeVolume disk0s2 20G

Then we have to install [rEFit][6] on the computer. It will allow us
to choose the partition / device to boot, and to resynchronize GPT /
MBR tables as will be covered in a next step.

We can now insert the Linux distribution installation CD into our Mac
(I downloaded the last [Debian stable i386 netinst ISO][4] and burned
it to a CD-RW with the Mac Mini's CD burner). When restarting the
computer, rEFit will allow us to boot on the CD.

During the installation process, we have to create new partition(s)
(for convenience, I chose a distinct / and /home partitions). When
asked to install grub, choose `/dev/sda4` (the partition that will be
mounted as /).

Once the Linux installation is finished, reboot and use rEFit
`Partition Tool` to resync GPT / MBR tables. Then boot back to MacOS
and use its `bless` tool to make the new OS bootable:

    ::::bash
    $ sudo bless --device /dev/disk0s4 -setBoot

Eventually, we can customize the rEFit configuration file
`/efi/refit/refit.conf` to make the boot sequence more convenient. The
rEFit menu timeout can be set with the `timeout` option. The option
`default_selection` (at the end of the file) allows us to choose the
default OS to boot.

That's it ! Restart, rEFit allows us to choose between booting Mac OS
X and Linux.

[0]: https://wiki.debian.org/MacMiniIntel
[1]: http://en.wikipedia.org/wiki/Macmini#Specifications
[2]: http://support.apple.com/kb/HT1237
[3]: http://en.wikipedia.org/wiki/Core_2_duo#64-bit_Core_microarchitecture_based
[4]: http://www.debian.org/distrib/netinst
[5]: https://discussions.apple.com/message/17645953#17645953
[6]: http://refit.sourceforge.net/
[7]: http://rom-o-matic.net/gpxe/gpxe-git/gpxe.git/contrib/rom-o-matic/
[8]: {filename}macmini21-pxe-install.md
