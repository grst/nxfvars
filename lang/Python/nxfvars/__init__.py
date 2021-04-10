"""Access nextflow variables from Python"""
from ._params_handler import NextflowParamsHandler

__version__ = "0.2"

nxfvars = NextflowParamsHandler(".params.yml")
