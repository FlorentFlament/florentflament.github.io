Title: Openstack volume in-use although VM doesn't exist
Date: 2014-01-04
Tags: OpenStack, Cinder, bug

A user at [Cloudwatt][0] had an issue about Cinder volumes with
status `in-use`, attached to VMs that didn't exist anymore. I could
find similar bugs referenced in launchpad [here][1] and [there][2],
both with status `invalid`... But I didn't succeed in reproducing the
bug (using both the Horizon dashboard and the CLIs) until I got
feedback about what our user was doing.

The issue
---------

The issue appears when one tries to attach a volume by using the
`python-cinderclient` library in some Python code. There are actually
some weird methods for both version of the API.

* [cinderclient.v1.volumes.VolumeManager.attach][3]
* [cinderclient.v2.volumes.VolumeManager.attach][4]

These methods call the Cinder `POST /volumes/{volume_id}/action` API,
which is neither documented [here][5] nor [there][6]. They can be used
to "set attachment metadata", which according to my opinion has no
good reason to be performed directly by a user.

    ::::python
    >>> import time
    >>> import cinderclient.v1.client
    >>> import novaclient.v1_1.client
    >>>
    >>> # Creating manager
    ...
    >>> args = ["username", "password", "project_name", "auth_url"]
    >>> cinder = cinderclient.v1.client.Client(*args)
    >>> nova = novaclient.v1_1.client.Client(*args)
    >>>
    >>> # Getting an image and a flavor to launch our VM
    ...
    >>> img = nova.images.list()[0]
    >>> fla = nova.flavors.list()[0]
    >>>
    >>> # Creating our resources (vm and volume)
    ...
    >>> vm = nova.servers.create("MyVm", img, fla)
    >>> vol = cinder.volumes.create(1, display_name="MyVol")
    >>>
    >>> # Waiting for VM to be spawned
    ...
    >>> while nova.servers.get(vm.id).status != "ACTIVE":
    ...    time.sleep(1)
    ...
    >>> # Try an attach the volume using the VolumeManager.attach method
    ...
    >>> cinder.volumes.attach(vol, vm.id, "/dev/vdb")
    (<Response [202]>, None)
    >>> cinder.volumes.get(vol.id)._info["attachments"]
    [{u'device': u'/dev/vdb', u'server_id': u'3ee03547-7b93-4c8f-9316-bc2adafbd08a', u'volume_id': u'f024883d-4b35-4894-9fbf-51498e6c3c09', u'host_name': None, u'id': u'f024883d-4b35-4894-9fbf-51498e6c3c09'}]
    >>> # Well it looks like it is attached
    ...
    >>> vm = nova.servers.get('3ee03547-7b93-4c8f-9316-bc2adafbd08a')
    >>> vm._info['os-extended-volumes:volumes_attached']
    []
    >>> # But actually it isn't
    ...
    >>>

The solution
------------

