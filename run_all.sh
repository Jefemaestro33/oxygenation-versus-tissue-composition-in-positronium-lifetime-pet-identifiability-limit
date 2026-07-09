#!/usr/bin/env bash
# Full pipeline: numerical results + figures, then the paper build.
# Reproduce only the science (no PDF toolchain):   ./run_results.sh
# Build only the PDFs (needs pandoc + xelatex):     ./build_paper.sh
# Use a specific interpreter:                       PYTHON=/path/to/python ./run_all.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYTHON="${PYTHON:-python3}" "$ROOT/run_results.sh"
"$ROOT/build_paper.sh"

echo "wrote results, figures, the canonical EJNMMI manuscript, and the submission bundle (paper/submission_ejnmmi/)"
