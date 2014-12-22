Installation
============

Windows
-------

 1. `Download <https://github.com/OpenHydrology/OH-Auto-Statistical/releases>`_ and run the OH Auto Statistical
    installer.
 2. This will first run the Miniconda Python package manager. All options can be left to their defaults.
 3. Next the required Python packages are installed. This requires an internet connection.

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