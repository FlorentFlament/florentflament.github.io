Title: Chef Server on Raspberry Pi
Date: 2014-03-03
Tags: Chef, Raspberry Pi, Raspbian

[Raspberry Pi][4] devices are cheap, quiet, and powerful enough to run
a Debian based Linux Operating System called [Raspbian][5]. Such
device would be very convenient to manage one's personal
infrastructure, composed of some physical and / or virtual machines,
by running Chef Server.

While, the official Chef website mostly documents [the installation of
Chef Server on Ubuntu and (Red Hat) Enterprise Linux][1], Chef Server
is available through its API and already packaged for Raspbian as
package `chef-server-api`.

The installation of Chef Server on a Raspberry Pi is therefore quite
forward. The steps to follow, that are described below, are somehow
inspired from these [instructions to have Chef Server installed on
Debian using binary packages][2].

Installation procedure
----------------------

* Start from a fresh installation of Raspbian on a Raspberry Pi. From
NOOBS menu, install Raspbian (Using NOOBS v1.2.1).

* Install Chef Server binary package:

        ::::bash
        $ sudo apt-get update
        $ sudo apt-get install chef-server-api

* Configure Chef Server, by answering to the two questions that will
  be asked:

    * URL of Chef server: http://CHEF_SERVER_IP:4000
    * Chef AMQP user password: RANDOM_PASSWORD (Avoid using special
      characters)

Note: Some services won't start, like jetty. `chef-server` will also
be said to have failed, but Chef Server APIs will be working anyway.

* Testing:

        ::::text
        root@raspberrypi:~# knife configure -i
        WARNING: No knife configuration file found
        Where should I put the config file? [/root/.chef/knife.rb] 
        Please enter the chef server URL: [http://raspberrypi:4000] http://CHEF_SERVER_IP:4000
        Please enter a clientname for the new client: [pi] root
        Please enter the existing admin clientname: [chef-webui] 
        Please enter the location of the existing admin client's private key: [/etc/chef/webui.pem] 
        Please enter the validation clientname: [chef-validator] 
        Please enter the location of the validation key: [/etc/chef/validation.pem] 
        Please enter the path to a chef repository (or leave blank): 
        Creating initial API user...
        Created client[root]
        Configuration file written to /root/.chef/knife.rb
        root@raspberrypi:~# knife client list
          chef-validator
          chef-webui
          root
        root@raspberrypi:~# 

Update of 2014/03/03
--------------------

Note that I hit the bug [Rabbitmq does not appear to get configured
when installing chef-server via deb packages][6]. I got errors when
launching commands `knife client create` or `knife client reregister`,
with following message in `rabbitmq` log:

    ::::text
    =ERROR REPORT==== 4-Jun-2012::14:56:01 ===
    exception on TCP connection <0.583.0> from 127.0.0.1:34143
    {channel0_error,starting,
        {amqp_error,access_refused,
            "AMQPLAIN login refused: user 'chef' - invalid credentials",
            'connection.start_ok'}}


Fix consists in executing the following commands:

    ::::bash
    $ sudo rabbitmqctl add_vhost /chef
    $ sudo rabbitmqctl add_user chef PASSWORD_PER_CONFIGURATION
    $ sudo rabbitmqctl set_permissions -p /chef chef ".*" ".*" ".*"


[1]: http://www.getchef.com/chef/install/#tab2
[2]: http://www.cschramm.net/howtos/installing-chef-server-debian/
[3]: https://github.com/opscode/chef
[4]: http://www.raspberrypi.org/
[5]: http://www.raspbian.org/
[6]: https://tickets.opscode.com/browse/CHEF-3170