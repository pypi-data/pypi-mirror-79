# pyproteome

[![Build Status](https://img.shields.io/travis/white-lab/pyproteome.svg)](https://travis-ci.org/white-lab/pyproteome)
[![Coverage Status](https://img.shields.io/coveralls/white-lab/pyproteome.svg)](https://coveralls.io/r/white-lab/pyproteome?branch=master)
[![Documentation Status](https://readthedocs.org/projects/pyproteome/badge/?version=latest)](https://pyproteome.readthedocs.io/en/latest/)
[![Requirements Status](https://requires.io/github/white-lab/pyproteome/requirements.svg?branch=master)](https://requires.io/github/white-lab/pyproteome/requirements/?branch=master)
[![PyPI](https://img.shields.io/pypi/v/pyproteome.svg)](https://pypi.python.org/pypi/pyproteome)


Python library for analyzing mass spectrometry proteomics data.

## Installation

To install the core pyproteome python library, [install Python >= 3.6](https://www.python.org/) and [the latest version of pip](https://pip.pypa.io/en/stable/installing/). Then run the following command:

```
pip install pyproteome
```

To install dependencies for [PHOTON](https://github.com/jdrudolph/photon), run the following command:

```
pip install pyproteome[photon]
```

### Windows

If you are using Windows, it is easiest to use the latest version of
[Anaconda](https://www.continuum.io/downloads) for your Python installation, as
pyproteome requires several hard-to-install packages, such as NumPy and SciPy.

Then, you can simply run the above `pip install pyproteome` command to install
this package and the rest of its dependencies.

### CAMV

pyproteome can use CAMV for data validation. If you have the executable
installed on your system, simply add "CAMV.exe" to your system path and
pyproteome will locate it automatically.

## Examples

There are several example analyses located in the [pyproteome-data
repository](https://github.com/white-lab/pyproteome-data/tree/master/examples).

For a full list of package functionality, refer to the
[online documentation](https://pyproteome.readthedocs.io/en/latest/).

## Directory Hierarchy

pyproteome expects a certain directory hierarchy in order to import data files
and interface with CAMV. This pattern is as follows:

```
base_directory/
    CAMV Output/
    Figures/
    MS RAW/
    Searched/
```

See `pyproteome.paths` if you are using a custom directory hierarchy. i.e.:

```
>>> from pyproteome import paths
>>> paths.MS_RAW_DIR = "path/to/raw_files/"
>>> paths.MS_SEARCHED_DIR = "path/to/msf_files/"
```
