Title: Ubuntu VM auto installation
Date: 2013-11-30
Tags: Ubuntu, KVM, libvirt

Installing a fresh Ubuntu, or any other Linux distribution, on a new
system is quite forward. The installer asks you a few question about
your country, keyboard, network, ... . Then it installs all the
required packages on the system, and makes it bootable.

However, when playing with VMs (Virtual Machines), you may wish to
install your distribution many times ; in which case the installation
process (with the questions to answer) becomes somehow tedious.

There are several approaches to deal with this issue. This post will
deal with the automatic installation of an Ubuntu 12.04 Precise, by
using [Debian preseeding mecanism][0] with virt-install (virtinst
package).

An alternative approach would be to do a manual full installation,
then making several copies of the installed image. Each copy will be
customized to be used for a new VM. These two methods have their pros
and cons, and can be used together.

A running system with libvirt and virtinst packages is required. The
key of a preseed automatic installation is to have the good
`preseed.cfg` file. This file will provide the Debian installer (also
used by Ubuntu) with all the information it requires to install and
configure the system, without the need to ask any question.

Preseed file
------------

Here's my generic [preseed.cfg][1] file. It is a mix of [Debian's
example-preseed][2] file and parameters gathered using Debian's
suggested method after a manual installation:

    ::::bash
    debconf-get-selections --installer > file
    debconf-get-selections >> file

The password for the `vmuser` user has to be set, by changing the
current CRACKMECRACKM encrypted password to a valid one. A valid
crypted password can be generated with the following command:

    ::::bash
    python -c 'from crypt import crypt; print crypt("MYPASSWORD", "SALT")'

Some other parameters may be customized, like locale, user name, ...

Empty image creation
--------------------

Then we need to create an empty disk that will be used to install the
system. A 5GB disk should be enough for a minimal Ubuntu installation
(depending on one's requirements).

    ::::bash
    qemu-img create vm.qcow2 5G

virt-install
------------

Installing Ubuntu Precise on a VM can now be launched with the
following unique command (to be customized):

    ::::bash
    virt-install \
	--name vm \
	--ram 128 \
	--location http://fr.archive.ubuntu.com/ubuntu/dists/precise-proposed/main/installer-i386/ \
	--disk vm.qcow2,bus=virtio \
	--graphics vnc,keymap=local,listen=0.0.0.0,port=5900 \
	--network user,model=virtion \
	--initrd-inject preseed.cfg

Note that the `precise-proposed` Ubuntu distribution is used instead
of the standard `precise`. It addresses a [bug that makes the
installation freeze for 10+ minutes][3] during the components download
phase.

After some 30 minutes the system installation should be completed.

[0]: http://www.debian.org/releases/stable/i386/apbs02.html.en
[1]: {filename}/static/preseed.cfg
[2]: http://www.debian.org/releases/squeeze/example-preseed.txt
[3]: https://bugs.launchpad.net/ubuntu/+source/net-retriever/+bug/1067934