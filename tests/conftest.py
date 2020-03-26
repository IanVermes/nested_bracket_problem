#!/usr/bin/env python
# -*- coding: utf8 -*-

import pathlib

import pytest
import yaml


def create_params_from_yaml():
    yaml_file = pathlib.Path("strings.yaml")
    if not yaml_file.exists():
        msg = (
            f"Cannot find {yaml_file}. Either file does not exist or "
            "pytest is not called from the repository root."
        )
        raise FileNotFoundError(msg)
    parameters = []
    param_args = "test_input,expected_output"

    with open("strings.yaml") as handle:
        data = yaml.safe_load(handle)
    for key, strings in data.items():
        if key.lower() == "valid":
            expected_output = 0
        elif key.lower() == "invalid":
            expected_output = 1
        else:
            raise KeyError("Unexpected key in yaml. Got {key!r}")
        for test_input in strings:
            if len(test_input) > 50:
                param_name = f" {key} {len(test_input)=} test_input='LONGSTRING!' "
            else:
                param_name = f" {key} {len(test_input)=} {test_input=} "
            one_param = pytest.param(test_input, expected_output, id=param_name,)
            parameters.append(one_param)

    for parameter in parameters:
        print(f"{parameter=}")

    return (param_args, parameters)
