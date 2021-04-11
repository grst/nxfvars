#!/usr/bin/env nextflow

nextflow.enable.dsl=2
params.global_param = "Hey, I'm a global parameter!"

include { nxfvars } from "./nxfvars.nf"

process nxfvars_rmarkdown {

    publishDir "results"
    cpus 2
    conda "r-rmarkdown r-yaml"
    // work around https://github.com/rstudio/rmarkdown/issues/1508
    stageInMode "copy"

    input:
    val input_value 
    path notebook
    path input_file 

    output:
    path "report.html"

    script:
    """
    ${nxfvars(task)}

    render.R ${notebook} report.html
    """
}

workflow {
    nxfvars_rmarkdown(
        "bar",
        Channel.fromPath(projectDir + "/notebook.Rmd"), 
        Channel.fromPath(params.test_file)
    )
}