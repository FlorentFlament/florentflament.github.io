Title: Ceph and Cinder multi-backend
Date: 2013-11-17
Tags: Ceph, OpenStack, Cinder

[Ceph's documentation][0] is quite extensive. However, when trying and
[installing Ceph on a running Openstack platform][1], I met two main
issues: How to deal with a multi-backend setup? And how to deal with
several nova-compute nodes?  This note will focus on the steps that I
followed in order to have Ceph running as a Cinder backend (among
other backends), using [cephx authentication][2].

Ceph node
---------

As described on Ceph's documentation, one has to create a pool on the
Ceph nodes (Ceph's doc provides extensive [documentation about the
number of placement groups that should be used][3]). The following
command has to be launched on any Ceph node:

    ::::bash
    ceph osd pool create volumes 128

Because of cephx authentication, we have to create a new user with the
appropriate rights for cinder and nova to be able to access Ceph's
storage. The following command has to be launched on a Ceph node:

    ::::bash
    ceph auth get-or-create client.volumes mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=volumes, allow rx pool=images'

The keyring (token used to identify Ceph users) has to be copied on
cinder-volume nodes. The keyring file can be created with the
following command on a Ceph node:

    ::::bash
    ceph auth get-or-create client.volumes > ceph.client.images.keyring

Cinder-volume nodes
-------------------

The file created above has to be copied on the cinder-volume nodes, in
the directory `/etc/ceph` with the propoer uid and gid:

    ::::bash
    chown cinder:cinder /etc/ceph/ceph.client.images.keyring

Ceph's configuration file `/etc/ceph/ceph.conf` has to be copied at
the same location.

Then we have to install the following packages on these nodes:

    ::::bash
    sudo apt-get install python-ceph ceph-common

Cinder configuration file `/etc/cinder/cinder.conf` has to be updated,
by [setting a new backend][4]. A new backend that we'll call `ceph`
will be added to the `enabled_backends` parameter, and the
corresponding backend section will be created:

    ::::python
    enabled_backends = former-backend,ceph
    [former-backend]
    ...
    [ceph]
    volume_driver = cinder.volume.drivers.rbd.RBDDriver
    volume_backend_name = ceph
    rbd_pool = volumes
    glance_api_version = 2
    rbd_user = volumes
    rbd_secret_uuid = uuid_of_secret

The `rbd_secret_uuid` value cannot be set right now, this parameter
will allow nova to mount Ceph block devices. We will update this value
in a next step.

If the `scheduler_driver` parameter is not set to FilterScheduler, it
has to be updated:

    ::::python
    scheduler_driver = cinder.scheduler.filter_scheduler.FilterScheduler

Once the configuration file updated, cinder-volume service has to be
restarted to load the new configuration:

    ::::bash
    sudo service cinder-volume restart

And a new volume-type has to be added to Cinder, with the following
command, which has to be called with an adminitrator credentials
(OS_USERNAME, OS_TENANT_NAME and OS_PASSWORD):

    ::::bash
    cinder type-create ceph
    cinder type-key ceph set volume_backend_name=ceph

At that point, we should be able to create new Cinder volumes using
Ceph as a backend, with the following command:

    ::::bash
    cinder create --volume-type ceph --display-name ceph-test 1
    cinder list

Nova-compute nodes
------------------

Now we have to configure our nova-compute nodes to allow our VMs to
mount Ceph block devices. To do that, we have to dump Ceph's
authentication token to a file that we'll use on each nova-compute
node. On a Ceph node:

    ::::bash
    ceph auth get-key client.volumes > client.volumes.key

We will also need a `secret.xml` file that will be used on each
compute node, with the following initial content:

    ::::xml
    <secret ephemeral='no' private='no'>
      <usage type='ceph'>
        <name>client.volumes secret</name>
      </usage>
    </secret>
    
Now we can copy these two files (`client.volumes.key` and
`secret.xml`) on any nova-compute node. We'll call this node our first
nova-compute node. On this first node we will define a secret with the
following command:

    ::::bash
    virsh secret-define --file secret.xml

The UUID_OF_SECRET displayed has to be copied somewhere, since it will
be used multiple times to configure nova-compute, as well as
cinder-volume. We can then update the secret's value with the
following command:

    ::::bash
    virsh secret-set-value --secret UUID_OF_SECRET --base64 $(cat client.volumes.key)

If using several nova-compute nodes, the `secret.xml` file has to be
updated on the first nova-compute node (in order to ensure that the
same UUID_OF_SECRET will be used on each nova-compute node), with the
following command:

    ::::bash
    virsh secret-dumpxml UUID_OF_SECRET > secret.xml

 Then with the new `secret.xml` file and the `client.volumes.key`
 file, the previous operation has to be repeated on each nova-compute
 node (except the first one that is already configured):
    
    ::::bash
    virsh secret-define --file secret.xml
    virsh secret-set-value --secret UUID_OF_SECRET --base64 $(cat client.volumes.key)

Finally, cinder-volume configuration files `/etc/cinder/cinder.conf`
have to be updated with the proper UUID_OF_SECRET value:

    ::::python
    rbd_secret_uuid = UUID_OF_SECRET

And cinder-volume service restarted:

    ::::bash
    sudo service cinder-volume restart

After that point, any VM should be able to mount volumes using Ceph
backend!

[0]: http://ceph.com/docs/master/
[1]: http://ceph.com/docs/master/rbd/rbd-openstack/
[2]: http://ceph.com/docs/master/rados/operations/authentication/
[3]: http://ceph.com/docs/master/rados/operations/placement-groups/
[4]: https://wiki.openstack.org/wiki/Cinder-multi-backend