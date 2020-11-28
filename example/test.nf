params.module_param = "bar"

include {nxfVars} from "./nxfvars.nf"

process TEST_SCRIPT {

    conda "conda-forge::setuptools_scm conda-forge::flit"
    publishDir "results/result_script", mode: 'copy'
    cpus 2

    input:
    val bar
    path foo
    path nxfvars

    output:
    path "result_script.txt"

    script:
    """
    ${nxfVars(task)}
    test.py > result_script.txt
    """
}


process TEST_NOTEBOOK {
    
    conda "conda-forge::jupyterlab conda-forge::ipython=7.19.0 conda-forge::setuptools_scm conda-forge::flit"
    publishDir "results/result_notebook", mode: 'copy'
    cpus 2

    input:
    path notebook
    val bar
    path foo
    path nxfvars

    output:
    path "*.html"

    script:
    """
    ${nxfVars(task)}
    jupyter nbconvert ${notebook} --execute --to html 
    """
}

