#!/bin/bash
set -e -x

if [ -f ./requirements_test.txt ]; then
   pip install -q -r ./requirements_test.txt
else
   pip install -q -r ../requirements_test.txt
fi

pytest --cov=PyStacks --pyargs PyStacks -s