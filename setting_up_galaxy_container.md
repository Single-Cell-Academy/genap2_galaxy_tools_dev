Setting up Galaxy container for developing tools
================
FlorianW
02/03/2020

# Introduction

This markdown will exaplain how to setup and connec to the VM for
developing single-cell Galaxy tools for GenAP2. In February 2020, the
GenAP2 team changed the general architecture of how the Galaxy image was
organized. This directly changed the paths for developing and
implementing single-cell tools for Galaxy.

# Setting up a galaxy container

## 1\) Connecting to FAC04

First, we will need to connect to the fac04. To do this, we need to add
the following code to our .ssh/config file. If this file doesn’t exist,
you can manually create it. Add this code in the file

``` bash
host *.m
  ProxyCommand ssh -i  ~/.ssh/id_rsa -W %h:%p %r@206.12.92.5 -p 22004
  IdentityFile ~/.ssh/id_rsa
```

Once Michel has made you an account on fac04 and you have configured
your ssh/config, you can connect like this:

``` bash
ssh wueflo00@fac04.m
```

## 2\) Instantiate your Galaxy docker container

Now we are ready to create our galaxy container. First run the following
commands to define parameters:

``` bash
## Setup some aliases and parameters
alias genapproxy=/nfs3_ib/ip24/home.local/barrette.share/singproxy-slurm/singproxy
data_path=~/test;mkdir $data_path
export GENAP_GALAXY_SOURCE=/nfs3_ib/ip24/home.local/barrette.share/template-singproxy/galaxy2;export PG_VERSION=11
```

Then, to create the container run:

``` bash
## These commands actually create or destroy the singularity container

# To create
genapproxy create --app=galaxy --path=$data_path --conf=/nfs3_ib/ip24/home.local/barrette.share/singproxy/conf/jonathan_tool_mike.conf
```

When the Galaxy container is created, it will automatically add a admin
user and provide the username and password for you. Save these, as you
will need them to login to your Galaxy. Galaxy will also provide a
weblink, that you can use to connect to the galaxy instance. In my
example, the weblink looks like this:

``` bash
https://wueflo00-galaxy1.proxy-east01.genap.ca
```

To destroy the container, run the following code:

``` bash
# To clean
genapproxy destroy --app=galaxy --path=$data_path --conf=/nfs3_ib/ip24/home.local/barrette.share/singproxy/conf/jonathan_tool_mike.conf
```

## 3\) Enter the container and check data structures

To find out your container id, run the following code in the shell:

``` bash
singularity instance list
```

This will return a list with running instances to you. Copy the name of
your instance and then run the following to enter the container. In this
example, the container id is galaxy322

``` bash
singularity exec instance://galaxy1 bash
```

There are mainly 4 folders inside the container that are important

**1) /etc/galaxy**

This is where the main config is (galaxy.yml)

**2) /cvmfs/soft.galaxy/v2.1/**

That’s is where Galaxy reads most of it contents. I modified Galaxy to
“ignore” most of what is installed inside the container and use what
is in /cvmfs/

**3) /galaxy-central/**

This is where all Galaxy files, configs and libs are. This is the main
Galaxy dir

**4) /export/galaxy-central/**

This is the dir that Galaxy mount in the job node. Be aware that tools/
and config/ are there as well (they are a copy of the one in
/galaxy-central/, so keep them synchronized)
