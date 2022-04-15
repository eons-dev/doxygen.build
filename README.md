# EBBS Doxygen Builder

In order to make compiling Doxygen comments easier and prevent cluttering your repo with documentation configuration files, we provide this EBBS build script. To use this, you'll need to store your style and configuration files in another repo or directory. You may specify a style to download from the Infrastructure repository with `--style my-style-to-download`. If `--style` is not specified, we'll try to use the current directory.

This script supports all project types.

Prerequisites:
* Doxygen (including flex and bison)

Suggested Prerequisites:
* graphviz
* pdf2svg

## Configuration

`--style` : the style to download.
`--doxygen_conf` : the name of the doxygen configuration file; "doxygen.conf" by default.

No configuration is available at this time. In a future release, we will be supporting overriding doxygen configuration tags.

You can also set up a multi-stage build pipeline with "ebbs_next". See [ebbs](https://github.com/eons-dev/bin_ebbs) for more info.
For an example, check out the [infrastructure.tech web server](https://github.com/infrastructure-tech/srv_infrastructure)