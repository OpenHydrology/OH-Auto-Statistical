Installation
============

Windows
-------

To install OH Auto Statistical, simply download and run the installer.

   Download OH Auto Statistical for Windows:

   .. image:: https://img.shields.io/github/release/openhydrology/oh-auto-statistical.svg?style=flat-square
      :target: https://github.com/OpenHydrology/OH-Auto-Statistical/releases/latest

An internet connection is required during the installation process.

.. note::
   During the installation process, a complete set of gauged catchment data will be downloaded from the
   `National River Flow Archive (NRFA) <http://www.ceh.ac.uk/data/nrfa/>`_ for pooled analyses. This may take some time!
   NRFA data are subject to `terms and conditions <http://www.ceh.ac.uk/data/nrfa/data/data_terms.html>`_.


.. attention::

   No Windows Start Menu items are created, except for a link to the online documentation. This is intentionally. OH
   Auto Statistical is run by **right-clicking on a .CD3-file**.


Mac OS and Linux
----------------

OH Auto Statistical can be installed on Mac OS and Linux operating systems from binstar.org using the `Conda package
manager <http://conda.pydata.org/miniconda.html>`_:

   .. image:: https://binstar.org/openhydrology/autostatistical/badges/version.svg
      :target: https://binstar.org/openhydrology/autostatistical

.. code-block:: shell

   conda install -c https://conda.binstar.org/openhydrology autostatistical

Or alternatively directly from the source code:

   .. image:: https://img.shields.io/github/release/openhydrology/oh-auto-statistical.svg?style=flat-square
      :target: https://github.com/OpenHydrology/OH-Auto-Statistical/releases/latest



OH Auto Statistical is run as follows:

.. code-block:: shell

   python -m autostatistical "path/to/catchment.cd3"