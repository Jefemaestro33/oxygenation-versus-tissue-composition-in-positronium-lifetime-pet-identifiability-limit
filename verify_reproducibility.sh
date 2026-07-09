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
  paper/manuscript.pdf \
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
  check_expected_hash "pdftext paper/manuscript.pdf" \
    "5999bc803f1507623f96244b9a895d97ec5b0141bcd3495cec03bb2fe3250b91" \
    "$(pdftotext paper/manuscript.pdf - | hash_stream)"
  check_expected_hash "pdftext paper/manuscript_ejnmmi.pdf" \
    "75819f7e0428c3fe02640007a4cfe3c9eb66b0e71eda93a5c7eef5c07237a185" \
    "$(pdftotext paper/manuscript_ejnmmi.pdf - | hash_stream)"
  check_expected_hash "pdftext paper/cover_letter_ejnmmi.pdf" \
    "1533ed1f9652d35080d844e579b3f3af08f50bcfab98f76aeea2df8a064812ea" \
    "$(pdftotext paper/cover_letter_ejnmmi.pdf - | hash_stream)"
  check_expected_hash "pdftext paper/ESM_1_monte_carlo_validation.pdf" \
    "2125e7be9904f2e98e34260f7f92433af8273bbb91752cc6618092823ffdf3e5" \
    "$(pdftotext paper/ESM_1_monte_carlo_validation.pdf - | hash_stream)"
else
  echo "skip PDF text hashes: pdftotext not found"
fi

if command -v unzip >/dev/null 2>&1; then
  check_expected_hash "docxxml paper/manuscript_ejnmmi.docx" \
    "1ad41b797880dba1919392f6fe4fc05b82657d193c99c56a43446caf8029e966" \
    "$(unzip -p paper/manuscript_ejnmmi.docx word/document.xml | hash_stream)"
  check_expected_hash "docxxml paper/cover_letter_ejnmmi.docx" \
    "5e11912e380b2748955a6a05c846de960a6a3aa752bf28f5dd8a04bc2db0fe8e" \
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
