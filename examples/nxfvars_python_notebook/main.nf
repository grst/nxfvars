#!/usr/bin/env nextflow

nextflow.enable.dsl=2
params.global_param = "Hey, I'm a global parameter!"

include { nxfvars } from "./nxfvars.nf"

process nxfvars_python_notebook {

    publishDir "results"
    cpus 2

    input:
    val input_value 
    path notebook
    path input_file 

    output:
    path "report.html"

    script:
    """
    ${nxfvars(task)}
    nxfvars execute ${notebook} report.html
    """
}

workflow {
    nxfvars_python_notebook(
        "bar",
        Channel.fromPath(projectDir + "/notebook.ipynb"), 
        Channel.fromPath(params.test_file)
    )
}