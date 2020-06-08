GenAP2: Galaxy tool management
================
Florian Wuennemann
08/06/2020

# Introduction

This markdown will discuss how to install, manage and remove tools
inside a galaxy app on fac04.

The handling of tools for galaxy on fac04 can be a little bit confusing.
To make things easier, this overview aims to clearly point to the most
important locations and practices when writing or importing galaxy tools
for single-cell research.

# Tool organization inside Galaxy

Galaxy manages the dependencies for all of the tools using conda
internally. You can find the list of dependencies for tools by going
inside a Galaxy web link, clicking on Admin ==\> Manage dependencies.
This will show you a long list of all the tools currently inside Galaxy,
alongside it’s environment path, the different requirements inside the
environment, their version number, the resolver and whether the
requirement was found.

Galaxy is very particular about the naming of the environment, to be
able to find it internally. There are two different scenarios of how
Galaxy wants the environments named.

1)  If your tool only requires a single package to work correctly (only
    1 requirement specified in the tool .xml file), Galaxy wants the
    environment named as the tool with the specific version number in
    the following format. For example, the tool BAM filter, only
    requires ngsutils as a dependency. The environment for the tool BAM
    filter is therefore named: \_\_<ngsutils@0.5.9> and the path is
    specified as
    /<cvmfs/soft.galaxy/v2.1/tool-dependency/_conda/envs/__ngsutils@0.5.9>

2)  In many cases however, our tools will require more than 1 package to
    function. These cases require a bit more involved way of naming the
    environment. Galaxy will require a so called “mulled” environment.
    We will show you below how to create these environments, but first,
    we need to show you how these environments have to be named for
    Galaxy to find them. For each tool with multiple dependencies, you
    will have to create a mulled name, that is based on the package
    names, numbers and importantly, the order in which you specify them.
    Let’s take the tool featureCounts for example, which requires
    subread and samtools as dependencies. The mulled environment name
    for this tool
is:

<!-- end list -->

``` bash
mulled-v1-938544fe20e36df2ea834972e2239b04494d9d46996877294d1f239acd309e33
```

You can create mulled environment names for your tools using the script
“mulled\_name.py” which is included in this github repo.

Let’s go through an example of creating a mulled environment. Let’s say
we wanted to make a galaxy tool for the pseudoalignment algorithm salmon
and we need 3 dependencies (bzip2,salmon,seqtk). We would have to call
the script mulled\_name.py the following way:

``` bash
python mulled_name.py __bzip2@1.0.6 __salmon@0.11.2 __seqtk@1.2
## returns
mulled-v1-0f2791bb260c3b308e9af3187885d5ee7a01e661ddab2623d2e5386ec9448578
```

We can then use this mulled environment name to build our environment.
We will now show you how to create, manage and delete environments.

# Managing tools

## Installing tools

To create an environment that will be usable and visible inside Galaxy,
we need to use the conda from Galaxy to create environments and install
tools. To activate this conda, run the following lines of code inside
your container:

``` bash
cd /cvmfs/soft.galaxy/v2.1/tool-dependency/_conda
source ./bin/activate

## After running this code, your command line should show:  (base) Singularity>
```

**All executions of “conda” below assume, that you have activated the
conda from the Galaxy. If you don’t activate this conda, you will
install environments and packages inside your home or with insufficient
permissions and will run into problems, so make sure to activate the
Galaxy conda\!**

## Single dependency environments

For environments with only 1 dependency, the procedure is very simple.
Let’s take an example of a tool that only requires regex as it’s
depdency. We can create an environment for this tool using the following
command:

``` bash
conda create --prefix /cvmfs/soft.galaxy/v2.1/tool-dependency/_conda/envs/__regex@2020.4.4  regex=2020.4.4 --channel conda-forge
```

## Mulled environments (multiple dependencies)

Let’s continue with our example above for the tools salmon. To create
the mulled environment name, we can run the following
code:

``` bash
conda create --prefix /cvmfs/soft.galaxy/v2.1/tool-dependency/_conda/envs/mulled-v1-0f2791bb260c3b308e9af3187885d5ee7a01e661ddab2623d2e5386ec9448578 bzip2=3.4.1 --channel anaconda
```

This will create an environment with the specified name and install the
tool bzip2 version 3.4.1 inside. Now we need to go inside our new
environment and install the rest of the tools. Sometimes, you have to be
careful and pay attention to specific requirements of the tools you
install, as they can override the requirements from programs you
installed earlier. Make sure that you read the installation prompts and
that all of your packages inside your environment are compatible with
each other\!

In the case of salmon, we have to install 2 more tools:

``` bash
## Activate the new mulled environment
conda activate /cvmfs/soft.galaxy/v2.1/tool-dependency/_conda/envs/mulled-v1-0f2791bb260c3b308e9af3187885d5ee7a01e661ddab2623d2e5386ec9448578

conda install salmon=0.11.2 --channel bioconda
conda install seqtk=1.2 --channel bioconda
```

## Removing environment

To permanently delete a conda environment, follow the steps below.
Attention, this action cannot be reversed, so only continue if you are
sure, that you do not need the environment anymore.

``` bash
## Example of an environment I had to remove 
conda env remove --name mulled-v1-f15f2990922649e8d475c29369a096c6a0404769bf8aaaeaa6b402f5fd3657eb ## replace this name by the environment name you want to remove
```
