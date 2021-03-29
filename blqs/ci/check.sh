#!/usr/bin/env bash

###############################################################################
# Runs the CI tests locally.
###############################################################################

pytest blqs
black --check --line-length=100 blqs
mypy --config-file=ci/mypy.ini blqs
