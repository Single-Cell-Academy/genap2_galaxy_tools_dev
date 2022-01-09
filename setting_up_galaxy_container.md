Setting up Galaxy container for developing tools
================
FlorianW
02/03/2020

# Setting up a galaxy container

## Introduction

This markdown will exaplain how to setup and connec to the VM for
developing single-cell Galaxy tools for GenAP2. In February 2020, the
GenAP2 team changed the general architecture of how the Galaxy image was
organized. This directly changed the paths for developing and
implementing single-cell tools for Galaxy.

## 1) Connecting to FAC04

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

## 2) Instantiate your Galaxy docker container

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
## Service connected on:
https://wueflo00-galaxy2.proxy-east01.genap.ca
```

To destroy the container, run the following code:

``` bash
## To clean
genapproxy destroy --app=galaxy --path=$data_path --conf=/nfs3_ib/ip24/home.local/barrette.share/singproxy/conf/jonathan_tool_mike.conf

## Another way to stop the container is the following method:
singularity instance stop galaxy
```

## 3) Enter the container and check data structures

To find out your container id, run the following code in the shell:

``` bash
singularity instance list
```

This will return a list with running instances to you. Copy the name of
your instance and then run the following to enter the container. In this
example, the container id is galaxy322

``` bash
singularity exec instance://galaxy2 bash
```

There are mainly 4 folders inside the container that are important

**1) /etc/galaxy**

This is where the main config is (galaxy.yml)

**2) /cvmfs/soft.galaxy/v2.1/**

That’s is where Galaxy reads most of it contents. I modified Galaxy to
“ignore” most of what is installed inside the container and use what is
in /cvmfs/

**3) /galaxy-central/**

This is where all Galaxy files, configs and libs are. This is the main
Galaxy dir

**4) /export/galaxy-central/**

This is the dir that Galaxy mount in the job node. Be aware that tools/
and config/ are there as well (they are a copy of the one in
/galaxy-central/, so keep them synchronized)

## 4) Create a single-cell tool config file

To add our single-cell tools to the main galaxy, we need to create a
config file specifically for single-cell tools. Create a file in the
following directory

``` bash
nano /cvmfs/soft.galaxy/v2.1/server/config/tool_SC_config.xml
```

and enter the following template code:

``` bash
<?xml version='1.0' encoding='utf-8'?>
<toolbox monitor="true">
  <section id="testing" name="Test section">
  </section>
</toolbox>
```

Add the single-cell config file as well as the data table config file to
the tool config file:

``` bash
nano /etc/galaxy/galaxy.yml

## Add the cvmfs tool folder as the default tool dir
tool_path:  /cvmfs/soft.galaxy/v2.1/server/tools

## find tool_config_file in the file and add:
# tool_config_file
/cvmfs/soft.galaxy/v2.1/server/config/tool_SC_config.xml

## Table for references
## find: tool_data_table_config_path in the file and add 
# tool_data_table_config_path
/cvmfs/soft.galaxy/v2.1/server/tools/single_cell_tools/tool_data_table_config.xml

## .loc files for single-cell references can be found here:
/cvmfs/soft.galaxy/v2.1/server/tools/single_cell_tools/refs/data_tables
```

After adding and modifying these files, restart the galaxy:

``` bash
## Restart galaxy from within container
supervisorctl restart galaxy:
```

## Error logs

In case the Galaxy does not work, the error logs can be found under:

``` bash
## File containing error reports
/var/log/galaxy/uwsgi.log

## To surveil erors live
tail -f /var/log/galaxy/uwsgi.log
```

## Log rotation

This is an important final step of setting up the container. We need to
enable log rotation, otherwise error logs can clog the system and create
problems for other users containers.

In your /etc/galaxy/galaxy/yml search for the following option and
uncomment.

``` bash
nano /etc/galaxy/galaxy.yml

## Set log_level: ERROR
```

Afterward, we have to create a file called /etc/logrotate.d/galaxy and
insert the following code:

``` bash
## /etc/logrotate.d/
/var/log/galaxy/*.log {
   daily
   rotate 14
   copytruncate
   compress
   missingok
   notifempty
}
```

## Reseting configs after destroying and recreating a galaxy

If you recently destroyed your galaxy app but saved your config files
beforehand, you can simply copy paste these files above the defaults and
basically recreate all of your previous settings. If your config files
are in your home folder under /galaxy\_config\_backup. Run these
commands:

``` bash
## Galaxy yaml config file
cp galaxy.yml /etc/galaxy

# log rotation file
cp galaxy /etc/logrotate.d/
```

## Useful alias for fac04

``` bash
## app creation alias
alias genapproxy=/nfs3_ib/ip24/home.local/barrette.share/singproxy-slurm/singproxy

## Enter singularity container
alias enter_galaxy="singularity exec instance://galaxy2 bash"

## Restart singularity container
alias restart_galaxy="supervisorctl restart galaxy:"

## Go to location of tool_conf.xml
alias to_conf="cd /cvmfs/soft.galaxy/v2.1/server/config"

## Go to tools
alias to_tools="cd /cvmfs/soft.galaxy/v2.1/server/tools"

## Listen to error report
alias listen_to_errors="tail -f /var/log/galaxy/uwsgi.log"

## Show singularity instances
alias show_instances="singularity instance list"
```

## Troubleshooting

In case the Galaxy app returns a spawn error when trying to restart
using the following command:
