#!/usr/bin/env python

from nxfvars import nxfvars

print("input_value:", nxfvars["input_value"])
print("input_file:", nxfvars["input_file"])
print("params.global_param:", nxfvars["params"]["global_param"])
print("task.cpus:", nxfvars["task"]["cpus"])

with open(nxfvars["input_file"]) as f:
    print(f"The content of {nxfvars['input_file']} is:", "".join(f.readlines()))
