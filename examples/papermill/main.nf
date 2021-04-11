#!/usr/bin/env nextflow

nextflow.enable.dsl=2
params.global_param = "Hey, I'm a global parameter!"

include { nxfvars } from "./nxfvars.nf"

process papermill {

    publishDir "results"
    cpus 2
    conda "papermill ipykernel nbconvert"

    input:
    val input_value 
    path notebook
    path input_file 

    output:
    path "report.html"

    script:
    """
    ${nxfvars(task)}

    papermill ${notebook} notebook_executed.ipynb -f .params.yml -k python3
    jupyter nbconvert --to html --output report.html notebook_executed.ipynb
    """
}

workflow {
  papermill(
        "bar",
        Channel.fromPath(projectDir + "/notebook.ipynb"), 
        Channel.fromPath(params.test_file)
    )
}