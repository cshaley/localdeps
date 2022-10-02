# conda-dev: Usage

Conda-dev is meant to be used as an easy way to install all dependencies of a conda package in development into a conda environment.

For example, let's say I'm developing a package named `mypackage`, and I want to package it as a conda package so other developers can `conda install mypackage`.  The prescribed path to do this in the open source world is to publish as a package on pypi and then to create a feedstock using conda forge to publish the conda package.

If I'm working on closed source packages, I may need to build a conda package without publishing as a pypi package first.  Here's the problem: conda does not provide a way to install a package or its dependencies listed in meta.yaml in a development environment the same way that pip does, so it becomes difficult to automate development environment setup.

So here comes conda-dev to the rescue:

```
conda-dev --conda-dir conda.recipe --env my-dev-env
pip install -e . --no-deps --no-build-isolation
```

Now, I only need one copy of the dependencies of my conda package (meta.yaml), and I can develop the code and have changes instantly take effect in the active environment.


## Installation

`conda install conda-dev -c conda-forge`

Note: This is not available via `pip install` because it depends on conda and conda-build, which are not available via pip.
