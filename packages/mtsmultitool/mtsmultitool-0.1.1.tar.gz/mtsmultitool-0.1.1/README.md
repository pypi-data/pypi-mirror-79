# MultiTech Multitool Utility

Library and command line tool for working with Multitech products.

# Usage

Command line tool `multitool` has functionality split into subcommands.  To get a list of valid subcommands use `--help`
or `-h`.  Each subcommand can also be queried for details using `--help`.

## Examples

Get help:
```
multitool --help
multitool device --help
multitool device patch --help
```

### Device Subcommand

The `device` command has tools for packaging device firmware upgrades.

Create a patch for an MDot when the images contain bootloaders:
```
multitool device patch -m -v 3.3.6 -d MTDOT -b 0x10000 mdot_image_3.3.6.bin mdot_image_3.3.7.bin
```

Compress an XDot image which does not contain a bootloader and append a CRC32:
```
multitool device compress -m -c -d XDOT xdot_image_3.3.7_application.bin
```

# Installation 
Use PIP to install, the `multitool` executable will be added to the Python scripts directory.

```
pip install mtsmultitool
```

[//]: # (End long description)

From local source:
```
pip install -e . mtsmultitool
```

# Building Distributions

Run the following command to build a source distribution which requires compiling when installed by PIP.

```
python setup.py sdist
```

Run the following command on each platform to build a pre-compiled distribution.  Note the distribution will only be
valid for the python version used.  Separate builds must be created for each version of Python supported, including
32-bit and 64-bit.

```
python setup.py sdist bdist_wheel
```

# Running Tests

Install `tox` with `pip install tox`.

Execute the following command to run tests:
```
tox
```

# Building Documentation

Module and command interface documentation is located in `docs` and is built using [Sphinx](https://www.sphinx-doc.org/en/master/index.html).

Install the `mtsmultitool` package and follow instruction for [installing Sphinx](https://www.sphinx-doc.org/en/master/usage/installation.html).

To build HTML documentation:
```
cd docs
make html
```
