---
title: Setting up Python for EEG analysis
date: 2017-10-09T00:00:00+00:00
summary: Installing Python is usually pretty straightforward, but there are some gotchas when setting up Python for scientific computing. In this post, I describe pros and cons of various installation methods (and recommend one particular option for EEG analysis).
tags:
  - Python
  - EEG
aliases:
  - 2017-10-09-setting-up-python
---

## Installing Python
There are several ways to install a Python environment on your computer. For example, the most obvious way involves downloading an installer from the [official Python website](https://www.python.org/). Official installers are available for Windows and macOS. Most Linux distributions include Python out of the box (if not you can use the package manager to quickly set up a working Python environment). While this option works in many situations, obtaining additional Python packages for scientific computing might not be particularly convenient for beginners.

An alternative available on macOS is the package manager [Homebrew](https://brew.sh/). Although this is my preferred way of installing Python on a Mac, I will not describe it in detail here (other than mention that running `brew install python` in a terminal is all it takes).

While Python is relatively easy to set up, installing additional packages sometimes involves compiling source code. This means that you need to have a working build toolchain on your machine, which is standard on Linux systems, relatively straightforward on macOS, but a bit more challenging on Windows.

This is where Python distributions come in handy &ndash; they bundle Python with additional pre-built packages, which means that compiling is not necessary. One of the most popular Python distributions (at least in the scientific community) seems to be [Anaconda](https://www.anaconda.com/distribution/), which includes [hundreds of useful Python packages](https://anaconda.org/anaconda/repo). Among the most notable features are versions of [NumPy](http://www.numpy.org/), [SciPy](https://www.scipy.org/scipylib/index.html), and [Scikit-learn](http://scikit-learn.org/stable/) with [Intel Math Kernel Library (MKL)](https://software.intel.com/mkl) support. This basically means that if you have an Intel CPU many computations will be faster than with standard versions of these packages (although in my experience [OpenBLAS](https://www.openblas.net) is just as fast and also runs on AMD CPUs).

Installing Anaconda is as easy as downloading and running the [installer](https://www.anaconda.com/distribution/) for your operating system. After that, you are all set.

If you do not want to install dozens of packages that come with Anaconda (for example because you want to save precious disk space), you can install its barebones sibling called [Miniconda](https://conda.io/miniconda.html). Just know that you will need to install (almost) all additional packages manually via the `conda` package manager.

## Installing additional packages
Although Python comes with an extensive [standard library](https://docs.python.org/3/library/index.html), most scientific packages are not part of Python itself. Luckily, installing additional Python packages is not difficult. If you use Anaconda or Miniconda, you can leverage the `conda` command line tool to manage Python packages. Open a terminal (sometimes also called a command line) to use the tool.

The first step is to find out if a particular package is available in the Anaconda repository (replace `<package>` with the actual name of the package):

```
conda search <package>
```

If the package is available (meaning that the previous command returned a match), here's how you can install it:

```
conda install <package>
```

For example, if you are planning to do EEG analysis, chances are that you will be using [MNE](https://mne.tools). Let's see if a package called `mne` is available in Anaconda:

```
conda search mne
```

Unfortunately, the search returns no matches (meaning that MNE is not available in Anaconda), so we need to use another method to install it. The standard way to go about this is to use the official Python package manager `pip` for packages that are not available with `conda`. The `pip` command line tool searches the [Python Packaging Index (PyPI)](https://pypi.python.org/pypi), which is the central repository for third-party Python packages.

Here's how you can search for the `mne` package:

```
pip search mne
```

This command spits out several matches, including a package called `mne`. We can install the package as follows:

```
pip install mne
```

That's all there's to it. Just remember to use `conda` to search and install a package first, because Anaconda packages are often optimized and tested to work well in combination with other Anaconda packages. If a package is not available in Anaconda, use `pip` to install it. If you do not use Anaconda/Miniconda, you can only use `pip` anyway.

## Recommended scientific packages
Here are some useful packages that I recommend if you want to use Python for scientific computing in general and EEG processing in particular (use `conda` and/or `pip` to install them):

- [NumPy](http://www.numpy.org/) provides a multi-dimensional array data type; it is the basis for almost all scientific packages.
- [SciPy](https://www.scipy.org/scipylib/index.html) contains a large number of various algorithms used in scientific computing.
- [Pandas](http://pandas.pydata.org/) extends the NumPy array and provides a more flexible data frame type similar to the one found in [R](https://www.r-project.org/).
- [Matplotlib](https://matplotlib.org/) is the most popular package to create all kinds of plots in Python.
- [IPython](https://ipython.org/) is an enhanced interactive Python shell.
- [Scikit-learn](http://scikit-learn.org/stable/) is a powerful machine learning package for Python.
- [MNE](http://martinos.org/mne/stable/index.html) is a package for EEG/MEG processing.
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) provides Python bindings for the [Qt GUI toolkit](https://www.qt.io/).

## Keeping everything up to date
It is generally a good idea to use the most recent version of Python. In addition, you probably also want to keep all installed packages up to date. If you use Anaconda, you can update all installed packages with:

```
conda update --all
```

Packages installed via `pip` cannot be updated with `conda`. However, you can use `pip` to get a list of outdated packages:

```
pip list --outdated
```

This list might also include packages installed via `conda` (in general, `pip` offers the latest versions before they get into Anaconda/Miniconda). You can keep track of packages installed via `pip` by inspecting the rightmost "Channel" column of the output of `conda list`. If it says "pypi" then you can (and should) only update this package using `pip`:

```
pip install -U <package>
```

If you do not use Anaconda (or Miniconda), you have to use `pip` to find and update all outdated packages. Unfortunately, there is no built-in flag to update all outdated packages at once. You can either update each package individually or use any of the numerous methods mentioned in this [StackOverflow post](https://stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip).

Finally, feel free to install as many packages as you like. After all, Python makes it easy and fun to try out stuff that others have already implemented so that you don't have to! If you decide later on that you do not need a specific package, you can completely remove it with either `conda` or `pip` (depending on how you installed it):

```
conda uninstall <package>
```

```
pip uninstall <package>
```