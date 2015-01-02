Usage
=====

OH Auto Statistical takes a **catchment descriptors (.CD3) file as input data**. The analyses are undertaken without any
further user input and a report file is generated containing the calculation details and results.

Flood estimation
----------------

To undertake an analysis:

 1. Export a .CD3-file from the `FEH CD-ROM <http://www.hydrosolutions.co.uk/products.asp?categoryID=4670>`_ and save
    it somewhere.

 2. Locate the .CD3-file using Windows Explorer, right-click and select `Create OH Auto Statistical report`.

    .. image:: _static/context-menu.png

 3. A report is generated which has the same file name as the .CD3-file but ending with
    `Flood estimation report.yyyy-mm-dd.md`. This is a simple text file [#f1]_ and can be opened with `notepad`.

    .. image:: _static/report.png


Updating NRFA data
------------------

National River Flow Archive (NRFA) data are automatically downloaded during the installation of OH Auto Statistical. To
update the data using the latest published NRFA dataset, select in the Windows Start Menu `Open Hydrology` →
`OH Auto Statistical` → `Reload NRFA data`.

All existing data will be removed before downloading a complete new dataset. This may take a while.


Customising the report template
-------------------------------

The report template can be customised by placing a file `normal.md` in the folder
`C:\\Users\\<username>\\AppData\\Local\\Open Hydrology\\OH Auto Statistical\\templates`. It is recommended to copy and modify
the content from the standard templates saved in
`C:\\Program Files\\Open Hydrology\\OH Auto Statistical\\ohvenv\\Lib\\site-packages\\autostatistical\\templates\\plain.md`.

.. rubric:: Footnotes

.. [#f1] This is in fact a `Markdown (*.md) file <http://daringfireball.net/projects/markdown/>`_ or more precisely a
         `GitHub Flavoured Markdown file <https://help.github.com/articles/github-flavored-markdown/>`_. Markdown files
         are plain text files that can be easily rendered as web pages or other formats.