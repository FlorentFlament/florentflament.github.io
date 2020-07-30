Title: Right VM cost
Date: 2014-08-03
Tags: Virtualization,VM,Hardware,Costs

With cloud Virtual Machines prices dropping month after month, we may
be asking if the margins previously done by cloud operators were not
outrageously high. I actually find surprising that current VM price is
on average higher than equivalent dedicated server even though
virtualization allows sharing more hardware.


Comparing dedicated server versus VM costs
------------------------------------------

Low cost dedicated servers:

* CPU 1 Core / 2 threads - RAM 2 GB - HDD 500 GB - costs €5 / month at [Kimsufi][1]
* CPU 1 Core - RAM 2 GB - SHDD 500 GB - costs €9.99 / month at [online][2]

Low cost VMs:

* CPU 2 Cores - RAM 2 GB - SSD 40 GB - costs $20 / month at [DigitalOcean][3]
* vCPUs 2 - RAM 2 GB - SSD 60 GB - $54 / month at [rackspace][4]
* vCPUs 1 (fractional) - RAM 2 GB - 0 (additional storage cost) - $19 / month at [Amazon][5]

Virtual machines CPUs don't have much meaning, since depending on the
underlying hardware a virtual machine CPU may correspond to a physical
CPU core, thread or a fraction of CPU if the hypervisor is sharing
CPUs among VMs. Amazon introduces an EC2 Compute Unit (ECU), that
would allow objectively [comparing CPU performance between VMs][6].

At first glance we can see that for low end configurations the
price/performance ratio of Virtual Machines looks much higher than
ratio of dedicated servers.


Estimating cost of hardware
---------------------------

We can make an estimate of the cost of hardware by performing a
[multiple regression analysis][7] on dedicated server prices.

[OVH prices][8] (only considering Intel Xeon CPUs):

    ::::text
    |-------------------------------------------------------------------------------------------|
    |         CPU type        | # threads | RAM (GB) | HDD (TB) | SSD (GB) | Price (€/month HT) |
    |-------------------------------------------------------------------------------------------|
    |                                 OVH Enterprise                                            |
    |-------------------------------------------------------------------------------------------|
    | Intel Xeon E5-1620v2    |     8     |    64    |     4    |     0    |       €81.99       |
    | Intel Xeon E5-1650v2    |    12     |   128    |     4    |     0    |      €131.99       |
    | Intel Xeon 2x E5-2650v2 |    32     |   128    |     4    |     0    |      €202.99       |
    | Intel Xeon 2x E5-2670v2 |    40     |   256    |     4    |     0    |      €302.99       |
    |-------------------------------------------------------------------------------------------|
    |                                   OVH Infra                                               |
    |-------------------------------------------------------------------------------------------|
    | Intel Xeon E5-1620v2    |     8     |    32    |     6    |     0    |       €81.99       |
    | Intel Xeon E5-1650v2    |    12     |    64    |     6    |     0    |      €141.99       |
    | Intel Xeon 1x E5-2650v2 |    16     |   128    |     6    |     0    |      €191.99       |
    | Intel Xeon 2x E5-2650v2 |    32     |   128    |     6    |     0    |      €302.99       |
    | Intel Xeon 2x E5-2670v2 |    40     |   256    |     6    |     0    |      €402.99       |
    |-------------------------------------------------------------------------------------------|
    |                                   OVH Storage                                             |
    |-------------------------------------------------------------------------------------------|
    | Intel Xeon 1x E5 2620v2 |    12     |    48    |    48    |     0    |      €372.99       |
    | Intel Xeon 1x E5 2620v2 |    12     |    48    |    72    |     0    |      €522.00       |
    | Intel Xeon 2x E5 2620v2 |    24     |    64    |   144    |     0    |      €822.00       |
    | Intel Xeon 2x E5 2620v2 |    24     |    64    |   216    |     0    |     €1272.00       |
    | Intel Xeon 1x E5 2620v2 |    12     |    48    |    36    |   360    |      €372.99       |
    | Intel Xeon 1x E5 2620v2 |    12     |    48    |    54    |   360    |      €522.00       |
    | Intel Xeon 2x E5 2620v2 |    24     |    64    |   108    |  1080    |      €822.00       |
    | Intel Xeon 2x E5 2620v2 |    24     |    64    |   162    |  1080    |     €1272.00       |
    |-------------------------------------------------------------------------------------------|

In our case, for each server setting we have:
Yi = ß1 + ß2*Xi2 + ß3*Xi3 + ß4*Xi4 + ß5*Xi5 + Ei
where:

* Yi is the price for setting i
* ß1 is a constant per server
* ß2 is the estimate of € / thread
* ß3 is the estimate of € / GB of RAM
* ß4 is the estimate of € / TB of HDD
* ß5 is the estimate of € / GB of SSD
* Xi2 is the number of CPU threads for setting i
* Xi3 is the amount of RAM in GB for setting i
* Xi4 is the amount of HDD space in TB for setting i
* Xi5 is the amount of SSD space in GB for setting i
* Ri is the residual error for setting i

