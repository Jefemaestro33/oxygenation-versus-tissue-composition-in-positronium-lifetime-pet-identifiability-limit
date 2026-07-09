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
    "b2c1723a760ffdfc8f89807f54af61849a0c958f59140718f88a6c4105a52c9c" \
    "$(pdftotext paper/manuscript_ejnmmi.pdf - | hash_stream)"
  check_expected_hash "pdftext paper/cover_letter_ejnmmi.pdf" \
    "1ea2dd6ea1cb76ba8314047bd4bba2565909e88395fe89d9cb5389b8abceb65b" \
    "$(pdftotext paper/cover_letter_ejnmmi.pdf - | hash_stream)"
  check_expected_hash "pdftext paper/ESM_1_monte_carlo_validation.pdf" \
    "9c1b3089f3e98ea097f2dc977742ae215756de77c5c87dcddcd485d4c8ecec59" \
    "$(pdftotext paper/ESM_1_monte_carlo_validation.pdf - | hash_stream)"
else
  echo "skip PDF text hashes: pdftotext not found"
fi

if command -v unzip >/dev/null 2>&1; then
  check_expected_hash "docxxml paper/manuscript_ejnmmi.docx" \
    "f4de79b7f88c46fae0931fc4ba60fffba99fea60343e0e05adec32747fc9b5e6" \
    "$(unzip -p paper/manuscript_ejnmmi.docx word/document.xml | hash_stream)"
  check_expected_hash "docxxml paper/cover_letter_ejnmmi.docx" \
    "2329222b7534499851f3983ec418dc7bfd379624180f885fa8c3fe896899f464" \
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
