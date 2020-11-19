params.module_parame = "bar"

process TEST_SCRIPT {

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
    ${Nxf.vars(this, task)}
    test.py > result_script.txt
    """
}


process TEST_NOTEBOOK {
    
    conda "conda-forge::jupyterlab conda-forge::ipython=7.19.0"
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
    ${Nxf.vars(this, task)}
    jupyter nbconvert ${notebook} --execute --to html 
    """
}

