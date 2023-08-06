========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/cuimage/badge/?style=flat
    :target: https://readthedocs.org/projects/cuimage
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/gigony/cuimage.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/gigony/cuimage

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/gigony/cuimage?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/gigony/cuimage

.. |requires| image:: https://requires.io/github/gigony/cuimage/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/gigony/cuimage/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/gigony/cuimage/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/gigony/cuimage

.. |version| image:: https://img.shields.io/pypi/v/cuimage.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/cuimage

.. |wheel| image:: https://img.shields.io/pypi/wheel/cuimage.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/cuimage

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/cuimage.svg
    :alt: Supported versions
    :target: https://pypi.org/project/cuimage

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/cuimage.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/cuimage

.. |commits-since| image:: https://img.shields.io/github/commits-since/gigony/cuimage/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/gigony/cuimage/compare/v0.0.0...master



.. end-badges

A CUDA-accerlated image processing library

* Free software: Apache Software License 2.0

Installation
============

::

    pip install cuimage

You can also install the in-development version with::

    pip install https://github.com/gigony/cuimage/archive/master.zip


Documentation
=============


https://cuimage.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
