"""Access nextflow variables from Python"""
from .nxf_var_handler import NxfVarHandler
from ._metadata import __version__, __author__, __email__, within_flit

nxf = NxfVarHandler()
