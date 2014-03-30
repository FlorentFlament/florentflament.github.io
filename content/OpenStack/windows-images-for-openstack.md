Title: Windows Images for OpenStack
Date: 2014-03-30 19:15
Tags: OpenStack, Microsft, Windows

This note summarizes articles from other places about Microsoft
Windows images for OpenStack creation, along with some first hand
experience. The whole process of creating Windows 2008 and Windows
2012 images fully usable on OpenStack instances is described there.

Prerequisite
============

To achieve the creation of a qcow2 Windows image for OpenStack, we
need the following ISO images:

* An ISO image of the installation DVD for all OSes that we wish to
  use in OpenStack. These ISOs can usually be downloaded from a
  company's account on Microsoft website, once the appropriate
  contract has been signed. For testing purpose, [Windows Server 2012
  Evaluation ISO][2] can be downloaded on Microsoft website.

* The latest [VirtIO drivers for Windows][3]. These are optimized
  drivers to run Windows OSes with KVM virtualized hard disk
  controller and network devices.

Base image creation
===================

The first step to build a Microsoft Windows image is to install the OS
in a VM as we would have done on a bare metal computer. [Gridcentric's
article about Windows image creation][1] describes this procedure in
details.

The steps to follow are:

* Create an empty qcow2 image (this will be the disk on which we'll
  install our OS). I typically use a 9 GB image for Windows 2008, and
  a 17 GB for Windows 2012 (although I think it should work with a 11
  or 12 GB image). Example:

        ::::bash
        $ qemu-img create -f qcow2 Windows-Server-2008-R2.qcow2 9G

* Next step is to launch Windows' installation in a (KVM) virtual
  machine. The following command is an example for that:

        ::::bash
        $ kvm \
            -m 2048 \
            -cdrom <WINDOWS_INSTALLER_ISO> \
            -drive file=Windows-Server-2008-R2.qcow2,if=virtio \
            -drive file=<VIRTIO_DRIVERS_ISO>,index=3,media=cdrom \
            -net nic,model=virtio \
            -net user \
            -nographic \
            -vnc :9 \
            -k fr \
            -usbdevice tablet

* The following step consists in connecting to the display of the VM
  launched previously through VNC, in order to manually pursue the
  installation. This can be done with the following command:
 
        ::::bash
        $ xvncviewer <IP_OF_HYPERVISOR>:9

* During the installation, Windows will ask for the Hard Disk
  controller driver. We have to select the VirtIO driver, which is
  located on the VirtIO CDROM (WIN7 directory for Windows 2008,
  and WIN8 directory for Windows 2012).

* Once the basic Windows installation is done, we have to set the
  appropriate Network device driver in the Windows Devices
  Manager. The Network device VirtIO driver is available in the same
  directory than the Hard Disk controller driver specified in the
  previous step.

* Since VMs will be managed by RDP, we have to activate the
  service. This is done by navigating through the following menu:
  Computer (right-lick) -> Properties -> remote tab, and selecting the
  following option: allow connections from computers running any
  version of Remote Desktop.

* An additional step consisting in opening the appropriate Firewall
  ports is required on Windows 2012: Network (right-click) ->
  Properties -> Windows Firewall -> Advanced Settings -> Inbound
  rules. Then enable: Remote Desktop - Shadow, Remote Desktop - User
  Mode TCP, Remote Desktop - User Mode UDP.

Customizing image for OpenStack
===============================

The previous steps allowed us to have Windows fully installed in a KVM
virtual machine. The last steps consist in installing [Cloud-Init for
Windows][4], a Windows implementation of the Linux based
[Cloud-Init][5] mechanism. This set of scripts transforms a legacy OS
image into a ready for OpenStack image. At instantiation of a VM,
Cloud-Init fetches from a meta-data server, data such as ssh public
key and hostname that allows the instance to become unique. Cloud-Init
base is Open source, and Cloudbase provides an [installer][6] on its
blog. We'll install Cloud-Init by injecting the installer that we just
downloaded. To to that, we have to follow these steps:

