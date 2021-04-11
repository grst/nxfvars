Nxfvars: Parameterize Notebooks from Nextflow 
=============================================
|pytestworkflow| |pytest|


.. |pytest| image:: https://github.com/grst/nxfvars/actions/workflows/pytest-nxfvars-python.yml/badge.svg
     :target: https://github.com/grst/nxfvars/actions/workflows/pytest-nxfvars-python.yml
     :alt: CI test for the nxfvars python library
     
.. |pytestworkflow| image:: https://github.com/grst/nxfvars/actions/workflows/pytest-workflow-examples.yml/badge.svg
    :target: https://github.com/grst/nxfvars/actions/workflows/pytest-workflow-examples.yml
    :alt: Running the examples with pytest-workflow

Nxfvars makes it easy to parameterize Jupyter notebooks, Rmarkdown notebooks, or plain 
Python scripts from a Nextflow process. All variables accessible in
a process's ``script`` section are made available directly in the notebook.  


Using nxfvars in a Nextflow pipeline
------------------------------------

Download `nxfvars.nf <lang/nextflow/nxfvars.nf>`_ and add the script to your pipeline. 
Import the `nxfvars` function and call it from the script section of your process: 

.. code-block:: nextflow

    nextflow.enable.dsl = 2
    include { nxfvars } from "./nxfvars.nf"

    process foo {
        script:
        """
        ${nxfvars(task)}

        # run script or execute notebook here
        """
    }

When the process is executed, nxfvars generates a ``.params.yml`` file
in the work directory. It contains all variables that can be accessed in the `script`
section. The YAML-file can be consumed by the nxfvars Python library,
`Papermill <https://papermill.readthedocs.io/en/latest/usage-parameterize.html>`_,
or any YAML parser (see below). 


Usage with the nxfvars Python library
-------------------------------------

.. 

   Full examples at `examples/nxfvars_python_script <examples/nxfvars_python_script>`_ and `examples/nxfvars_python_notebook <examples/nxfvars_python_notebook>`_.

The nxfvars Python library is a thin wrapper around a YAML parser. It may be used
from both Jupyter notebooks or plain Python scripts. You can install it using pip:

.. code-block:: bash

    pip install nxfvars

In python, nextflow variables can be accessed through the ``nxfvars`` object: 

.. code-block:: python

    from nxfvars import nxfvars
    
    print(nxfvars["foo"])
    print(nxfvars["params"]["bar"])
    print(nxfvars["task"]["cpus"])

It is common to execute notebooks interactively during development and run them later
with parameters. In that case you can use ``.get()`` to obtain default values, 
when a ``.params.yml`` is not yet present

.. code-block:: python

    nxfvars.get("foo", "default value for development")


From nextflow, just invoke the python script, or use e.g. ``jupyter nbconvert`` to 
execute the notebook. 

``nxfvars execute`` is a convenient wrapper around `jupytext <https://jupytext.readthedocs.io/en/latest/>`_
and `jupyter nbconvert <https://nbconvert.readthedocs.io/en/latest/>`_ to execute and 
convert arbitrary jupytext notebook formats to a html report. 

.. code-block:: nextflow

    process nxfvars_python {
        script:
        """
        ${nxfvars(task)}

        # simply execute the script here
        python my_script.py
        # or execute the notebook
        nxfvars execute notebook.ipynb report.html        
        """
    }


Usage with Papermill
--------------------
.. 

   Full example at `examples/papermill <examples/papermill>`_ 

Papermill is an established library for parameterizing jupyter notebooks. It can 
readily consume yaml files generated with nxfvars. 

.. code-block:: nextflow

    process papermill {

        output:
            file("report.html), emit: report

        script:
        """
        ${nxfvars(task)}

        papermill some_notebook.ipynb notebook_executed.ipynb -f .params.yml -k python3
        # optional: convert to HTML report
        jupyter nbconvert --to html --output report.html notebook_executed.ipynb
        """
    }

Usage with Rmarkdown
--------------------
.. 

   Full example at `examples/rmarkdown <examples/rmarkdown>`_ 

For now, we use the following R snippet (``render.R``) to parse the yaml file and
render the notebook with ``rmarkdown``. This could be facilitated in the future by 
porting the nxfvars library to R. 

.. code-block:: R

    # USAGE: render.R notebook.Rmd report.html
    args = commandArgs(trailingOnly=TRUE)
    nxfvars = list(nxfvars = yaml::read_yaml('.params.yml'))
    rmarkdown::render(args[1], params = nxfvars, output_file=args[2])

.. code-block:: nextflow

    process rmarkdown {
        stageInMode "copy" // work around https://github.com/rstudio/rmarkdown/issues/1508
        output:
            file("report.html"), emit: report

        script:
        """
        ${nxfvars(task)}

        render.R 'notebook.Rmd' 'report.html'
        """
    }



How it works
------------

All variables in a nextflow process (except local variables declared with ``def``) can be 
programmatically accessed through Nextflow's implicit variables ``this`` and ``task``. 
See also my `blog post <https://grst.github.io/bioinformatics/2020/11/28/low-level-nextflow-hacking.html>`_
about these variables. 

The ``nxvfars(task)`` function encodes all variables as YAML and injects them into the 
bash script. 
