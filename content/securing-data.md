Title: Securing Data
Date: 2014-05-03 23:34
Tags: Data Safety, Data Security

As a data geek, I've been wondering how I could protect my data from
the main threats (if possible by using only open source software). For
instance, losing data because of a hardware failure is just something
that shouldn't happen anymore, thanks to all the technology available
today. One could argue that cloud storage services may be the
solution, which may be true to deal with hardware failure; but there
are other threats to be taken into account that are worsen by the use
of the such services (I'm thinking about piracy).

So what's the need in term of data safety, security and availability?
Well here's how I would summarize my ideal target. I basically wish to
protect my data against most threats, while still being able to access
it according to my usage. I've been thinking about the following
threats:

* Hardware failure (Hard disk failure)

* Piracy (Pirate breaking into ones computer / online account)

* Human mistakes (mistakenly deleting important data)

* Theft (Losing data stored on the stolen hardware, thieves abusing
  of sensitive data).



Data Safety and Security
========================

Basically, data protection may be split into two categories:

* Data Safety, consisting in measures against hardware failures and
  human mistakes (also natural disasters if we really want to ensure a
  first grade safety level);

* Data Security, consisting in protecting data against theft and
  piracy.


Data Safety
-----------

In order to avoid losing data because of hardware failure data should
be duplicated. So that if a hard disk fails, the data still remains on
the second disk. Some technologies like RAID (Hardware or Software),
provide such service by performing real time data duplication on
several disks.

To deal with natural disasters, like fires or floods, we may duplicate
our data at distant locations. This is becoming easier with new
technologies like [Ceph][1] or [OpenStack Swift][2], that allow real
time duplication of data on distant storage nodes.

Another category of threat (maybe the most frequent) is human
mistake. One can easily delete an important file by mistake. The good
old solution to deal with such issues is doing regular backups. While
this is a very good idea, depending on the frequency of the backups,
we may accidentally loose some recent data that didn't have the time
to be saved. There are other means to ensure data can be recovered
even after being deleted, such as versioning by using tools like
[git][3], or [ownCloud][4].


Data Security
-------------

Piracy is a quite broad topic. However, by following a few simple
rules, we may avoid most of piracy threats:

* Don't store online data that we don't need to have online. Online
  data have much more chances of being stolen than offline data (or
  data available in a private network); If pirates cannot access the
  data through the network, it is much more complicated to gain access
  to it. This is the main reason why I believe that cloud storage may
  not be the best solution for everything. If by chance a pirate
  guesses one's cloud storage account password, he can then access
  freely any data that has been stored there.

* Strongly encrypt private data that may be accessed by pirates or
  thieves. Basically any data may potentially be accessed by pirates or
  thieves, but as written previously, online data is much more
  vulnerable, and should therefore be encrypted in priority.

Theft can happen:

* To deal with the issue of loosing its data because of its laptop
  being stolen, we may use some solutions that were discussed
  previously to ensure data safety. Good old backups are still a
  working solution; real time duplication at different locations is
  another one.

* To deal with private data exploit (meaning malicious usage of
  private data by thieves), encryption is a good option. By ensuring
  that the thieves cannot decrypt the data, we protect us against such
  scenario.


Cost of Protection
------------------

All these measures for ensuring a proper data protection do have a
cost. To duplicate our data, we need twice as much hard disks than if
we don't. To encrypt our data and decrypt it on the fly to read it
consumes more CPU than processing plain files. Although storage costs
as well as computing costs have collapsed these last years, we may be
smart by [categorizing our data][5] (e.g: public versus private data,
text documents versus binary files, small versus large files, ...) and
apply different safety and security measures accordingly.


Layered architecture
====================

Now we need to find out an overall solution that will meet our
requirements. There is not a single tool I can think of that provides
all of the features mentioned in this article. To build our overall
solutions, we'll need to have several tools work together. The
approach I thought about is to split our need into features provided
by different layers:

* A versioning layer (git, owncloud, ...) that keeps track of the
  history of our data and allows recovering data that has been
  accidentally deleted or altered.

* An exposition layer, which is more a functional layer that a
  security one, that make data available according to our
  requirements.  For instance, it makes sense to have emails available
  from the internet through IMAPs, while other data may only be
  available through ssh from a host on the private network.

* An encryption layer to deal with private data abuse by
  thieves. Technologies like dm-crypt, LUKS and Truecrypt seem to be
  good candidates.

* A (possibly redundant) storage backend: object storage, block
  storage or file system (ceph, RAID, ...). First thoughts lead me to
  think about using Ceph as a backend storage. However, it happens
  that Ceph monitor's play a crucial role and may become a SPOF
  (single point of failure) if not redundant. Also they must be an odd
  number, which means at least 3 nodes are required. A simpler RAID
  approach with regular backups seems to be a good compromise for
  small infrastructures.

* And regular backups. This is cheap, easy to implement, and deals
  with most of our issues. However, the efficiency of backups directly
  depends on their frequency, since work done between successive
  backups will be lost in case of hardware failure, human mistake or
  theft.


Example table
-------------

    +------------------+-------------+--------+-------------+-------------+------------------+
    |                  |             |        |             |             |                  |
    | Files            | text / code | Emails | Binary data | Binary data |      Threat      |
    |                  |             |        | important   | throwable   |                  |
    +------------------+-------------+--------+-------------+-------------+------------------+
    |                  |             |                                    |                  |
    | Version layer    |     git     |                 None               | Human            |
    |                  |             |                                    | error ++         |
    +------------------+-------------+--------+---------------------------+------------------+
    |                  |             |        |                           |                  |
    | Exposition layer |     ssh     | IMAPs  |            NFS            |                  |
    |                  |             |        |                           |                  |
    +------------------+------------------- Block devices ----------------+------------------+
    |                  |                      |                           |                  |
    | Encryption layer |         LUKS         |           None            | Theft (abuse)    |
    |                  |                      |                           |                  |
    +------------------+------------------- Block devices ----------------+------------------+
    |                  |                                                  |                  |
    | Redundancy       |                  Disks / RAID                    | Hardware         |
    |                  |                                                  | failure ++       |
    +------------------+------------------------------------+-------------+------------------+
    |                  |                                    |             | Human error /    |
    | Backup           |         Regular snapshots          |    None     | Theft (loss) /   |
    |                  |                                    |             | Piracy /         |
    |                  |                                    |             | Hardware failure |
    +------------------+------------------------------------+-------------+------------------+



[1]: http://ceph.com/
[2]: http://www.openstack.org/software/openstack-storage/
[3]: http://git-scm.com/
[4]: http://owncloud.org/
[5]: http://www.florentflament.com/blog/data-management.html