# Reproducibility audit

This repository separates scientific reproducibility from editorial artifact
reproducibility.

## Audited environment

The submission package was audited with:

- Python 3.13.6
- NumPy 2.4.3
- SciPy 1.17.1
- Matplotlib 3.11.0
- Pandoc 3.9.0.2
- XeTeX / TeX Live 2026
- Poppler `pdfinfo`/`pdftotext` 26.04.0

The tested Python package set is pinned in `requirements-lock.txt`. The minimal
unpinned dependency list is `requirements.txt`.

## Recommended reproduction

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
./verify_reproducibility.sh
```

On the author's workstation:

```bash
PYTHON=/Users/darellplascencia/tesis_env/bin/python ./verify_reproducibility.sh
```

## What is byte-reproducible

The scientific outputs are expected to reproduce byte-for-byte:

- `results/01_headline.txt`
- `results/02_poisson_fim.txt`
- `results/03_figures.txt`
- `results/04_nuisance.txt`
- `results/05_separability.txt`
- `results/06_mc_validation.txt`
- `results/figures/*.png`

These are checked against `results/checksums_science.sha256`.

## What is content-reproducible

The manuscript and submission package are editorial artifacts generated through
Pandoc and TeX. They are reproducible in content and idempotent when re-run in a
populated tree, but the PDF/DOCX binary containers should not be treated as
bit-for-bit reproducible after deleting all generated files and rebuilding from
scratch.

The verification script checks:

- the manuscript and submission files exist;
- submission copies match their generated sources;
- Fig. 1--6 and Online Resource PNG map byte-for-byte to `results/figures`;
- extracted PDF text hashes match the audited content hashes when `pdftotext` is
  available;
- DOCX `word/document.xml` hashes match the audited content hashes when `unzip`
  is available.

For archival integrity of the exact uploaded files, use:

```bash
STRICT_BINARY=1 ./verify_reproducibility.sh
```

That strict mode checks `paper/submission_ejnmmi/submission_manifest.sha256`.
It is intentionally stricter than scientific reproducibility and may fail if a
fresh Pandoc/TeX rebuild changes binary container bytes without changing content.

## Source date

`.source-date-epoch` pins the default `SOURCE_DATE_EPOCH` used by
`build_paper.sh`. This prevents later commits from changing document metadata
only because `HEAD` changed. Override it explicitly if needed:

```bash
SOURCE_DATE_EPOCH=<unix-time> ./build_paper.sh
```
