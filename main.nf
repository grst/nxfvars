#!/usr/bin/env nextflow

nextflow.enable.dsl=2
include { TEST } from "./modules/nxf" addParams(testparam: 'testparam')

workflow {
    TEST("bar", Channel.fromPath("data/test_input.txt"), "myenv")
}