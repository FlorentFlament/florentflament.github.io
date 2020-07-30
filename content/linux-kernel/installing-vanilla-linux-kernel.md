Title: Installing a Vanilla Linux Kernel on Fedora
Date: 2017-11-19
Tags: Linux, Kernel

Updated on 2017-12-28

Installing a Vanilla Linux Kernel on Fedora is quite simple (once one
knows how to do it..)

## Configuring & Building Linux

One can start by cloning Torvalds' Linux repository to fetch the
latest master (or we could fetch the latest stable release) :

```text
$ git clone https://github.com/torvalds/linux.git
$ cd linux
```

I like setting `EXTRAVERSION` in the `Makefile` to be able to identify
which kernel I am testing. That can be done by opening the `Makefile`
with one's favorite editor or replacing the `EXTRAVERSION` line with
`sed`:

```text
$ sed -i "s/^EXTRAVERSION = .*$/EXTRAVERSION = name_of_my_version/" Makefile
```

Now we need to generate the `.config` Linux kernel configuration
file. We can start from the default one:

```text
$ make defconfig
```

Or we can reuse configuration files from the local installation with:

```text
$ make olddefconfig
```

Note that `make help` provides the list of possible `make` commands.

For computers using (U)EFI, one may need to update the `.config` file
to support `EFI handover`. This is done by setting `EFI stub support`
when configuring the kernel (for instance with `make menuconfig`).

```text
Processor type and features  --->
    [*] EFI runtime service support
    [*]   EFI stub support
```

Sources: [stackoverflow][1] and [gentoo linux wiki][2].

Without that option activated, I ended up having the following error
message when trying to boot my new kernel:

```text
error: kernel doesn't support EFI handover
```

This option isn't required when building a kernel for a virtual
machine.

In order to compile the kernel, (at least) the following dependencies
are required:

* git
* gcc
* ncurses-devel
* elfutils-libelf-devel
* openssl-devel
* perl-interpreter
* rpm-build (if building rpm packages)

Then we can build the kernel as simply as that:

```text
$ make
```

The straight forward approach to install the Kernel, if it has been
built on the target machine is:

```text
$ sudo make install
$ sudo make modules_install
```

We can now reboot on the newly built Kernel.


## Building RPM package

We can even make RPMs to install the new kernel on any RPM based
machine:

```text
$ make binrpm-pkg
```

The packages are available in the `~/rpmbuild/RPMS/x86_64` directory:

```text
$ ls ~/rpmbuild/RPMS/x86_64/
kernel-4.14.0efistub+-3.x86_64.rpm  kernel-headers-4.14.0efistub+-3.x86_64.rpm
$
```

The newly built kernel can be installed with the standard rpm install
command:

```text
$ cd ~/rpmbuild/RPMS/x86_64/
$ sudo rpm -i kernel-4.14.0efistub+-3.x86_64.rpm
```

That's it, when rebooting, the new kernel is available in the grub
menu (together with the previously installed kernels) .

```text
$ dmesg | head -3
[    0.000000] microcode: microcode updated early to revision 0x1c, date = 2015-02-26
[    0.000000] Linux version 4.14.0efistub+ (florent@amn) (gcc version 7.2.1 20170915 (Red Hat 7.2.1-2) (GCC)) #3 SMP Sun Nov 19 22:52:23 CET 2017
[    0.000000] Command line: BOOT_IMAGE=/vmlinuz-4.14.0efistub+ root=/dev/mapper/fedora-root ro rd.lvm.lv=fedora/root rd.lvm.lv=fedora/swap rhgb quiet LANG=en_US.UTF-8
```

Tested with Linux 4.14.0 hash ed30b147e1f6e396e70a52dbb6c7d66befedd786

[1]: https://stackoverflow.com/questions/40344484/cant-load-self-compiled-linux-kernel#40344635
[2]: https://wiki.gentoo.org/wiki/EFI_stub_kernel#Configuration
