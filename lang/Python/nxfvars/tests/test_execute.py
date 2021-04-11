import pytest
from . import TESTDATA
from nxfvars.execute import nxfvars_execute


@pytest.mark.parametrize(
    "notebook", [TESTDATA / "notebook.ipynb", TESTDATA / "notebook.py"]
)
def test_execute_notebook(notebook, tmp_path):
    report_file = tmp_path / "report.html"
    nxfvars_execute(notebook, report_file, kernel_name="python3")
    assert "The answer is 42." in report_file.read_text()
