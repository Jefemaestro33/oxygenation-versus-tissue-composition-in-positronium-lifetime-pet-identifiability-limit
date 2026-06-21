"""
Counts-from-scanner model + per-voxel separability (deliverable #4 capstone).

Translates the CRLB into clinically meaningful terms: given a realistic o-Ps
triple-coincidence yield, what ROI VOLUME (pooling) is needed to separate pO2
from composition, as a function of lipid fraction and isotope?
"""
import numpy as np
import forward as fwd
import spectrum_fim as sfim

# o-Ps triple-coincidence yield, field-anchored:
# Sc-44 (arXiv:2506.13460): a ~5.57 mL ROI reached tau to ~5% -> ~3.6e4 o-Ps counts.
OPS_COUNTS_PER_ML = 6.5e3
# Relative effective o-Ps yield by isotope (prompt branching / pSBR). These are
# scenario-level scalings, not universal measured constants.
ISOTOPE_FACTOR = {"I-124": 4.0, "Ga-68": 1.0, "Sc-44": 1.0, "Rb-82": 0.6}


def n3_for_volume(vol_mL, isotope="Ga-68"):
    return OPS_COUNTS_PER_ML * vol_mL * ISOTOPE_FACTOR.get(isotope, 1.0)


def ntotal_from_n3(N3, f, pO2, bg_frac=sfim.BG_FRAC):
    I3 = fwd.I3(f, pO2)
    return N3 / max(I3 * (1 - bg_frac), 1e-6)


def sigma_pO2(vol_mL, f, pO2, isotope="Ga-68", profiled=True):
    N3 = n3_for_volume(vol_mL, isotope)
    Nt = ntotal_from_n3(N3, f, pO2)
    if profiled:
        return sfim.crlb_profiled(pO2, f, Nt)["sigma_pO2"]
    return sfim.crlb(pO2, f, Nt)["sigma_pO2"]


def volume_for_precision(target_mmHg, f, pO2, isotope="Ga-68", profiled=True):
    """ROI volume (mL) needed for sigma(pO2) <= target; sigma ~ 1/sqrt(vol)."""
    s1 = sigma_pO2(1.0, f, pO2, isotope, profiled)   # at 1 mL reference
    if not np.isfinite(s1):
        return np.inf
    return (s1 / target_mmHg) ** 2


def virtual_tumor(n=60):
    """A 2D phantom: hypoxic core, normoxic rim, normal tissue, a fatty patch.
    Returns (pO2_map, f_map) on an n x n grid (~24 cm field, 4 mm pixels)."""
    y, x = np.mgrid[0:n, 0:n].astype(float)
    cx, cy = n * 0.45, n * 0.5
    r = np.hypot(x - cx, y - cy)
    pO2 = np.full((n, n), 40.0)     # normal tissue normoxic
    f = np.full((n, n), 0.05)       # lean-ish
    rim = r < n * 0.22              # tumor
    core = r < n * 0.10             # hypoxic necrotic core
    pO2[rim] = 28.0
    pO2[core] = 5.0
    f[core] = 0.12                  # necrosis: somewhat more lipid
    # an adjacent fatty region (e.g., adipose / fatty organ)
    fatty = (x > n * 0.75)
    f[fatty] = 0.70
    pO2[fatty] = 40.0
    return pO2, f
