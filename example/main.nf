#!/usr/bin/env nextflow
nextflow.enable.dsl=2

params.global_param = "Hey, I'm a global parameter"

include { 
    TEST_SCRIPT;
    TEST_NOTEBOOK
} from "./test" addParams(module_param: "Hey, I'm a module parameter")

//this, obviously, should become a pip-installable package at some point 
// instead of staging it manually
nxfvars = file("..") 


workflow {
    TEST_SCRIPT("bar", Channel.fromPath("data/test_input.txt"), nxfvars)
    TEST_NOTEBOOK(
        Channel.fromPath("data/test_notebook.ipynb"), 
        "bar",
        Channel.fromPath("data/test_input.txt"),
        nxfvars
    )
}