Title: ZNC in Docker container
Date: 2013-12-15
Tags: ZNC, Docker, IRC

[ZNC][1] is a popular IRC bouncer, which stays connected to IRC
channels and log conversations while one isn't connected. This note
desrcibes how to launch ZNC in a [Docker][2] container, so that it be
launched on any Docker enabled platform. To quick start with Docker,
one can follow the steps proposed to [install Docker on an Ubuntu
Linux][3] (for instance in a VM).

Using ZNC setup wizard
----------------------

Once Docker is installed on the system, we can prepare an image that
will be used to run ZNC with the following `Dockerfile` (Docker
configuration file):

    ::::text
    FROM ubuntu:precise
    MAINTAINER Florent Flament

    # Using fr ubuntu mirrors and adding universe repository, to install znc
    RUN echo "deb http://fr.archive.ubuntu.com/ubuntu precise main restricted" \
    > /etc/apt/sources.list
    RUN echo "deb http://fr.archive.ubuntu.com/ubuntu precise universe" \
    >> /etc/apt/sources.list

    # Installing znc package
    RUN apt-get -y update
    RUN apt-get -y install znc

    # Creating directory to store znc configuration
    RUN mkdir -m 775 /var/znc
    RUN chgrp daemon /var/znc
    USER daemon

Let's assume that the `Dockerfile` is stored in the `znc-noconf`
directory. We can build the ZNC ready image with the following
command:

    ::::bash
    $ docker build -t znc:noconf znc-noconf/

The next step is to configure ZNC. The following command will run the
configuration wizard in a new container based on the previously
generated image:

    ::::bash
    $ docker run -i -t znc:noconf -d /var/znc -c

After having answered to all the questions, ZNC will generate its
configuration files. It will then be ready to run in daemon mode. Now
we can save a Docker image including ZNC's configuration files.

    ::::bash
    $ CONT=$(docker ps -a | grep "minutes ago" | head -1 | awk '{print $1}')
    $ docker commit \
    > -run='{"Cmd": ["/usr/bin/znc", "-f", "-d", "/var/znc/"], "User": "daemon"}' \
    > $CONT znc:ready

The ZNC image is now ready, and can be launched. In addition to launch
ZNC in a new container, the following command will map the host's 6697
TCP port on the container's 6697 port (assuming that ZNC has been
configured to listen to port 6697).

    ::::bash
    $ docker run -d -p 6697:6697 znc:ready


Using a previously made ZNC configuration file
----------------------------------------------

One can setup a ZNC Docker container even quicker if he already has a
`znc.conf` configuration file. One has to create a directory (for
instance `myznc/`) containing both: `znc.conf` and a `Dockerfile`, with
the following content:

    ::::text
    FROM ubuntu:precise
    MAINTAINER Florent Flament

    # Using fr ubuntu mirrors and adding universe repository, to install znc
    RUN echo "deb http://fr.archive.ubuntu.com/ubuntu precise main restricted" \
    > /etc/apt/sources.list
    RUN echo "deb http://fr.archive.ubuntu.com/ubuntu precise universe" \
    >> /etc/apt/sources.list

    # Installing znc package
    RUN apt-get -y update
    RUN apt-get -y install znc

    # Creating directory to store znc configuration
    RUN mkdir -m 775 /var/znc
    # Generates key for SSL exchanges
    RUN /usr/bin/znc -d /var/znc -p
    # Copies ZNC configuration file
    ADD znc.conf /var/znc/configs/
    RUN chown -R daemon:daemon /var/znc
    USER daemon

    # Setting default container's command
    CMD ["/usr/bin/znc", "-f", "-d", "/var/znc/"]

Then the ZNC container can be launched right after having built the image:

    ::::bash
    $ docker build -t znc:myznc myznc/
    $ docker run -d -p 6697:6697 znc:myznc

[1]: http://wiki.znc.in/ZNC
[2]: https://www.docker.io/
[3]: http://docs.docker.io/en/latest/installation/ubuntulinux/