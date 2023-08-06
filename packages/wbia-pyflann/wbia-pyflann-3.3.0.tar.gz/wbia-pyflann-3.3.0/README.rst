=====================
Wildbook IA - PyFlann
=====================

|Build| |Pypi| |ReadTheDocs|

FLANN - Fast Library for Approximate Nearest Neighbors! - Part of the WildMe / Wildbook IA Project.

This is a Fork of the FLANN repo, under a different name for use in the Wildbook
project. The main difference is that it has a few more helper function calls
and it should be easier build wheels and to pip install.

FLANN is a library for performing fast approximate nearest neighbor searches in high dimensional spaces. It contains a collection of algorithms we found to work best for nearest neighbor search and a system for automatically choosing the best algorithm and optimum parameters depending on the dataset.
FLANN is written in C++ and contains bindings for the following languages: C, MATLAB, Python, and Ruby.


Documentation
-------------

Check FLANN web page [here](http://www.cs.ubc.ca/research/flann).

Documentation on how to use the library can be found in the doc/manual.pdf file included in the release archives.

More information and experimental results can be found in the following paper:

  * Marius Muja and David G. Lowe, "Fast Approximate Nearest Neighbors with Automatic Algorithm Configuration", in International Conference on Computer Vision Theory and Applications (VISAPP'09), 2009 [(PDF)](http://people.cs.ubc.ca/~mariusm/uploads/FLANN/flann_visapp09.pdf) [(BibTex)](http://people.cs.ubc.ca/~mariusm/index.php/FLANN/BibTex)


Getting FLANN
-------------

If you want to try out the latest changes or contribute to FLANN, then it's recommended that you checkout the git source repository: `git clone git://github.com/mariusmuja/flann.git`

If you just want to browse the repository, you can do so by going [here](https://github.com/mariusmuja/flann).


Build and Installation
----------------------

This package requires the following system dependencies:

 - lz4 (in debian as liblz4)
 - pkg-config (in debian as pkg-config)
 - gcc (use build-essential in debian)

For development use the ``run_develop_setup.sh`` script.

Conditions of use
-----------------

FLANN is distributed under the terms of the [BSD License](https://github.com/mariusmuja/flann/blob/master/COPYING).


.. |Build| image:: https://img.shields.io/github/workflow/status/WildbookOrg/wbia-tpl-pyflann/Build%20and%20upload%20to%20PyPI/master
    :target: https://github.com/WildbookOrg/wbia-tpl-pyflann/actions?query=branch%3Amaster+workflow%3A%22Build+and+upload+to+PyPI%22
    :alt: Build and upload to PyPI (master)

.. |Pypi| image:: https://img.shields.io/pypi/v/wbia-pyflann.svg
   :target: https://pypi.python.org/pypi/wbia-pyflann
   :alt: Latest PyPI version

.. |ReadTheDocs| image:: https://readthedocs.org/projects/wbia-tpl-pyflann/badge/?version=latest
    :target: http://wbia-tpl-pyflann.readthedocs.io/en/latest/
    :alt: Documentation on ReadTheDocs
