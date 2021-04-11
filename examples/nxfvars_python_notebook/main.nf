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
    path "result.txt"
    path "report.html"

    script:
    """
    ${nxfvars(task)}
    nxfvars execute ${notebook} report.html
    """
}

workflow {
    nxfvars_python_script("bar", Channel.fromPath(params.test_file))
}