from typing import Union
import yaml
from pathlib import Path
from collections.abc import Mapping


class _ParamsMapping(Mapping):
    """A mapping holding parameters. Behaves like an immutable dictionary,
    but provides additional safety checks."""

    def __init__(self, params: Mapping = None, set_initalized: bool = False):
        self._is_initalized = params is not None or set_initalized
        self._store = dict() if params is None else dict(**params)

    @property
    def is_initalized(self):
        """True if the the Mapping has been initalized with parameters"""
        return self._is_initalized

    def __getitem__(self, key):
        return self._store[key]

    def __iter__(self):
        return self._store.__iter__()

    def __len__(self):
        return self._store.__len__()

    def get(self, key, default):
        """Get an item if present, return `default` if no configuration was loaded.
        Raise a KeyError if a configuration was loaded, but the key is not present"""
        if not self.is_initalized:
            return default
        else:
            try:
                return self[key]
            except KeyError:
                raise KeyError(f"{key} not found in parameters. ")


class NextflowParamsHandler(_ParamsMapping):
    """A mapping initialized from a config file. If the config
    file does not exists, it will be an empty mapping"""

    def __init__(self, params_file: Union[Path, str]):
        try:
            with open(params_file, "r") as f:
                # manually set to initalized, as safe_load on an empty file returns None
                super().__init__(yaml.safe_load(f), True)
        except FileNotFoundError:
            super().__init__()

        # params and task should always be present (in doubt empty)
        # and also raise an error on `get`, when a config file was loaded.
        self._store["params"] = _ParamsMapping(
            self._store.get("params", None), self.is_initalized
        )
        self._store["task"] = _ParamsMapping(
            self._store.get("task", None), self.is_initalized
        )
