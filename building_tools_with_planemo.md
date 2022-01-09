Building a galaxy tool with planemo
================
Florian Wuennemann
12/11/2020

In this tutorial, I will describe how to construct a galaxy tool wrapper
for a local galaxy installation from beginning to end.

This walkthrough assumes you are using a local Galaxy via a Docker
container from
[galaxy-docker-stable](https://github.com/bgruening/docker-galaxy-stable).
For this particular example, I am running [version
20.05](https://github.com/bgruening/docker-galaxy-stable/releases/tag/20.05)
of the container on Ubuntu 20.04.1 LTS.

The tool we will create is going to be a wrapper for the R package
[alevinQC](http://www.bioconductor.org/packages/release/bioc/html/alevinQC.html),
which can be used to produce QC reports for runs of salmon-alevin. At
the time of writing, no galaxy tool was available on galaxy toolshed and
therefore I thought it was a good place to start with a fresh tool.

[Planemo tutorial
website](https://planemo.readthedocs.io/en/latest/writing_standalone.html)

# Galaxy dev mailing list

<https://lists.galaxyproject.org/user-profile/>

## Example run of alevinQC

Since alevinQC is an R package, here is a short example of a standard
run. We require the output files from a salmon-alevin run. The package
developers of alevinQC have kindly provided some example output files
with alevinQC. Let’s load them now and check that they are indeed
available:

``` r
library(alevinQC)
baseDir <- system.file("extdata/alevin_example_v0.14", package = "alevinQC")
checkAlevinInputFiles(baseDir = baseDir)
```

A standard run of alevinQC is also given as an example in the tutorial:

``` r
outputDir <- tempdir()
alevinQCReport(baseDir = baseDir, sampleId = "testSample", 
               outputFile = "alevinQCReport.html", 
               outputFormat = "html_document",
               outputDir = ".", forceOverwrite = TRUE, quiet = FALSE)
```

## Setting up tool XML file

The first command we will run is used to setup a very basic template
XML.

``` bash
## More 
planemo tool_init --force \
  --id 'alevinQC_galaxy' \
  --name 'Produce QC reports for salmon-alevin runs'\
  --requirement bioconductor-alevinqc@1.6.0 \
  --example_command ' Rscript alevinQC.R' \
  --test_case \
  --cite_url 'https://github.com/csoneson/alevinQC' \
  --help_from_command 'alevinQC'
```

We can then manually edit the tool to add or remove any necessary
elements.

``` bash
baseDir
  |--alevin
  |    |--featureDump.txt
  |    |--raw_cb_frequency.txt
  |    |--whitelist.txt  (depending on how alevin was run)
  |--aux_info
  |    |--meta_info.json
  |    |--alevin_meta_info.json
  |--cmd_info.json
```

## Preparing submission for tool shed

``` bash
## This only needs to be run once at the very beginning of setting up planemo
planemo config_init
```

``` bash
planemo shed_init --name=alevinqc --owner=fwuennemann --description="AlevinQC produces quality control reports for salmon-alevin runs." --remote_repository_url=https://github.com/Single-Cell-Academy/alevinQC_galaxy --homepage_url=https://bioconductor.org/packages/release/bioc/html/alevinQC.html
```
