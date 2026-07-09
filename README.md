# Identifiability limits of oxygenation vs composition in positronium-lifetime imaging

A modeling/methods paper. **Thesis:** from the o-Ps lifetime alone, tissue
oxygenation (pO2) and tissue composition (lipid/free-volume) are *structurally
non-identifiable* — they enter as one summed decay rate. We quantify the
resulting hypoxia-imaging bias, show when a second observable (o-Ps intensity
I3, or the 3γ/2γ ratio) can break the degeneracy, and define the decisive
experiment.

**Framing rule:** this is a *limits* paper, never "o-Ps senses oxygen."

## Deliverables (Codex+Claude convergent plan) — TECHNICAL PART COMPLETE
1. Non-identifiability from τ alone (rate-additivity → rank-1 Fisher). ✅ `identifiability.py` + fig4
2. Lipid-O2 bias map in mmHg (κ_lipid swept). ✅ `forward.naive_bias_mmHg` + fig1, fig2
3. 2-parameter CRLB for (τ, I3). ✅ analytic + Poisson-spectrum + **nuisance-profiled** (`spectrum_fim.py`) + fig3
4. Separable/impossible boundary (counts / ROI volume / isotope). ✅ `voxel_sim.py` + fig5, fig6
5. Decisive PALS experiment (O2 × lipid/water/protein → κ_lipid, ∂I3/∂composition). ✅ spec in manuscript §5
6. Monte-Carlo recovery under the assumed spectrum model. ✅ fixed-nuisance Poisson CRLB attainability + figS1

## Headline results (robust across noise models)
- **Bias:** even 2-5% lipid throws the naive hypoxia read by hundreds of mmHg → composition-dominated.
- **τ alone:** structurally non-identifiable (rank-1 Fisher).
- **(τ, I3) rescue:** real but weak — σ(pO2) ~330-760 mmHg @ N3=1e5 (bracket: optimistic→nuisance-profiled).
- **Linchpin (model-corrected):** separability needs a non-collinear Jacobian; in the pessimistic ∂I3/∂pO2≈0 case, it needs **∂I3/∂composition ≠ 0**.
- **Feasibility:** clinical pO2 separation (<=10 mmHg) needs **liters** of pooled ROI even with I-124 ->
  infeasible at native voxel scale (needs ~10^5-10^6x effective o-Ps yield: 8e4x best-case
  I-124/60% lipid to 2e6x for Rb-82/5%; the ~10^3-10^4x figure only holds for a pooled ~5 mL ROI).
- **Monte Carlo:** the MLE reaches the fixed-nuisance Poisson CRLB under the forward model (pull std ~1.00);
  this validates estimator attainability, not the unmeasured biological constants.

## Status (v0, this session)
- Core engine built + verified; headline numbers in `results/01_headline.txt`.
- Numbers are physically calibrated (water sensitivity ~0.09 ps/mmHg matches
  Shibuya; ~3e8 counts for 10 mmHg matches the field).
- **Correction the model surfaced:** the formal separability condition is a non-collinear
  Jacobian. In the pessimistic case where oxygen does not move I3, composition must move I3.
- Monte-Carlo validation is integrated into `./run_all.sh`; the remaining empirical anchor is physical
  validation of κ_lipid and the I3 slopes.

## Two LOAD-BEARING UNKNOWNS (what deliverable #5 measures)
- **κ_lipid** — o-Ps O2 quenching constant in biological lipid-like media (sets bias magnitude).
- **∂I3/∂composition** — must be non-zero for separability (the real linchpin).

## Run
```
python3 run/01_headline.py
```

## Manuscript
- `paper/manuscript_ejnmmi.md` — **canonical single submission manuscript** for EJNMMI:
  Original Article structure, structured abstract, statements/declarations, 6 separate main
  figures, 4 tables, and one Online Resource. This is the source to submit.
- `paper/submission_ejnmmi/` — **complete EJNMMI submission bundle, ready to upload**:
  EJNMMI-formatted manuscript (PDF + DOCX), cover letter (PDF + DOCX), Online Resource 1
  (Monte-Carlo supplement), Fig1-Fig6, and the submission checklist. See
  `paper/submission_ejnmmi/README.md` for the upload list.
- `paper/manuscript.md` — extended development/preprint draft retained for provenance and
  audit history; it is not the active submission source.

  Target order: EJNMMI main, then EJNMMI Physics / PMB / IEEE TRPMS depending on reviewer fit.
  Preprint on bioRxiv/medRxiv only after author review. The decisive experiment spec is in the Discussion.

## Remaining
- Author final read-through and EditorialManager metadata entry.
- Journal-strength empirical anchor: a real-data I3 re-analysis or a minimal PALS measurement.
- Optional robustness: profile-nuisance Monte Carlo if a reviewer demands estimator validation
  under the conservative nuisance model.

## Run everything
```
./run_all.sh
```

To reproduce **only the numerical results and figures** (no PDF toolchain needed):
```
./run_results.sh
```
To build **only the PDFs** from the sources (needs `pandoc` + `xelatex`):
```
./build_paper.sh
```

Use a specific environment with:
```
PYTHON=/path/to/python ./run_all.sh      # (also honored by ./run_results.sh)
```

Python dependencies are listed in `requirements.txt`; PDF compilation also needs `pandoc`
and `xelatex`. `pdfinfo` is optional and only records the PDF metadata.

The paper build is **incremental and reproducible**: a document is rebuilt only when its
source is newer, and embedded dates are pinned via `SOURCE_DATE_EPOCH` (default: the HEAD
commit time). Re-running the pipeline therefore leaves git clean unless a source changed.
Override the date with `SOURCE_DATE_EPOCH=<unix-time> ./build_paper.sh` if needed.

## License
- Code: MIT (`LICENSE-CODE.md`).
- Manuscript text, tables, and figures: CC-BY-4.0 (`LICENSE-TEXT-FIGURES.md`).

## Constants & sources
See `src/constants.py` (core numeric values sourced; the two unknowns flagged).
