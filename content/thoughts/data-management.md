Title: Data management
Date: 2014-02-27
Tags: Data management

When using several computers (or devices) from different locations,
the question of data management arises. Basically, I wish being able
to access my data from any computer; I wish my data to be protected,
accordingly to its privacy and I wish my data to be backed up
appropriately.

With the arrival of Cloud technologies, some of the requirements
become easier to satisfy. For instance, when using online storage,
data is automatically backed up. But in the same time, the question of
data management takes all of its meaning, because we surely don't want
any information to become public. Hence comes the need to classify its
data according to its privacy level, and to use appropriate storage
backend according to data privacy levels.

Data classification
-------------------

I chose four levels of classification, because it makes sense to me
and map well with storage backend that will be described later. I'll
also borrow some terminology from security guys:

* White data (i.e. public data): this is a blog post, Open Source
  code, or any information that we want to make available to everyone.

* Grey data: this is all the data that I'd gladly share with my
  friends, but do not want my worse enemy to have access to. Fall in
  this category: interesting documents that I found online or public
  information based notes that are not good enough to make a blog
  post.

* Black data: private data, that only trusted people should have
  access to. I'd put in this category any personal documents, from
  emails (some being potentially private) and picture of my holidays
  to administrative documents (ID scans, ...).

* Red data: data that only I should have access to, typically
  credentials (passwords, keys, ...).

Note that the content of these categories may depend on each one's
perception of data privacy. For instance, I put pictures of holidays
in the 'Black data', but we can also consider that pictures of
landscapes may go into the 'Gray data' category.

Storage backend
---------------

So where to store our data? Well now that we've classified our data,
we can choose where we will store it according to the category it is
into.

* White data: The easiest. There are many services on internet that
  will host your public data for free, or almost. For instance, Open
  Source code can be stored into public repositories like [GitHub][0],
  or [Bitbucket][1]. Blogs can be published on [WordPress][2], [GitHub
  Pages][3] or some personal web site. These services provide both
  availability of the data from anywhere, and easy / automatic backup
  (especially when using a versioning tools like git on GitHub).

* Grey data: These data would typically be stored online on a
  "personal" account, which access is restricted by a password. We
  assume that the service provider has full access to the clear data,
  and that this data may be compromised by an attacker. With new cloud
  services available, like free online storage provided by
  [Cloudwatt][4] or [Dropbox][5], it becomes very easy to have files
  stored online and available from multiple locations, backup possibly
  performed automatically (by default the OpenStack object storage
  module, Swift, uses three copies of each file stored in its data
  store) and possibly versioned (Swift provides an option to
  automatically keep several version of each file). A distributed
  network filesystem on [Ceph][6], may be another approach.

* Black data: This data should be stored in a way that provides a fair
  level of data protection, since we typically don't want our service
  provider or hackers to have access to it. There are two completely
  opposite solutions for this: keep this private data locally and not
  put it online at all; or store this data online encrypted with
  strong cryptography algorithms (for instance by using
  [duplicity][7]). Having its data stored online (encrypted) allows us
  to benefit from automatic backup and ubiquity, but is riskier that
  the local storage solution. When stored online encrypted, a security
  breach in the software used to protect the data would allow
  attackers to recover all of the private data. When stored locally,
  backup has to be done by ourselves and the data may not be as easily
  available from different locations.

* Red data: Data in this category are typically keys used to decrypt
  Black data, or passwords to access online services. This data should
  be very well protected. The best way to achieve such level of
  protection is to keep this data locally AND encrypted. This way even
  if the data is stolen, it cannot be read. Backup has to be done
  locally.
  
[0]: https://github.com/
[1]: https://bitbucket.org/
[2]: https://wordpress.org/
[3]: http://pages.github.com/
[4]: http://www.cloudwatt.com/
[5]: http://www.dropbox.com/
[6]: http://ceph.com/
[7]: http://duplicity.nongnu.org/