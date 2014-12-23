Usage
=====

OH Auto Statistical takes a **catchment descriptors (.CD3) file as input data**. The analyses are undertaken without any
further user input and a report file is generated containing the calculation details and results.

.. note::
   The first time OH Auto Statistical is run, it will download a complete set of gauged catchment data from the
   `National River Flow Archive (NRFA) <http://www.ceh.ac.uk/data/nrfa/>`_ for pooled analyses. This may take some time!
   NRFA data are subject to `terms and conditions <http://www.ceh.ac.uk/data/nrfa/data/data_terms.html>`_.

To undertake an analysis:

 1. Export a .CD3-file from the `FEH CD-ROM <http://www.hydrosolutions.co.uk/products.asp?categoryID=4670>`_ and save
    it somewhere.

 2. Locate the .CD3-file using Windows Explorer, right-click and select `Create OH Auto Statistical report`.

    .. image:: _static/context-menu.png

 3. A report is generated which has the same file name as the .CD3-file but ending with
    `Flood estimation report.yyyy-mm-dd.md`. This is a simple text file [#f1]_ and can be opened with `notepad`.

    .. image:: _static/report.png


.. rubric:: Footnotes

.. [#f1] This is in fact a `Markdown (*.md) file <http://daringfireball.net/projects/markdown/>`_ or more precisely a
         `GitHub Flavoured Markdown file <https://help.github.com/articles/github-flavored-markdown/>`_. Markdown files
         are plain text files that can be easily rendered as web pages or other formats.