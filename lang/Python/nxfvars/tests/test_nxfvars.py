from nxfvars._params_handler import _ParamsMapping, NextflowParamsHandler
import pytest
from . import TESTDATA


def test_empty_params_mapping():
    pm = _ParamsMapping()
    with pytest.raises(KeyError):
        pm["foo"]

    assert pm.get("foo", "bar") == "bar"

    assert len(pm) == 0
    for _ in pm:
        assert False, "iterator not empty"

    assert pm.is_initalized is False


def test_params_mapping():
    pm = _ParamsMapping({"foo": "bar", "task": {"task.foo": "bar"}})
    with pytest.raises(KeyError):
        pm["doesntexist"]

    with pytest.raises(KeyError):
        pm.get("doesntexist", "default")

    assert pm["foo"] == "bar"
    assert pm.get("foo", "default") == "bar"
    assert pm["task"]["task.foo"] == "bar"

    assert pm.is_initalized is True


def test_nextflow_params_handler():

    pm = NextflowParamsHandler(TESTDATA / ".doesntexist.yml")
    assert pm.is_initalized is False

    with pytest.raises(KeyError):
        pm["doesntexist"]

    assert pm.get("doesntexist", "default") == "default"

    assert pm["params"] == dict()
    assert pm["params"].get("params.foo", "default") == "default"

    assert pm["task"] == dict()
    assert pm["task"].get("task.foo", "default") == "default"


def test_nextflow_params_handler_empty_file():
    pm = NextflowParamsHandler(TESTDATA / "params_empty.yml")
    assert pm.is_initalized is True

    with pytest.raises(KeyError):
        pm.get("doesntexist", "default")

    assert pm["params"] == dict()
    with pytest.raises(KeyError):
        pm["params"].get("doesntexist", "default")

    assert pm["task"] == dict()
    with pytest.raises(KeyError):
        pm["task"].get("doesntexist", "default")


def test_nextflow_params_handler_reduced_file():
    pm = NextflowParamsHandler(TESTDATA / "params2.yml")
    assert pm.is_initalized is True

    assert pm["foo"] == "bar"
    assert pm["bar"] == "baz"

    with pytest.raises(KeyError):
        pm.get("doesntexist", "default")

    assert pm["params"] == dict()
    with pytest.raises(KeyError):
        pm["params"].get("doesntexist", "default")

    assert pm["task"] == dict()
    with pytest.raises(KeyError):
        pm["task"].get("doesntexist", "default")


def test_nextflow_params_handler_full_file():
    pm = NextflowParamsHandler(TESTDATA / "params1.yml")

    with pytest.raises(KeyError):
        assert pm["params"].get("foo", "default")

    assert pm["params"]["global_param"] == "Hey, I'm a global parameter"

    assert pm["task"]["cpus"] == "2"

    assert pm["bar"] == "bar"
