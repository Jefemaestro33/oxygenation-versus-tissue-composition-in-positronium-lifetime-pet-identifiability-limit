#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python3}"

cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p results results/figures paper/figures paper/submission_ejnmmi/figures

for dep in pandoc xelatex; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "missing dependency: $dep" >&2
    exit 1
  fi
done

"$PY" run/01_headline.py > results/01_headline.txt
"$PY" run/02_poisson_fim.py > results/02_poisson_fim.txt
"$PY" run/03_figures.py > results/03_figures.txt
"$PY" run/04_nuisance.py > results/04_nuisance.txt
"$PY" run/05_separability.py > results/05_separability.txt
"$PY" run/06_mc_validation.py > results/06_mc_validation.txt

cp results/figures/*.png paper/figures/

(cd paper && pandoc manuscript.md -o manuscript.pdf --pdf-engine=xelatex)
(cd paper && pandoc manuscript_ejnmmi.md -o manuscript_ejnmmi.pdf --pdf-engine=xelatex)
(cd paper && pandoc manuscript_ejnmmi.md -o manuscript_ejnmmi.docx)
(cd paper && pandoc cover_letter_ejnmmi.md -o cover_letter_ejnmmi.pdf --pdf-engine=xelatex)
(cd paper && pandoc cover_letter_ejnmmi.md -o cover_letter_ejnmmi.docx)
(cd paper && pandoc ESM_1_monte_carlo_validation.md -o ESM_1_monte_carlo_validation.pdf --pdf-engine=xelatex)

cp paper/manuscript_ejnmmi.pdf paper/submission_ejnmmi/
cp paper/manuscript_ejnmmi.docx paper/submission_ejnmmi/
cp paper/cover_letter_ejnmmi.pdf paper/submission_ejnmmi/
cp paper/cover_letter_ejnmmi.docx paper/submission_ejnmmi/
cp paper/ESM_1_monte_carlo_validation.pdf paper/submission_ejnmmi/
cp paper/submission_checklist_ejnmmi.md paper/submission_ejnmmi/
cp results/figures/fig1_bias_surface.png paper/submission_ejnmmi/figures/Fig1.png
cp results/figures/fig2_sensitivity.png paper/submission_ejnmmi/figures/Fig2.png
cp results/figures/fig4_degeneracy.png paper/submission_ejnmmi/figures/Fig3.png
cp results/figures/fig3_separability.png paper/submission_ejnmmi/figures/Fig4.png
cp results/figures/fig5_boundary.png paper/submission_ejnmmi/figures/Fig5.png
cp results/figures/fig6_tumor_map.png paper/submission_ejnmmi/figures/Fig6.png
cp results/figures/fig7_mc_validation.png paper/submission_ejnmmi/ESM_1_monte_carlo_validation.png

if command -v pdfinfo >/dev/null 2>&1; then
  pdfinfo paper/manuscript.pdf > results/pdfinfo.txt
  pdfinfo paper/manuscript_ejnmmi.pdf > results/pdfinfo_ejnmmi.txt
else
  echo "pdfinfo unavailable; manuscript.pdf was written." > results/pdfinfo.txt
  echo "pdfinfo unavailable; manuscript_ejnmmi.pdf was written." > results/pdfinfo_ejnmmi.txt
fi

echo "wrote results, figures, paper/manuscript.pdf, paper/manuscript_ejnmmi.pdf, and paper/submission_ejnmmi/"
