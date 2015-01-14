Installation
============

Windows
-------

`Download <https://github.com/OpenHydrology/OH-Auto-Statistical/releases/latest>`_ and run the OH Auto Statistical
installer. An internet connection is required during the installation process.

.. note::
   During the installation process, a complete set of gauged catchment data will be downloaded from the
   `National River Flow Archive (NRFA) <http://www.ceh.ac.uk/data/nrfa/>`_ for pooled analyses. This may take some time!
   NRFA data are subject to `terms and conditions <http://www.ceh.ac.uk/data/nrfa/data/data_terms.html>`_.


.. attention::

   No Windows Start Menu items are created, except for a link to the online documentation. This is intentionally. OH
   Auto Statistical is run by **right-clicking on a .CD3-file**.

Alternatively, if a Python (>=3.3) installation including the packages `numpy` and `scipy` already exists, OH Auto
Statistical can be installed from the `Python Package Index <https://pypi.python.org/pypi/autostatistical>`_.

Other operation systems
-----------------------

There are many ways to install OH Auto Statistical on Linux and Mac operating systems. OH Auto Statistical requires the
following Python packages:

 - numpy
 - scipy
 - sqlalchemy
 - appdirs
 - lmoments3
 - floodestimation
 - Jinja2
 - autostatistical

The `Miniconda Python package manager <http://conda.pydata.org/miniconda.html>`_ is available for all major operation
systems and can be used to install packages suchs as `numpy` and `scipy`.

OH Auto Statistical is run as follows:

.. code-block:: shell

   python -m autostatistical "path/to/catchment.cd3"