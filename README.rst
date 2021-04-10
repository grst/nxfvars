Nxfvars: Parametrize Notebooks from Nextflow 
============================================

Nxfvars makes it easy to parametrize Jupyter notebooks, Rmarkdown notebooks, or plain 
Python scripts from a Nextflow process. All variables accessible in
a process's `script` section are made available directly in the notebook.  


Using nxfvars in a Nextflow pipeline
------------------------------------

Download `nxfvars.nf <lang/nextflow/nxfvars.nf>`_ and add the script to your pipeline. 
Import the `nxfvars` function and call it from the script section of your process: 

.. code-block:: console

    nextflow.enable.dsl = 2
    import { nxfvars } from "./nxfvars.nf"

    process foo {
        script:
        """
        ${nxfvars(task)}

        # run script or execute notebook here
        """
    }

When the process is executed, nxfvars generates a `.params.yml` file
in the work directory. It contains all variables that can be accessed in the `script`
section. The YAML-file can be consumed with the nxfvars python library,
`papermill <https://papermill.readthedocs.io/en/latest/usage-parameterize.html>`_,
or any YAML parser (see below). 


Usage with the nxfvars Python library
-------------------------------------

The nxfvars Python library is a thin wrapper around a YAML parser. It may be used
from both Jupyter notebooks or plain Python scripts.

In python, nextflow variables can be accessed through the `nxfvars` object: 

.. code-block:: python

    from nxfvars import nxfvars
    
    print(nxfvars["foo"])
    print(nxfvars["params]["bar])

It is common to execute notebooks interactively during development and run them later
with parameters. In that case you can use `.get()` to obtain default values, 
when a `.params.yml` is not yet present

.. code-block:: python

    print(nxfvars.get("foo", "default value for development"))


From nextflow, just invoke the python script, or use e.g. `jupyter nbconvert` to 
execute the notebook. `nxfvars execute` is a convenient wrapper around `jupytext` and
`jupyter nbconvert` to execute and convert arbitrary jupytext notebook formats 
to a html report. 

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

Papermill is an established library for parametrizing jupyter notebooks. It can 
readily consume yaml files generated with nxfvars. 

.. code-block:: nextflow

    process papermill {

        output:
            file("report.html), emit: report

        script:
        """
        ${nxfvars(task)}

        papermill some_notebook.ipynb notebook_executed.ipynb -f .params.yml
        # optional: convert to HTML report
        jupyter nbconvert --to html -o report.html notebook_executed.ipynb
        """
    }

Usage with Rmarkdown
--------------------

For now, we use an R snippet to parse the yaml file. This could be facilitated
in the future by porting the nxfvars library to R. 

.. code-block:: nextflow

    process rmarkdown {

        output:
            file("report.html"), emit: report

        script:
        """
        ${nxfvars(task)}

        Rscript -e "rmarkdown::render(
            'notebook.Rmd', 
            params = yaml::read_yaml('.params.yml')),
            output_file = "report.html"
        )"
        """
    }



How it works
------------

All variables in a nextflow process (except local variables declared with `def`) can be 
programmatically accessed through Nextflow's implicit variables `this` and `task`. 
See also my `blog post <https://grst.github.io/bioinformatics/2020/11/28/low-level-nextflow-hacking.html>`_
about these variables. 

The `nxvfars(task)` function encodes all variables as YAML and injects it into the 
bash script. 
