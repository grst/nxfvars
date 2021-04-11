import jupytext
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor


def nxfvars_execute(input_notebook, output_report, *, kernel_name="python3"):
    """Execute a notebook and convert it to a HTML report"""
    nb = jupytext.read(input_notebook, as_version=4)
    execute_preprocessor = ExecutePreprocessor(timeout=0, kernel_name=kernel_name)
    nb_executed, _ = execute_preprocessor.preprocess(nb)
    html_exporter = HTMLExporter()
    html_exporter.template_name = "classic"
    body, _ = html_exporter.from_notebook_node(nb_executed)
    with open(output_report, "w") as f:
        f.write(body)
