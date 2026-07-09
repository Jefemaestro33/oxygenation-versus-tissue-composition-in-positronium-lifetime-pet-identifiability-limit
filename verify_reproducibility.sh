#!/usr/bin/env bash
# Verify the reproducibility boundary for this paper package.
#
# Default mode checks byte-reproducible science outputs plus content-level
# reproducibility of the editorial artifacts. Set STRICT_BINARY=1 to additionally
# verify the exact current submission binary hashes.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PY="${PYTHON:-python3}"

say() { printf '\n== %s ==\n' "$1"; }
fail() { echo "ERROR: $*" >&2; exit 1; }
need_file() { [ -f "$1" ] || fail "missing file: $1"; }
same_file() { cmp -s "$1" "$2" || fail "files differ: $1 vs $2"; }

hash_stream() { shasum -a 256 | awk '{print $1}'; }

check_expected_hash() {
  local label="$1" expected="$2" actual="$3"
  [ "$actual" = "$expected" ] || fail "$label hash mismatch: expected $expected, got $actual"
  echo "ok  $label"
}

say "Environment"
"$PY" --version
"$PY" - <<'PY'
import numpy, scipy, matplotlib
print(f"numpy {numpy.__version__}")
print(f"scipy {scipy.__version__}")
print(f"matplotlib {matplotlib.__version__}")
PY
command -v pandoc >/dev/null 2>&1 && pandoc --version | head -1 || echo "pandoc: not found"
command -v xelatex >/dev/null 2>&1 && xelatex --version | head -1 || echo "xelatex: not found"
command -v pdfinfo >/dev/null 2>&1 && pdfinfo -v 2>&1 | head -1 || true

say "Rebuild science outputs"
PYTHON="$PY" "$ROOT/run_results.sh"
need_file results/checksums_science.sha256
shasum -a 256 -c results/checksums_science.sha256

say "Build manuscript and submission package"
"$ROOT/build_paper.sh"

for f in \
  paper/manuscript_ejnmmi.pdf \
  paper/manuscript_ejnmmi.docx \
  paper/cover_letter_ejnmmi.pdf \
  paper/cover_letter_ejnmmi.docx \
  paper/ESM_1_monte_carlo_validation.pdf \
  paper/submission_ejnmmi/manuscript_ejnmmi.pdf \
  paper/submission_ejnmmi/manuscript_ejnmmi.docx \
  paper/submission_ejnmmi/cover_letter_ejnmmi.pdf \
  paper/submission_ejnmmi/cover_letter_ejnmmi.docx \
  paper/submission_ejnmmi/ESM_1_monte_carlo_validation.pdf \
  paper/submission_ejnmmi/ESM_1_monte_carlo_validation.png \
  paper/submission_ejnmmi/figures/Fig1.png \
  paper/submission_ejnmmi/figures/Fig2.png \
  paper/submission_ejnmmi/figures/Fig3.png \
  paper/submission_ejnmmi/figures/Fig4.png \
  paper/submission_ejnmmi/figures/Fig5.png \
  paper/submission_ejnmmi/figures/Fig6.png
do
  need_file "$f"
done

same_file paper/manuscript_ejnmmi.pdf paper/submission_ejnmmi/manuscript_ejnmmi.pdf
same_file paper/manuscript_ejnmmi.docx paper/submission_ejnmmi/manuscript_ejnmmi.docx
same_file paper/cover_letter_ejnmmi.pdf paper/submission_ejnmmi/cover_letter_ejnmmi.pdf
same_file paper/cover_letter_ejnmmi.docx paper/submission_ejnmmi/cover_letter_ejnmmi.docx
same_file paper/ESM_1_monte_carlo_validation.pdf paper/submission_ejnmmi/ESM_1_monte_carlo_validation.pdf

same_file results/figures/fig1_bias_surface.png paper/submission_ejnmmi/figures/Fig1.png
same_file results/figures/fig2_sensitivity.png paper/submission_ejnmmi/figures/Fig2.png
same_file results/figures/fig4_degeneracy.png paper/submission_ejnmmi/figures/Fig3.png
same_file results/figures/fig3_separability.png paper/submission_ejnmmi/figures/Fig4.png
same_file results/figures/fig5_boundary.png paper/submission_ejnmmi/figures/Fig5.png
same_file results/figures/fig6_tumor_map.png paper/submission_ejnmmi/figures/Fig6.png
same_file results/figures/fig7_mc_validation.png paper/submission_ejnmmi/ESM_1_monte_carlo_validation.png
echo "ok  submission package file mapping"

say "Content hashes for document artifacts"
if command -v pdftotext >/dev/null 2>&1; then
  check_expected_hash "pdftext paper/manuscript_ejnmmi.pdf" \
    "8cc67c8f2fbdf18acda35516f0102733b3f68d97f3145aa6177f067da025273a" \
    "$(pdftotext paper/manuscript_ejnmmi.pdf - | hash_stream)"
  check_expected_hash "pdftext paper/cover_letter_ejnmmi.pdf" \
    "e852e00d7f69d366ebbb3ac0db6a8822c63dadd74fef317b960f19c6f8f59758" \
    "$(pdftotext paper/cover_letter_ejnmmi.pdf - | hash_stream)"
  check_expected_hash "pdftext paper/ESM_1_monte_carlo_validation.pdf" \
    "56de8e629f3a55e8231c1bcb9f263e46e5053a3f98afef95aec9b5c47245a266" \
    "$(pdftotext paper/ESM_1_monte_carlo_validation.pdf - | hash_stream)"
else
  echo "skip PDF text hashes: pdftotext not found"
fi

if command -v unzip >/dev/null 2>&1; then
  check_expected_hash "docxxml paper/manuscript_ejnmmi.docx" \
    "f9c98f36213a76352ee1d855d1d1d7c76943b6b3aacd59e5d51eb9c8b80fc256" \
    "$(unzip -p paper/manuscript_ejnmmi.docx word/document.xml | hash_stream)"
  check_expected_hash "docxxml paper/cover_letter_ejnmmi.docx" \
    "98b3293c425fc42f261f91fb139cec6d370ae2b63d8a0ff217c7ef0d8467e713" \
    "$(unzip -p paper/cover_letter_ejnmmi.docx word/document.xml | hash_stream)"
else
  echo "skip DOCX XML hashes: unzip not found"
fi

if [ "${STRICT_BINARY:-0}" = "1" ]; then
  say "Strict submission binary hashes"
  need_file paper/submission_ejnmmi/submission_manifest.sha256
  shasum -a 256 -c paper/submission_ejnmmi/submission_manifest.sha256
else
  echo
  echo "strict binary submission hash check skipped (set STRICT_BINARY=1 to enable)"
fi

say "Done"
echo "Reproducibility check passed."
