"""
Forward model: tissue state (pO2, f_lipid) -> observables (tau3, I3).
Plus the 'naive reader' inversion used for the lipid-O2 bias map.

f_lipid in [0,1] is the lipid (free-volume-rich) fraction of a 2-compartment
tissue. The model is deliberately minimal and transparent; modeling choices are
documented inline.
"""
import numpy as np
from constants import (TAU_WATER, TAU_LIPID, KAPPA_WATER, ALPHA_WATER, ALPHA_LIPID,
                       I3_WATER, I3_LIPID, KAPPA_LIPID_RATIO_DEFAULT, DI3_DPO2_DEFAULT)


def q_slope(f, kappa_lipid_ratio=KAPPA_LIPID_RATIO_DEFAULT):
    """O2 quenching slope d(1/tau)/dpO2 = kappa*alpha, mixed by lipid fraction.
    Units: 1/(ns*mmHg)."""
    q_water = KAPPA_WATER * ALPHA_WATER
    q_lipid = (KAPPA_WATER * kappa_lipid_ratio) * ALPHA_LIPID
    return (1.0 - f) * q_water + f * q_lipid


def tau0(f):
    """Baseline o-Ps lifetime (zero O2) at lipid fraction f.
    Intensity-weighted 2-compartment mean (modeling choice)."""
    return (1.0 - f) * TAU_WATER + f * TAU_LIPID


def tau3(pO2, f, kappa_lipid_ratio=KAPPA_LIPID_RATIO_DEFAULT):
    """Observed o-Ps lifetime, exact rate form 1/tau = 1/tau0 + q*pO2."""
    lam = 1.0 / tau0(f) + q_slope(f, kappa_lipid_ratio) * pO2
    return 1.0 / lam


def sensitivity(f, kappa_lipid_ratio=KAPPA_LIPID_RATIO_DEFAULT):
    """O2 sensitivity |dtau/dpO2| in ns/mmHg near pO2~0: tau0^2 * q."""
    return tau0(f) ** 2 * q_slope(f, kappa_lipid_ratio)


def I3(f, pO2=0.0, dI3_dpO2=DI3_DPO2_DEFAULT, i3_contrast=None):
    """o-Ps intensity. Composition slope dI3/df = i3_contrast (default
    I3_LIPID-I3_WATER); ~independent of pO2 unless dI3_dpO2 != 0.
    i3_contrast is the REAL linchpin of separability: if it -> 0, I3 carries no
    composition info and identifiability collapses."""
    if i3_contrast is None:
        i3_contrast = I3_LIPID - I3_WATER
    return I3_WATER + i3_contrast * f + dI3_dpO2 * pO2


# --- the naive reader: assumes pure water (f=0) and inverts tau -> pO2 ---
def naive_pO2(tau_obs):
    q_w = KAPPA_WATER * ALPHA_WATER
    return (1.0 / tau_obs - 1.0 / TAU_WATER) / q_w


def naive_bias_mmHg(pO2_true, f, kappa_lipid_ratio=KAPPA_LIPID_RATIO_DEFAULT):
    """Apparent-pO2 error (mmHg) from ignoring composition (assuming f=0)."""
    tau_obs = tau3(pO2_true, f, kappa_lipid_ratio)
    return naive_pO2(tau_obs) - pO2_true
