#!/usr/bin/env bash
# Install a local environment and reproduce the article's data products.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
PYTHON="${PYTHON:-python3}"
"$PYTHON" -c 'import sys; assert (3,11) <= sys.version_info[:2] <= (3,12), "Use Python 3.11 or 3.12"'
if [[ ! -x .venv/bin/python ]]; then
    "$PYTHON" -m venv .venv
fi
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
.venv/bin/python -m pip install --disable-pip-version-check --only-binary=:all: -r requirements.lock
.venv/bin/python -m reproduction "$@"