* Shutdown Windows

* Mount the qcow2 image on the hypervisor filesystem, then copy the
  installer on Windows' administrator desktop, with something like:

        ::::bash
        $ sudo qemu-nbd -c /dev/nbd2 Windows-Server-2008-R2.qcow2
        $ sudo mount /dev/nbd2p2 mnt/
        $ cp <INSTALLER> <ADMINISTRATOR_DESKTOP_ON_WINDOWS>
        $ sudo umount mnt/
        $ sudo qemu-nbd -d /dev/nbd2

* Restart Windows in KVM with the same command that we used to install
  Windows in the first place:

        ::::bash
        $ kvm \
            -m 2048 \
            -cdrom <WINDOWS_INSTALLER_ISO> \
            -drive file=Windows-Server-2008-R2.qcow2,if=virtio \
            -drive file=<VIRTIO_DRIVERS_ISO>,index=3,media=cdrom \
            -net nic,model=virtio \
            -net user \
            -nographic \
            -vnc :9 \
            -k fr \
            -usbdevice tablet

* Then connect again with xvncviewer:

        ::::bash
        $ xvncviewer <IP_OF_HYPERVISOR>:9

* This time, we have to launch the CloudbaseInitSetup_Beta.msi
  installer, and follow the instructions as described on [Cloudbase
  blog][4]. At the end of the installation, we have to check the "run
  sysprep" option, but not the "shutdown" one. Sysprep is the tool
  provided by Microsoft to make a VM unique (generates a unique OS ID
  to be used for some Microsoft services), once it's instantiated.

* Once the installation is done, we can clean any temporary files
  created, then shutdown the system. The image is ready to be uploaded
  in OpenStack Glance:

        ::::bash
        $ glance add name=<OPENSTACK_IMAGE_NAME> is_public=true \
            container_format=bare disk_format=qcow2 < <IMAGE_FILENAME>

Connecting to a Windows VM
==========================

The usual mechanism used in OpenStack to connect to VMs (running
Linux) is ssh. A public key specified by the user launching the VM is
set in the default user's `authorized_keys` file. This allows the user
to connect to the VM by using the corresponding private key.

However, it is not currently possible to connect to a Windows VM with
ssh (there is some [work done in this direction][7] that I've not
tested yet). Cloud-Init base creates an `Admin` user, with either:

* a password specified by the user on the command line. Note that the
  password must respect Windows password strength constraints (upper
  and lower case characters, as well as numbers). If not it will be
  silently ignored. For instance:

        ::::bash
        $ nova boot --key-name <KEYPAIR_NAME> --image <IMAGE_ID> \
            --flavor <FLAVOR_ID> --nic net-id=<NET_ID> \
            --meta admin_pass=<ADMIN_PASSWORD> <VM_NAME>

* a password automatically generated during VM instantiation, and
  encrypted with the ssh public key provided when launching the
  VM. Such password can be retrieved and decrypted with the
  corresponding private ssh key, by using the following command (note
  that the private key is used locally):

        ::::bash
        $ nova get-password <VM_NAME_OR_ID> <SSH_PRIVATE_KEY>

Note that to connect to a Windows VM from Linux, prefer using
`xfreerdp` instead of `rdesktop`. The pointer is bogus when connecting
to a windows 2012 VM using `rdesktop`.

[1]: http://blog.gridcentric.com/bid/297627/Creating-a-Windows-Image-on-OpenStack
[2]: http://technet.microsoft.com/en-us/evalcenter/hh670538.aspx
[3]: http://www.linux-kvm.org/page/WindowsGuestDrivers/Download_Drivers
[4]: http://www.cloudbase.it/cloud-init-for-windows-instances/
[5]: http://cloudinit.readthedocs.org/en/latest/
[6]: https://www.cloudbase.it/downloads/CloudbaseInitSetup_Beta.msi
[7]: http://www.cloudbase.it/windows-without-passwords-in-openstack/