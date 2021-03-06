#!/usr/bin/env bash

###############################################################################
# Runs the CI tests locally.
###############################################################################

pytest blqs blqs_cirq
black --check --line-length=100 blqs blqs_cirq
mypy --config-file=ci/mypy.ini blqs/blqs blqs_cirq/blqs_cirq
pylint --rcfile=ci/.pylintrc blqs_cirq/blqs_cirq/ blqs/blqs
