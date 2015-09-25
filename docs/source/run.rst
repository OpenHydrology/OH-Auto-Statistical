Usage
=====

OH Auto Statistical takes a **catchment descriptors (.CD3 or .xml) file as input data**. The analyses are undertaken
without any further user input and a report file is generated containing the calculation details and results.


Ungauged catchments flood estimation
------------------------------------

To undertake an analysis:

1. Export a .CD3 or .xml-file from the `FEH CD-ROM <http://www.hydrosolutions.co.uk/products.asp?categoryID=4670>`_
   and save it somewhere.

2. Start OH Auto Statistical from the Windows Start Menu.

3. Browse to and select the catchment file to run the analysis.

   .. image:: _static/run-analysis.png

4. A report is generated and is saved in the same folder as the catchment file with a file name ending with
   :file:`...Flood estimation report.yyyy-mm-dd.md` [#f1]_. Closing OH Auto Statistical will open the report. Untick the check
   box to close the application without opening the report.

   .. image:: _static/report.png


Gauged catchments flood estimation
----------------------------------

A statistical flood estimation for gauged catchments ("enhanced single site analysis") is undertaken when an .AM file is
saved alongside the catchment file. The files should have the same name (except for the file extension) and be located
in the same folder. The process is otherwise exactly the same as for ungauged catchments.

.. tip::

   .CD3 and .AM files for gauged catchments (as downloaded from the :abbr:`NRFA (National River Flow Archive )`) can be
   found in the cache folder :file:`C:\\Users\\{username}\\AppData\\Local\\Open Hydrology\\fehdata\\Cache` on Windows
   and equivalent locations on other operating systems.


Updating NRFA data
------------------

:abbr:`NRFA (National River Flow Archive )` data are automatically downloaded during the installation of OH Auto
Statistical. Before undertaking an analysis, OH Auto Statistical checks whether an NRFA update is available and will
download this if necessary. All existing data will be removed before downloading a complete new dataset. This may take a
while.


Customising the report template
-------------------------------

The report template can be customised by placing a file :file:`normal.md` in the folder
:file:`C:\\Users\\<username>\\AppData\\Local\\Open Hydrology\\OH Auto Statistical\\templates`.


.. rubric:: Footnotes

.. [#f1] This is a `Markdown (*.md) file <http://daringfireball.net/projects/markdown/>`_ or more precisely a
         `GitHub Flavoured Markdown file <https://help.github.com/articles/github-flavored-markdown/>`_. Markdown files
         are plain text files that can be easily rendered as web pages or other formats.
