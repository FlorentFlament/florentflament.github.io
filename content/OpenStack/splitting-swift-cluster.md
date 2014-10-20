Title: Splitting Swift cluster
Date: 2014-10-19

At [Cloudwatt][0], we have been operating a near hundred nodes Swift
cluster in a unique datacenter for a few years. The decision to split
the cluster on two datacenters has been taken recently. The goal is to
have at least one replica of each object on each site in order to
avoid data loss in case of the destruction of a full datacenter (fire,
plane crash, ...).


Constraints when updating a running cluster
-------------------------------------------

Some precautions have to be taken when updating a running cluster with
customers' data. We want to ensure that no data is lost or corrupted
during the operation and that the cluster's performance isn't hurt too
badly. 

In order to ensure that no data is lost, we have to follow some
guidelines including:

* Never move more that 1 replica of any object at any given step; That
  way we ensure that 2 copies out 3 are left intact in case something
  goes wrong.
* Process by small steps to limit the impact in case of failure.
* Check during each step that there is no unusual data corruptions,
  and that corrupted data are correctly handled and fixed.
* Check after each step that data has been moved (or kept) at the
  correct place.
* If any issue were to happen, roll back to previous step.

To limit the impact on cluster's performance, we have to address to
following issues:

* Assess the availability of cluster resources (network bandwidth,
  storage nodes' disks & CPU availability) at different times of day
  and week. This would allow to choose the best time to perform our
  steps.
* Assess the load on the cluster of the steps planned to split the
  cluster.
* Choose steps small enough so that:
    - it fits time frames where cluster's resources are more available;
    - the load incurred by the cluster (and its users) is acceptable.

A number of these requirements have been adressed by Swift for a while:

* When updating Swift ring files, the `swift-ring-builder` tool
  doesn't move more than 1 replica during reassignment of cluster's
  partitions (unless something really went wrong). By performing only
  one reassignment per process step, we ensure that we don't move more
  than 1 replica during 1 step.
* Checking for data corruption is made easy by Swift. 3 processes
  (`swift-object-auditor`, `swift-container-auditor` and
  `swift-account-auditor`) running on storage nodes are continuously
  checking and fixing data integrity.
* Checking that data is at the correct location is also made easy by
  the `swift-dispersion-report` provided.
* Updating the location of data is made seamless by updating and
  copying the Ring files to every Swift nodes. Once updated, the Ring
  files are loaded by Swift processes without the need of being
  restarted. Rollbacking data location is easily performed by
  replacing the new Ring files by previous ones.

However, being able to control the amount of data to move to a new
datacenter at a given step is a brand new feature, that has been fixed
in [version 2.2.0 of Swift][1], released on October 4th of 2014.


Checking data integrity
-----------------------

Swift `auditor` processes (`swift-object-auditor`,
`swift-container-auditor` and `swift-account-auditor`) running on
storage nodes are continuously checking data integrity, by checking
files' checksums. When a corrupted file is found, it is *quarantined*;
the data is removed from from the node and the *replication* mechanism
takes care of replacing the missing data. Below is an example of what
concretely happens when manually corrupting an object.

Let's corrupt data by hand:

    ::::bash
    root@swnode0:/srv/node/d1/objects/154808/c3a# cat 972e359caf9df6fdd3b8e295afd4cc3a/1410353767.57579.data
    blabla
    root@swnode0:/srv/node/d1/objects/154808/c3a# echo blablb > 972e359caf9df6fdd3b8e295afd4cc3a/1410353767.57579.data

The corrupted object is 'quarantined' by the object-auditor when it
checks the files integrity. Here's how it looks like in the log file
`/var/log/syslog`:

    ::::text
    Sep 10 13:56:44 swnode0 object-auditor: Begin object audit "forever" mode (ALL)
    Sep 10 13:56:44 swnode0 object-auditor: Begin object audit "forever" mode (ZBF)
    Sep 10 13:56:44 swnode0 object-auditor: Object audit (ZBF) "forever" mode completed: 0.00s. Total quarantined: 0, Total errors: 0, Total files/sec: 816.33, Total bytes/sec: 0.00, Auditing time: 0.00, Rate: 0.65
    Sep 10 13:56:44 swnode0 object-auditor: Quarantined object /srv/node/d1/objects/154808/c3a/972e359caf9df6fdd3b8e295afd4cc3a/1410353767.57579.data: ETag 9b36b2e89df94bc458d629499d38cf86 and file's md5 6235440677e53f66877f0c1fec6a89bd do not match
    Sep 10 13:56:44 swnode0 object-auditor: ERROR Object /srv/node/d1/objects/154808/c3a/972e359caf9df6fdd3b8e295afd4cc3a failed audit and was quarantined: ETag 9b36b2e89df94bc458d629499d38cf86 and file's md5 6235440677e53f66877f0c1fec6a89bd do not match
    Sep 10 13:56:44 swnode0 object-auditor: Object audit (ALL) "forever" mode completed: 0.02s. Total quarantined: 1, Total errors: 0, Total files/sec: 46.71, Total bytes/sec: 326.94, Auditing time: 0.02, Rate: 0.98
    Sep 10 13:56:44 swnode0 object-auditor: Begin object audit "forever" mode (ZBF)
    Sep 10 13:56:44 swnode0 object-auditor: Object audit (ZBF) "forever" mode completed: 0.00s. Total quarantined: 0, Total errors: 0, Total files/sec: 0.00, Total bytes/sec: 0.00, Auditing time: 0.00, Rate: 0.00
  
The quarantined object is then overwritten by the object-replicator of
a node that has the appropriate replica uncorrupted. Below is an
extract of the log file on such node:

    ::::text
    Sep 10 13:57:01 swnode1 object-replicator: Starting object replication pass.
    Sep 10 13:57:01 swnode1 object-replicator: <f+++++++++ c3a/972e359caf9df6fdd3b8e295afd4cc3a/1410353767.57579.data
    Sep 10 13:57:01 swnode1 object-replicator: Successful rsync of /srv/node/d1/objects/154808/c3a at 192.168.100.10::object/d1/objects/154808 (0.182)
    Sep 10 13:57:01 swnode1 object-replicator: 1/1 (100.00%) partitions replicated in 0.21s (4.84/sec, 0s remaining)
    Sep 10 13:57:01 swnode1 object-replicator: 1 suffixes checked - 0.00% hashed, 100.00% synced
    Sep 10 13:57:01 swnode1 object-replicator: Partition times: max 0.2050s, min 0.2050s, med 0.2050s
    Sep 10 13:57:01 swnode1 object-replicator: Object replication complete. (0.00 minutes)

The corrupted data has been replaced by the correct data on the
initial storage node (where the file had been corrupted):

    ::::text
    root@swnode0:/srv/node/d1/objects/154808/c3a# cat 972e359caf9df6fdd3b8e295afd4cc3a/1410353767.57579.data
    blabla


Checking data location
----------------------

### Preparation

We can use the `swift-dispersion-report` tool provided with Swift to
monitor our data dispersion ratio (ratio of objects on the proper
device / number of objects). A dedicated Openstack account is
required, that will be used by `swift-dispersion-populate` to create
containers and objects.

Then we have to configure appropriately the `swift-dispersion-report`
tool with the `/etc/swift/dispersion.conf` file:

    ::::text
    [dispersion]
    auth_url = http://SWIFT_PROXY_URL/auth/v1.0
    auth_user = DEDICATED_ACCOUNT_USERNAME
    auth_key = DEDICATED_ACCOUNT_PASSWORD

Once properly set, we can initiate dispersion monitoring by populating
our new account with test data:

    ::::bash
    cloud@swproxy:~$ swift-dispersion-populate
    Created 2621 containers for dispersion reporting, 4m, 0 retries
    Created 2621 objects for dispersion reporting, 2m, 0 retries

Our objects should have been placed on appropriate devices. We can
check this:

    ::::bash
    cloud@swproxy:~$ swift-dispersion-report
    Queried 2622 containers for dispersion reporting, 2m, 31 retries
    100.00% of container copies found (7866 of 7866)
    Sample represents 1.00% of the container partition space
    Queried 2621 objects for dispersion reporting, 45s, 1 retries
    There were 2621 partitions missing 0 copy.
    100.00% of object copies found (7863 of 7863)
    Sample represents 1.00% of the object partition space

### Monitoring data redistribution

Once updated ring has been pushed to every nodes and proxy servers, we
can follow the data redistribution with the
`swift-dispersion-report`. The migration is terminated when the number
of objects copies reach 100%. Here's an example of results obtained on
a 6 nodes cluster.

    ::::bash
    cloud@swproxy:~$ swift-dispersion-report
    Queried 2622 containers for dispersion reporting, 3m, 29 retries
    100.00% of container copies found (7866 of 7866)
    Sample represents 1.00% of the container partition space
    Queried 2621 objects for dispersion reporting, 33s, 0 retries
    There were 23 partitions missing 0 copy.
    There were 2598 partitions missing 1 copy.
    66.96% of object copies found (5265 of 7863)
    Sample represents 1.00% of the object partition space
        
    # Then some minutes later
    cloud@swproxy:~$ swift-dispersion-report
    Queried 2622 containers for dispersion reporting, 5m, 0 retries
    100.00% of container copies found (7866 of 7866)
    Sample represents 1.00% of the container partition space
    Queried 2621 objects for dispersion reporting, 26s, 0 retries
    There were 91 partitions missing 0 copy.
    There were 2530 partitions missing 1 copy.
    67.82% of object copies found (5333 of 7863)
    Sample represents 1.00% of the object partition space


Limiting the amount of data to move
-----------------------------------

There has been a number of recent contributions to Swift that have
been done in order to allow the smooth addition of nodes to a new
region.

With versions of `swift-ring-builder` earlier than Swift 2.1, when
adding a node to a new region, 1 replica of every object was moved to
the new region in order to maximise the dispersion of objects accross
different regions. Such algorithm had severe drawbacks. Let's consider
a one region Swift cluster with 100 storage nodes. Adding 1 node to a
second region had the effect of transferring 1/3 of the cluster's data
to the new node, which would not have the capacity to store the data
previously distributed over 33 nodes. So in order to add a new region
to our cluster, we had to add in 1 step enough nodes to store 1/3 of
our data. Let's consider we add 33 nodes to the new region. While
there is enough capacity on these nodes to receive 1 replica of every
objects, such operation would trigger the transfer of PetaBytes of
data to the new nodes. With a 10 Gigabits/second link between the 2
datacenters, such transfer would take days if not weeks, during which
the cluster's network and destination nodes' disks would be saturated.

With [commit 6d77c37][2] ("Let admins add a region without melting
their cluster"), that has been released with Swift 2.1, the number of
partitions assigned to nodes in a new region was determined by the
weights of the nodes' devices. This feature allowed a Swift cluster
operator the limit the amount of data transferred to a new
region. However, because of [bug 1367826][3] ("swift-ringbuilder
rebalance moves 100% partitions when adding a new node to a new
region"), even when limiting the amount of data transfered to a new
region, a big amount of data moved uselessly inside the initial
region. For instance, it could happen that after a `swift-ring-builder
rebalance` operation, 3% of partitions were assigned to the new
region, but 88% of partitions were reassigned to new nodes inside the
first region. The would lead to uselessly loading the cluster's
network and storage nodes.

Eventually, [commit 20e9ad5][4] ("Limit partition movement when adding
a new tier") fixed [bug 1367826][3]. This commit has been released
with Swift 2.2. It allows an operator to choose to the amount of data
that flows between regions, when adding nodes to a new region, without
border effects. This feature enable the operator to perform a multi
steps cluster split, by first adding devices with very low weights to
a new region, then by progressively increasing the weights step by
step, until 1 replica of every objects has been transfered to the new
region. Since the number of partitions assigned to the new region
depends on the weights assigned to the new devices, the operator has
to compute the appropriate weights.

### Computing new region weight for a given ratio of partitions

Given:

* w1 is the weight of a single device in region r1
* r1 has n1 devices
* W1 = n1 * w1 is the full weight of region r1
* r2 has n2 devices
* w2 is the weight of a single device in region r2
* W2 = n2 * w2 is the full weight of region r2
* r is the ratio of partitions we want in region r2

We have:

* r = W2 / (W1+W2)
* <=> W2 = (r*W1) / (1-r)

### Computing new devices weight for a given number of partitions

In some cases the operator may prefer to specify the number of
partitions (rather than its ratio) that he wishes to assign to the
devices of a new region.

Given:

* p1 the number of partitions in region r1
* W1 the full weight of region r1
* p2 the number of partitions in region r2
* W2 the full weight of region r2

We have the following equality:

* p1/W1 = p2/W2
* <=> W2 = W1*p2 / p1


WIP
===


=== First Step - Moving few GigaBytes ===

==== Adding 1 storage node to the new region an moving a few Gigabytes ====

By adding one node to our cluster, and assigning 1 partition to each device, we will move approximatively 0.003% of partitions, corresponding to about 3 GB of a 100 TB cluster.

Tools:

* https://git.corp.cloudwatt.com/florent.flament-ext/swift-ring-builder-scripts/blob/master/swift-add-nodes.py

We will use the `swift-add-nodes.py` script to easily add nodes to our new region with a minimal weight so that only 1 partition will be assigned to each device.

Assumptions:

* the node has 24 HDD disks `sdb1`, `sdc1`, ..., `sdy1`

If this assumption is false, the `swift-add-nodes.py` script must be updated accordingly.

Commands:

    ::::bash
    (swift-2.1-patched)florent@xubos:~/src/cw-docs/swift-cluster-split/swift-poc$ python swift-add-nodes.py object.builder object.builder.s1 2 6000 127.0.0.1
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdb1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdc1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdd1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sde1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdf1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdg1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdh1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdi1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdj1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdk1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdl1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdm1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdn1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdo1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdp1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdq1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdr1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sds1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdt1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdu1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdv1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdw1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdx1', 'port': 6000}
    Adding device: {'weight': 5.11, 'zone': 0, 'ip': '127.0.0.1', 'region': 2, 'device': 'sdy1', 'port': 6000}
    (swift-2.1-patched)florent@xubos:~/src/cw-docs/swift-cluster-split/swift-poc$ swift-ring-builder object.builder.s1 rebalance
    Reassigned 43 (0.02%) partitions. Balance is now 0.19.                                

The IP used in the example `127.0.0.1` should be replaced with the internal IP of the storage node to add to the cluster.

Note that the partitions percentage indicated is the ratio of 1 replica moved (i.e 1/3 of all data in a 3 replicas cluster).

The same operation has to be done for the `container.builder` and the `account.builder`.

 $ python swift-add-nodes.py container.builder container.builder.s1 2 6001 127.0.0.1
 $ swift-ring-builder container.builder.s1 rebalance
 $ python swift-add-nodes.py account.builder account.builder.s1 2 6002 127.0.0.1
 $ swift-ring-builder account.builder.s1 rebalance

==== Backup updated builders ====

    $ git add account.builder container.builder object.builder
    $ # If rings are stored in repository save them as well.
    $ git commit
    $ git push

==== Update ring file on Swift nodes ====

* On every Swift nodes (proxy + storage): update ring files (copy those generated by the rebalance operation):

    * account.ring.gz
    * container.ring.gz
    * object.ring.gz

Configuration (and ring) files must be updated on appropriate servers via the usual mechanism (Chef).

Save updated configuration into the versionning tool.

=== Second step - adding every new nodes to the new region ===

==== Adding 11 storage nodes to the new region and moving a few Gigabytes ====

Under the following assumptions:

* We have 11 nodes split in two zones corresponding to two racks ;
* 6 nodes are physically placed in the first zone (1st rack) ;
* 5 nodes are physically placed in the second zone (2nd rack) ;
* Each node has 24 HDD disks `sdb1`, `sdc1`, ..., `sdy1`

We can add the remaining 10 nodes and assign one partition to each device.

 $ python swift-add-nodes.py object.builder.s1 object.builder.s2 2 6000 127.0.0.2 127.0.0.3 127.0.0.4 127.0.0.5 127.0.0.6 127.0.0.7 127.0.0.8 127.0.0.9 127.0.0.10 127.0.0.11
 ...
 $ swift-ring-builder object.builder.s2 rebalance
 Reassigned 240 (0.09%) partitions. Balance is now 0.22.

The same operation has to be done for containers and accounts

 $ python swift-add-nodes.py container.builder.s1 container.builder.s2 2 6001 127.0.0.2 127.0.0.3 127.0.0.4 127.0.0.5 127.0.0.6 127.0.0.7 127.0.0.8 127.0.0.9 127.0.0.10 127.0.0.11
 ...
 $ swift-ring-builder container.builder.s2 rebalance
 Reassigned 275 (0.84%) partitions. Balance is now 3.69.
 $ python swift-add-nodes.py account.builder.s1 account.builder.s2 2 6002 127.0.0.2 127.0.0.3 127.0.0.4 127.0.0.5 127.0.0.6 127.0.0.7 127.0.0.8 127.0.0.9 127.0.0.10 127.0.0.11
 ...
 $ swift-ring-builder account.builder.s2 rebalance
 Reassigned 240 (0.09%) partitions. Balance is now 0.22.

=== Next steps: Moving data by steps of 10% ===

==== Update builders ====

Tools:
* https://git.corp.cloudwatt.com/florent.flament-ext/swift-ring-builder-scripts/blob/master/swift-assign-partitions.py

Script `swift-assign-partitions.py` allows assigning a chosen ratio of partitions to the new region. Typical values to use would be 0.03, 0.06, 0.09, ..., 0.3334. This would increase the partitions count by steps of 3% until one third of total cluster data is stored in the new region.

 $ python swift-assign-partitions.py object.builder.s2 object.builder.s3 2 0.03
 ...
 $ swift-ring-builder object.builder.s3 rebalance
 Reassigned 24954 (9.52%) partitions. Balance is now 0.71.

Same thing must be done for containers and accounts:

 $ python swift-assign-partitions.py container.builder.s2 container.builder.s3 2 0.03
 ...
 $ swift-ring-builder container.builder.s3 rebalance
 (swift-2.1-patched)florent@xubos:~/src/cw-docs/swift-cluster-split/swift-poc$ swift-ring-builder container.builder.s3 rebalance
 Reassigned 3008 (9.18%) partitions. Balance is now 7.73.
 -------------------------------------------------------------------------------
 NOTE: Balance of 7.73 indicates you should push this 
       ring, wait at least 1 hours, and rebalance/repush.
 -------------------------------------------------------------------------------
 $ python swift-assign-partitions.py account.builder.s2 account.builder.s3 2 0.03
 ...
 $ swift-ring-builder account.builder.s3 rebalance                                                                           
 Reassigned 24939 (9.51%) partitions. Balance is now 0.71.
 
At each step, builders must be backuped and rings should be pushed to Swift nodes.





Tuning configuration to have traffic concentrated on primary datacenter
-----------------------------------------------------------------------

The following options must be updated (or added). Other options remain unchanged.

* On Swift proxy servers: File `proxy-server.conf`

    [app:proxy-server]
    read_affinity = r1=100
    write_affinity = r1



[0]: https://www.cloudwatt.com/en/
[1]: https://github.com/openstack/swift/releases/tag/2.2.0
[2]: https://review.openstack.org/#/c/115441/
[3]: https://bugs.launchpad.net/swift/+bug/1367826
[4]: https://review.openstack.org/#/c/121422/
