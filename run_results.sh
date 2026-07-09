#!/usr/bin/env bash
# Reproduce the numerical results and figures. Needs only Python + requirements.txt
# (NumPy/SciPy/Matplotlib) -- no pandoc/xelatex. Split out from run_all.sh so the
# science is reproducible without the PDF toolchain.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python3}"

cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p results results/figures paper/figures

"$PY" run/01_headline.py > results/01_headline.txt
"$PY" run/02_poisson_fim.py > results/02_poisson_fim.txt
"$PY" run/03_figures.py > results/03_figures.txt
"$PY" run/04_nuisance.py > results/04_nuisance.txt
"$PY" run/05_separability.py > results/05_separability.txt
"$PY" run/06_mc_validation.py > results/06_mc_validation.txt

echo "wrote results/ and results/figures/ (no PDF toolchain required)"
