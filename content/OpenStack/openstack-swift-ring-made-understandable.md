Title: OpenStack Swift Ring made understandable
Date: 2014-10-11 22:00
Tags: OpenStack, Swift, Ring

When people talk about OpenStack Swift, we often hear the word
Ring. This is because the Ring is a central piece in how Swift is
working. But what *is* this thing everyone's talking about ?

The Ring refers to 3 files that are shared among every Swift nodes
(storage and proxy nodes):

* object.ring.gz
* container.ring.gz
* account.ring.gz

There is actually one ring per type of data manipulated by Swift:
Objects, Containers and Accounts. These files determine on which
physical devices (hard disks) will be stored each object (and also
each container and account). The number of devices on which an object
is stored depends on the number of replicas (copies) specified for the
Swift cluster.


How does it concretely work
---------------------------

When receiving an object to store, Swift computes a (MD5) hash of the
object's full name (including its account's and container's name). A
part of this hash is kept and interpreted by Swift as the partition
number. The length of the hash segment kept depends on the number of
partitions that has been set in the Swift cluster; This number is
necessarily a power of 2. So that if we keep n bits of the hash, we
have 2^n partitions.

The object ring is a map that associates each partition to a specific
physical device. This mechanism is then repeated for every object's
replicas, and also for containers and accounts.

To be more specific, the object's ring has 3 components:

* What is referred in the code as the `_replica2part2dev` table (which
  name is relatively explicit as we'll see later on)
* The table of devices describing each device
* The length of an object's hash to consider as the partition number

The `_replica2part2dev` structure is a 2-dimensional table, so that
for any (replica number, partition number) couple, the table indicates
the physical device, where the object should be stored.

The devices table contains every information that a Swift node needs
in order to reach a given device; It consists mostly in the device's
storage node's IP address, the TCP port to use, and the physical
device name on the storage node.

In the end, the Ring is composed of 2 tables and one integer. If I
were to choose a name for such structure, I would call it the Table. I
couldn't find any explanation of why the name Ring was adopted, but my
guess is that some previous algorithm may have used some modular
computation, which people tend to represent using rings..


Example
-------

Here is a simple example to make everything clear. Let's consider a
Swift cluster with 2 storage nodes, with the following IPs addresses:
`192.168.0.10` and `192.168.0.11`. Each storage node has two devices:
`sdb1` and `sdc1`.

An example of `_replica2part2dev` table with 3 replicas, 8 partitions
and 4 devices would be:

    ::::text
    r
    e  |   +-----------------+
    p  | 0 | 0 1 2 3 0 1 2 3 |
    l  | 1 | 1 2 3 0 1 2 3 0 |
    i  | 2 | 2 3 0 1 2 3 0 1 |
    c  v   +-----------------+
    a        0 1 2 3 4 5 6 7
           ------------------>
               partition
    
The table has 3 lines, one for each replica, and 8 columns, one for
each partition. To find the device storing the replica number 1 of
partition number 2, we select the line of index 1 and column of index
2. This lead us to the device ID 3.

The devices table is very similar to what we can obtain by using the
`swift-ring-builder` with only the builder file as argument:

    ::::bash
    $ swift-ring-builder mybuilder 
    mybuilder, build version 4
    8 partitions, 3.000000 replicas, 1 regions, 1 zones, 4 devices, 0.00 balance
    The minimum number of hours before a partition can be reassigned is 0
    Devices:    id  region  zone      ip address  port  replication ip  replication port      name weight partitions balance meta
                 0       1     1    192.168.0.10  6000    192.168.0.10              6000      sdb1 100.00          6    0.00 
                 1       1     1    192.168.0.10  6000    192.168.0.10              6000      sdc1 100.00          6    0.00 
                 2       1     1    192.168.0.11  6000    192.168.0.11              6000      sdb1 100.00          6    0.00 
                 3       1     1    192.168.0.11  6000    192.168.0.11              6000      sdc1 100.00          6    0.00 
    
The device of ID 3 can be found on server 192.168.0.11, port 6000,
device name sdc1.


Simple is good
--------------

What I like with such mechanism is that the smartness of the data
placement is performed by the `swift-ring-builder`, a standalone tool
provided with Swift. Once the rings have been built, Swift processes
running on the Swift nodes have a fully deterministic and easily
predictable behavior.

The `swift-ring-builder` manipulates `builders` files; these are files
containing architectural information about the Swift cluster (like
distribution of devices and nodes among regions and zones). These
`builders` are then used to generate the `rings` files. As with the
rings, there is one builder per type of data (objects, containers and
accounts).

Thanks to this mechanism the complexity of smartly storing objects has
been well separated between:

* Smartly assigning partitions (and corresponding objects, containers
  and accounts) to devices, taking into account the cluster's
  architecture. This is performed by the `swift-ring-builder`

* Ensuring that files are stored uncorrupted at the appropriate
  locations; This is performer by the processes running on the Swift
  nodes.


More
----

For more information about the ring, one can read the [Swift's
developer documentation about the Ring][1].

[1]: http://docs.openstack.org/developer/swift/overview_ring.html
