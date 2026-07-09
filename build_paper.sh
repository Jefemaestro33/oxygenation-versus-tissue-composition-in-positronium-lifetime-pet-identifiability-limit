#!/usr/bin/env bash
# Build the manuscript PDFs/DOCX and assemble the EJNMMI submission package.
#
# Incremental + source-date controlled: a target is rebuilt only when its source
# is newer (Make-style staleness), embedded dates are pinned via SOURCE_DATE_EPOCH,
# and all copies are content-conditional. Re-running a populated tree should not
# dirty git unless a source actually changed.
#
# Reproducibility scope: numerical results and PNG figures are byte-reproducible.
# Pandoc/TeX PDF and DOCX containers are content-reproducible and idempotent in a
# populated tree, but not promised bit-for-bit identical after deleting and
# rebuilding every binary artifact from scratch. See REPRODUCIBILITY.md.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
mkdir -p paper/figures paper/submission_ejnmmi/figures

for dep in pandoc xelatex; do
  command -v "$dep" >/dev/null 2>&1 || { echo "missing dependency: $dep" >&2; exit 1; }
done
[ -f results/figures/fig1_bias_surface.png ] || {
  echo "figures missing in results/figures/; run ./run_results.sh first" >&2; exit 1; }

# Pin embedded build dates. Prefer the versioned package epoch so rebuilding after
# a later commit does not silently change document metadata; override freely.
if [ -z "${SOURCE_DATE_EPOCH:-}" ]; then
  if [ -f "$ROOT/.source-date-epoch" ]; then
    SOURCE_DATE_EPOCH="$(tr -dc '0-9' < "$ROOT/.source-date-epoch")"
  else
    SOURCE_DATE_EPOCH="$(git -C "$ROOT" log -1 --format=%ct 2>/dev/null || echo 1782000627)"
  fi
fi
case "$SOURCE_DATE_EPOCH" in
  ''|*[!0-9]*) echo "invalid SOURCE_DATE_EPOCH: $SOURCE_DATE_EPOCH" >&2; exit 1 ;;
esac
export SOURCE_DATE_EPOCH
export FORCE_SOURCE_DATE=1

cp_diff() { cmp -s "$1" "$2" 2>/dev/null || cp "$1" "$2"; }          # copy only if bytes differ
stale()  { local o=$1; shift; [ -f "$o" ] || return 0; local f;     # OUT missing or any IN newer
           for f in "$@"; do [ "$f" -nt "$o" ] && return 0; done; return 1; }

# Mirror generated figures into the dir the PDFs reference (content-conditional).
for f in results/figures/*.png; do cp_diff "$f" "paper/figures/$(basename "$f")"; done
FIGS=(paper/figures/*.png)

stale paper/manuscript.pdf         paper/manuscript.md        "${FIGS[@]}" && (cd paper && pandoc manuscript.md -o manuscript.pdf --pdf-engine=xelatex)
stale paper/manuscript_ejnmmi.pdf  paper/manuscript_ejnmmi.md "${FIGS[@]}" && (cd paper && pandoc manuscript_ejnmmi.md -o manuscript_ejnmmi.pdf --pdf-engine=xelatex)
stale paper/manuscript_ejnmmi.docx paper/manuscript_ejnmmi.md "${FIGS[@]}" && (cd paper && pandoc manuscript_ejnmmi.md -o manuscript_ejnmmi.docx)
stale paper/cover_letter_ejnmmi.pdf  paper/cover_letter_ejnmmi.md  && (cd paper && pandoc cover_letter_ejnmmi.md -o cover_letter_ejnmmi.pdf --pdf-engine=xelatex)
stale paper/cover_letter_ejnmmi.docx paper/cover_letter_ejnmmi.md  && (cd paper && pandoc cover_letter_ejnmmi.md -o cover_letter_ejnmmi.docx)
stale paper/ESM_1_monte_carlo_validation.pdf paper/ESM_1_monte_carlo_validation.md && (cd paper && pandoc ESM_1_monte_carlo_validation.md -o ESM_1_monte_carlo_validation.pdf --pdf-engine=xelatex)

# Assemble the submission package (content-conditional -> no churn when unchanged).
cp_diff paper/manuscript_ejnmmi.pdf   paper/submission_ejnmmi/manuscript_ejnmmi.pdf
cp_diff paper/manuscript_ejnmmi.docx  paper/submission_ejnmmi/manuscript_ejnmmi.docx
cp_diff paper/cover_letter_ejnmmi.pdf paper/submission_ejnmmi/cover_letter_ejnmmi.pdf
cp_diff paper/cover_letter_ejnmmi.docx paper/submission_ejnmmi/cover_letter_ejnmmi.docx
cp_diff paper/ESM_1_monte_carlo_validation.pdf paper/submission_ejnmmi/ESM_1_monte_carlo_validation.pdf
cp_diff paper/submission_checklist_ejnmmi.md   paper/submission_ejnmmi/submission_checklist_ejnmmi.md
cp_diff results/figures/fig1_bias_surface.png  paper/submission_ejnmmi/figures/Fig1.png
cp_diff results/figures/fig2_sensitivity.png   paper/submission_ejnmmi/figures/Fig2.png
cp_diff results/figures/fig4_degeneracy.png    paper/submission_ejnmmi/figures/Fig3.png
cp_diff results/figures/fig3_separability.png  paper/submission_ejnmmi/figures/Fig4.png
cp_diff results/figures/fig5_boundary.png      paper/submission_ejnmmi/figures/Fig5.png
cp_diff results/figures/fig6_tumor_map.png     paper/submission_ejnmmi/figures/Fig6.png
cp_diff results/figures/fig7_mc_validation.png paper/submission_ejnmmi/ESM_1_monte_carlo_validation.png

# pdfinfo, content-conditional so metadata files don't churn on no-op runs.
pitmp="$(mktemp)"; trap 'rm -f "$pitmp"' EXIT
if command -v pdfinfo >/dev/null 2>&1; then
  pdfinfo paper/manuscript.pdf > "$pitmp"; cp_diff "$pitmp" results/pdfinfo.txt
  pdfinfo paper/manuscript_ejnmmi.pdf > "$pitmp"; cp_diff "$pitmp" results/pdfinfo_ejnmmi.txt
else
  echo "pdfinfo unavailable; manuscript.pdf was written." > "$pitmp"; cp_diff "$pitmp" results/pdfinfo.txt
  echo "pdfinfo unavailable; manuscript_ejnmmi.pdf was written." > "$pitmp"; cp_diff "$pitmp" results/pdfinfo_ejnmmi.txt
fi

echo "built paper/ and paper/submission_ejnmmi/ (incremental; unchanged targets skipped)"
