Title: Git SSH Docker container
Date: 2014-06-28
Tags: Git, SSH, Docker

My favorite option to backup and version my code and text files is
using git with a remote repository. The implementation I have chosen
for that consists in running an ssh server, with git, in a Docker
container. This has the following advantages over other solutions:

* 100% reproducible;
* Limits access to the container in case the account is compromised;
* Consumes less resources that running a VM.


Dockerfile
----------

The proposed Git SSH Dockerfile is based on the [Dockerizing an SSH
service][1] example.

    ::::bash
    FROM ubuntu:14.04

    RUN apt-get -y update
    RUN apt-get -y install openssh-server
    RUN apt-get -y install git

    # Setting openssh
    RUN mkdir /var/run/sshd
    RUN sed -i "s/#PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config

    # Adding git user
    RUN adduser --system git
    RUN mkdir -p /home/git/.ssh

    # Clearing and setting authorized ssh keys
    RUN echo '' > /home/git/.ssh/authorized_keys
    RUN echo 'First SSH public key' >> /home/git/.ssh/authorized_keys
    RUN echo 'Second SSH public key' >> /home/git/.ssh/authorized_keys
    # ...
    
    # Updating shell to bash
    RUN sed -i s#/home/git:/bin/false#/home/git:/bin/bash# /etc/passwd

    EXPOSE 22
    CMD ["/usr/sbin/sshd", "-D"]


Running the container
---------------------
    
* Building the image

        ::::bash
        $ docker.io build -t git-ssh_img .

* Running the image

        ::::bash
        $ sudo docker.io run -p 1234:22 -d --name git-ssh git-ssh_img

The previous command maps the container's host port 1234 on the
container's SSH port. Of course, this port can be changed to any
value. One can then ssh to the container with the following command:

    ::::bash
    $ ssh -p 1234 git@<container_host>


[1]: https://docs.docker.com/examples/running_ssh_service/
