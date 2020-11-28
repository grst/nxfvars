#!/usr/bin/env python

import sys

sys.path.insert(0, "nxfvars")
from nxfvars import nxf

print("Input 'bar': ", nxf.input("bar"))
print("Input 'foo': ", nxf.input("foo"))
print("Params 'global_param': ", nxf.params("global_param"))
print("Params 'module_param': ", nxf.params("module_param"))
print("Task 'cpus': ", nxf.params("module_param"))

print()
with open(nxf.input("foo")) as f:
    print("The content of 'foo' is ", "".join(f.readlines()))


print("Hello World!")