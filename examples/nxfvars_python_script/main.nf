#!/usr/bin/env nextflow

nextflow.enable.dsl=2
params.global_param = "Hey, I'm a global parameter!"

include { nxfvars } from "./nxfvars.nf"

process nxfvars_python_script {

    publishDir "results"
    cpus 2

    input:
    val input_value 
    path input_file 

    output:
    path "result.txt"

    script:
    """
    ${nxfvars(task)}
    test.py > result.txt
    """
}

workflow {
    nxfvars_python_script("bar", Channel.fromPath(params.test_file))
}