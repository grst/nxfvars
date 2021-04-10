import os
import base64
import json


class NxfVarHandler:
    def __init__(self, envvar="NXF_VARS") -> None:
        self.envvar = envvar
        try:
            nxfvars_b64_encoded = os.environ[envvar]
            nxfvar_json = base64.b64decode(nxfvars_b64_encoded)
            self.nxfvars = json.loads(nxfvar_json)
            if not {"task", "input", "params"}.issubset(self.nxfvars):
                raise ValueError(
                    "The NXFVARS map needs to define task, input and params"
                )

        except KeyError:
            self.nxfvars = None

    def _get_var(self, root_key, key, default):
        if self.nxfvars is None:
            if default is None:
                raise ValueError(
                    f"{self.envvar} is not set and no default value defined. "
                    "For running outside nextflow, define a default. "
                    "If running from nextflow, did you include `${nxfVars(task)}`?"
                )
            else:
                return default
        else:
            return self.nxfvars[root_key][key]

    def input(self, key, default=None):
        return self._get_var("input", key, default)

    def params(self, key, default=None):
        return self._get_var("params", key, default)

    def task(self, key, default=None):
        return self._get_var("task", key, default)