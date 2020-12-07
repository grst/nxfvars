nxfvars: Access nextflow variables from python scripts or notebooks
===================================================================

This is a proof-of-concept how to make it easier to access nextflow vars from
python scripts or notebooks.

Installation
------------

.. code-block::
    
    git clone git@github.com:grst/nxfvars.git
    cd nxfvars
    pip install . 


PyPI and conda will follow at some point. 

Usage
-----

Add the  `nxfvars.nf <example/nxfvars.nf>`_ script to your pipeline. Import the 
`nxfVars` function as follows: 

.. code-block::

    import { nxfVars } from "./nxfvars.nf"

In each process where you want to use `nxfvars`, add the following line
to the `script` section, right before executing the python script or notebook: 

.. code-block::

    ${nxfVars(task)}


For instance: 

.. code-block:: 

    process TEST { 
        cpus 2

        input:
        val bar
        path foo
        path nxfvar

        script:
        """
        ${nxfVars(task)}
        jupyter nbconvert notebook.ipynb --execute --to html 
        """
    }

In your python script, add

.. code-block:: python

    from nxfvars import nxf

You can now retrieve inputs, params and task variables as follows: 

.. code-block:: python

    nxf.input('bar')
    nxf.task('cpus')
    nxf.params('some_param')

To execute a notebook interactively (i.e. outside of nextflow), you may define
default values: 

.. code-block:: python

    nxf.input('bar', "/path/to/some/file.foo")
    
 
For a full example pipeline, see the `example directory <example/>`_. 



How it works
------------

The groovy library serializes the nextflow variables and encodes
them into an environment variable, which is injected using :code:`${nxfVars(task)}`. 
See also my `blog post <https://grst.github.io/bioinformatics/2020/11/28/low-level-nextflow-hacking.html>`_
about Nextflow's implicit variables `this` and `task`. 

The :code:`nxfvars` Python library decodes the env var and makes the values 
conveniently accessible


Ideas for the future
--------------------

* This can obviously be easily ported to other languages, e.g. :code:`R`. 
* The library could be extended to serve as a minimal argument parser, i.e. that 
  a Python script containing :code:`nxf.input("foo")` could also be executed (outside Nextflow)
  using :code:`scripyt.py --foo=bar`. 