We can estimate ßj coefficients with the following formula:
ß = (Xt*X)-¹*Xt*Y

    ::::bash
    $ python pricing_vm_simple.py
    Constant: 31.3530724158
    Eur / CPU thread: 3.12689639938
    Eur / GB of RAM: 0.639580183605
    Eur / TB of HDD: 5.18992626031
    Eur / GB of SSD: 0.197627042107
    R^2: 0.982339781679

Assuming that we rent some of the afore mentioned dedicated servers,
what comes out from these results is that the most expensive resource
is the Intel Xeon CPU thread, which costs more than €3/month. Hence
the monthly cost of the following configurations (including €1 share
of server fixed cost):

* 2 Full Xeon Threads - 2 GB RAM - 40 GB SSD : €16.50
* 1 Full Xeon Thread - 1 GB RAM - 10 GB SSD : €6.75
* 1/4th Xeon Thread - 1 GB RAM - 5 GB SSD : €3.40
* 1/8th Xeon Thread - 512 MB RAM - 1 GB SSD : €1.90


Interpretation
--------------

These hardware costs look rather aligned with cheapest (Digital Ocean)
VMs prices. On the other hand, public cloud leaders (Rackspace and
Amazon) are much more expensive.

So should Virtual Machines be cheaper than equivalent dedicated
servers ? Well, this is possible when virtualization allows sharing a
certain amount of fixed costs among users of the same hardware.
According to the previous regression analysis (and hardware
considered), these fixed costs account for roughly €30 / month per
server. Therefore, for low end VMs from some Euros to tens of Euros,
fixed costs sharing looks meaningful. On the other hand, high end VMs
are costly and don't allow many users to share the same server. In
that case, there is no real cost advantage in choosing a VM instead of
a dedicated server in a 24H / 24 7D / 7 usage scenario. However, for
ephemeral usage, high end virtual machines may make sense. Besides,
SSD storage (which is recommended when sharing a disk with many users)
is costly. Therefore, in the case of huge storage space requirements,
dedicated servers with big HDDs may be more appropriate.


Annex - Regression Analysis code
--------------------------------

    ::::python
    #!/usr/bin/env python

    import numpy

    X = numpy.matrix(
    '1,  8,  64,   4,    0;'
    '1, 12, 128,   4,    0;'
    '1, 32, 128,   4,    0;'
    '1, 40, 256,   4,    0;'
    '1,  8,  32,   6,    0;'
    '1, 12,  64,   6,    0;'
    '1, 16, 128,   6,    0;'
    '1, 32, 128,   6,    0;'
    '1, 40, 256,   6,    0;'
    '1, 12,  48,  48,    0;'
    '1, 12,  48,  72,    0;'
    '1, 24,  64, 144,    0;'
    '1, 24,  64, 216,    0;'
    '1, 12,  48,  36,  360;'
    '1, 12,  48,  54,  360;'
    '1, 24,  64, 108, 1080;'
    '1, 24,  64, 162, 1080')

    Y = numpy.matrix(
    '  81.99;'
    ' 131.99;'
    ' 202.99;'
    ' 302.99;'
    '  81.99;'
    ' 141.99;'
    ' 191.99;'
    ' 302.99;'
    ' 402.99;'
    ' 372.99;'
    ' 522.00;'
    ' 822.00;'
    '1272.00;'
    ' 372.99;'
    ' 522.00;'
    ' 822.00;'
    '1272.00')

    # Computing model parameters
    B = (X.T*X).I * X.T * Y

    # Computing predictions based on models
    F = X * B

    # Computing R^2
    M = Y.mean(0).item(0)
    SStot = numpy.multiply(Y-M, Y-M).sum()
    SSres = numpy.multiply(Y-F, Y-F).sum()
    Rsq = 1 - SSres / SStot

    print "Constant:", B.item(0,0)
    print "Eur / CPU thread:", B.item(1,0)
    print "Eur / GB of RAM:", B.item(2,0)
    print "Eur / TB of HDD:", B.item(3,0)
    print "Eur / GB of SSD:", B.item(4,0)
    print "R^2:", Rsq



[1]: http://www.kimsufi.com/en/
[2]: http://www.online.net/en/dedicated-server
[3]: https://www.digitalocean.com/pricing/
[4]: http://www.rackspace.com/cloud/public-pricing/
[5]: http://aws.amazon.com/ec2/pricing/
[6]: http://aws.amazon.com/ec2/faqs/
[7]: http://en.wikipedia.org/wiki/Regression_analysis
[8]: http://www.ovh.com/fr/serveurs_dedies/enterprise/