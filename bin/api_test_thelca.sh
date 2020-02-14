#!/bin/bash

TOP=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

export PYTHONPATH=$TOP

# run the python API tests against a running server

cd $TOP/thelca/test
python3 -m unittest -v api_tests_*.py