The solution is to use the appropriate method to attach a volume to an
instance. This should be done by using the
[novaclient.v1_1.volumes.VolumeManager.create_server_volume][7]
method. It actually allows to "attach a volume to a server", which is
what we want to do (And yes the method's name is not super clear).

    ::::python
    >>> # Let's continue on the example above
    ... # First by clearing our volume attachment's metadata
    ... # to recover a consistent state
    ... 
    >>> vol.detach()
    (<Response [202]>, None)
    >>> cinder.volumes.get(vol.id)._info['attachments']
    []
    >>> nova.servers.get(vm.id)._info['os-extended-volumes:volumes_attached']
    []
    >>> # Now we can use the VolumeManager.create_server_volume method
    ... # to really attach our volume to our vm
    ...
    >>> nova.volumes.create_server_volume(vm.id, vol.id, "/dev/vdb")
    <Volume: f024883d-4b35-4894-9fbf-51498e6c3c09>
    >>> cinder.volumes.get(vol.id)._info["attachments"]
    [{u'device': u'/dev/vdb', u'server_id': u'3ee03547-7b93-4c8f-9316-bc2adafbd08a', u'volume_id': u'f024883d-4b35-4894-9fbf-51498e6c3c09', u'host_name': None, u'id': u'f024883d-4b35-4894-9fbf-51498e6c3c09'}]
    >>> nova.servers.get(vm.id)._info['os-extended-volumes:volumes_attached']
    [{u'id': u'f024883d-4b35-4894-9fbf-51498e6c3c09'}]
    >>> 
    
The bug
-------

Although, we could argue that the inconsistent state is due to a bad
usage of the client libraries, I do believe that Cinder API (and
therefore python-cinderclient) should not allow the user to put its
resources in an inconsistent state. Moreover, it isn't possible to
recover from such state by using the Horizon dashboard or the CLIs. To
do so, one has to either use the Python client libraries, or update
entries in the database manually...

Recovering from inconsistent state
----------------------------------

One way to recover from a "volume attached to non-existent VM"
inconsistent state, is to manually update entries in the Cinder
database.

    ::::bash
    $ mysql cinder
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A

    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 1900
    Server version: 5.5.34-0ubuntu0.12.04.1-log (Ubuntu)

    Copyright (c) 2000, 2013, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> SELECT id,status,attach_status,mountpoint,instance_uuid from volumes;
    +--------------------------------------+---------+---------------+------------+--------------------------------------+
    | id                                   | status  | attach_status | mountpoint | instance_uuid                        |
    +--------------------------------------+---------+---------------+------------+--------------------------------------+
    | 0580142b-bfb5-4113-8676-4fb783ec05f2 | deleted | detached      | NULL       | NULL                                 |
    | 1085d96e-ae82-484b-8495-27cc2f25c9c3 | deleted | detached      | NULL       | NULL                                 |
    | 4fbff7ce-2c9f-4116-ad1e-12f78001da2d | deleted | detached      | NULL       | NULL                                 |
    | 57b32eaf-7b71-49bf-a8fd-4115567a6cda | in-use  | attached      | /dev/vdb   | fa53d190-426b-4ce6-8d36-1af408c25225 |
    | 60a7eb30-9849-4b8d-9ca1-8f554b9a4045 | deleted | detached      | NULL       | NULL                                 |
    | a34ca08a-2e6b-4820-b472-91aa27b47261 | deleted | detached      | NULL       | NULL                                 |
    | d827daa5-c8d7-427b-a53c-8be918a1a6fb | deleted | detached      | NULL       | NULL                                 |
    +--------------------------------------+---------+---------------+------------+--------------------------------------+
    7 rows in set (0.00 sec)

    mysql> UPDATE volumes SET status="available", attach_status="detached", mountpoint=NULL, instance_uuid=NULL WHERE id="57b32eaf-7b71-49bf-a8fd-4115567a6cda";
    Query OK, 1 row affected (0.00 sec)
    Rows matched: 1  Changed: 1  Warnings: 0

    mysql> SELECT id,status,attach_status,mountpoint,instance_uuid from volumes;
    +--------------------------------------+-----------+---------------+------------+---------------+
    | id                                   | status    | attach_status | mountpoint | instance_uuid |
    +--------------------------------------+-----------+---------------+------------+---------------+
    | 0580142b-bfb5-4113-8676-4fb783ec05f2 | deleted   | detached      | NULL       | NULL          |
    | 1085d96e-ae82-484b-8495-27cc2f25c9c3 | deleted   | detached      | NULL       | NULL          |
    | 4fbff7ce-2c9f-4116-ad1e-12f78001da2d | deleted   | detached      | NULL       | NULL          |
    | 57b32eaf-7b71-49bf-a8fd-4115567a6cda | available | detached      | NULL       | NULL          |
    | 60a7eb30-9849-4b8d-9ca1-8f554b9a4045 | deleted   | detached      | NULL       | NULL          |
    | a34ca08a-2e6b-4820-b472-91aa27b47261 | deleted   | detached      | NULL       | NULL          |
    | d827daa5-c8d7-427b-a53c-8be918a1a6fb | deleted   | detached      | NULL       | NULL          |
    +--------------------------------------+-----------+---------------+------------+---------------+
    7 rows in set (0.00 sec)

    mysql> Bye
    $ cinder list
    +--------------------------------------+-----------+------+------+-------------+----------+-------------+
    |                  ID                  |   Status  | Name | Size | Volume Type | Bootable | Attached to |
    +--------------------------------------+-----------+------+------+-------------+----------+-------------+
    | 57b32eaf-7b71-49bf-a8fd-4115567a6cda | available | vol1 |  1   |     None    |  false   |             |
    +--------------------------------------+-----------+------+------+-------------+----------+-------------+

[0]: http://www.cloudwatt.com
[1]: https://bugs.launchpad.net/cinder/+bug/1201418
[2]: https://bugs.launchpad.net/nova/+bug/1096197
[3]: https://github.com/openstack/python-cinderclient/blob/master/cinderclient/v1/volumes.py
[4]: https://github.com/openstack/python-cinderclient/blob/master/cinderclient/v1/volumes.py
[5]: http://docs.openstack.org/api/openstack-block-storage/2.0/content/Volumes.html
[6]: http://api.openstack.org/api-ref-blockstorage.html
[7]: https://github.com/openstack/python-novaclient/blob/master/novaclient/v1_1/volumes.py
