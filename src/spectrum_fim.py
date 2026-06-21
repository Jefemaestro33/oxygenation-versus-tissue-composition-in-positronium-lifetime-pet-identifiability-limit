"""
Rigorous Poisson-spectrum Fisher information for theta = (pO2, f_lipid).

Unlike the idealized analytic engine (which treats tau and I3 as two clean
observables with hand-set noise), this builds the actual o-Ps lifetime spectrum
m(t | pO2, f) -- a 2-component EMG (fast + o-Ps) on a large flat accidental
background -- and computes the per-bin Poisson FIM. The tau3-I3 estimation
covariance that Front-4 warned about is now INCLUDED automatically, because both
pO2 and f move the o-Ps component's slope (tau3) and amplitude (I3) together.

The fixed-nuisance FIM is the optimistic spectral bound; the profiled FIM below
is the review-grade bound used for the realistic/pessimistic brackets.
"""
import numpy as np
from scipy.special import erfc
import forward as fwd
from constants import KAPPA_LIPID_RATIO_DEFAULT, DI3_DPO2_DEFAULT

# Nominal instrument / spectral nuisance values (Quadra-like). The fixed-nuisance
# FIM holds these fixed; crlb_profiled marginalizes selected nuisances.
TAU_FAST = 0.35     # ns, combined p-Ps + direct/free annihilation
SIGMA_IRF = 0.20    # ns, Gaussian timing resolution (Quadra ~210 ps)
T0 = 0.0            # ns, prompt offset
BG_FRAC = 0.45      # fraction of in-window area that is flat accidental background


def _emg(t, tau, sigma, t0):
    """Exponentially-modified Gaussian (exp decay conv Gaussian)."""
    x = t - t0
    arg = np.clip(sigma ** 2 / (2 * tau ** 2) - x / tau, -700, 700)
    return (1.0 / (2 * tau)) * np.exp(arg) * erfc((sigma / tau - x / sigma) / np.sqrt(2))


def density(t, tau_oPs, I3, tau_fast=TAU_FAST, sigma=SIGMA_IRF, t0=T0, bg_frac=BG_FRAC):
    """Normalized spectral density over the grid t (integrates to ~1)."""
    dt = t[1] - t[0]
    fast = _emg(t, tau_fast, sigma, t0); fast /= fast.sum() * dt
    ops = _emg(t, tau_oPs, sigma, t0);  ops /= ops.sum() * dt
    sig = (1 - I3) * fast + I3 * ops
    sig /= sig.sum() * dt
    bg = np.ones_like(t) / (len(t) * dt)
    return (1 - bg_frac) * sig + bg_frac * bg


def fim(pO2, f, N_total, kappa_lipid_ratio=KAPPA_LIPID_RATIO_DEFAULT,
        dI3_dpO2=DI3_DPO2_DEFAULT, i3_contrast=None, t=None,
        bg_frac=BG_FRAC, eps_p=1.0, eps_f=1e-3):
    """2x2 Poisson FIM for (pO2,f). N_total = total in-window events. Returns (F,cov)."""
    if t is None:
        t = np.linspace(-1.0, 12.0, 261)   # ~50 ps bins
    dt = t[1] - t[0]

    def dens(p, x):
        tau = fwd.tau3(p, x, kappa_lipid_ratio)
        i3 = fwd.I3(x, p, dI3_dpO2, i3_contrast)
        return density(t, tau, i3, bg_frac=bg_frac)

    m = dens(pO2, f) * N_total * dt
    dm_dp = (dens(pO2 + eps_p, f) - dens(pO2 - eps_p, f)) / (2 * eps_p) * N_total * dt
    dm_df = (dens(pO2, f + eps_f) - dens(pO2, f - eps_f)) / (2 * eps_f) * N_total * dt
    msk = m > 1e-9
    F = np.zeros((2, 2))
    F[0, 0] = np.sum(dm_dp[msk] ** 2 / m[msk])
    F[1, 1] = np.sum(dm_df[msk] ** 2 / m[msk])
    F[0, 1] = F[1, 0] = np.sum(dm_dp[msk] * dm_df[msk] / m[msk])
    try:
        cov = np.linalg.inv(F)
        if np.any(np.diag(cov) <= 0):
            cov = None
    except np.linalg.LinAlgError:
        cov = None
    return F, cov


def crlb(pO2, f, N_total, **kw):
    """Return dict with sigma(pO2) [mmHg], sigma(f), correlation, and N3 (o-Ps counts)."""
    F, cov = fim(pO2, f, N_total, **kw)
    I3v = fwd.I3(f, pO2, kw.get("dI3_dpO2", DI3_DPO2_DEFAULT), kw.get("i3_contrast"))
    N3 = I3v * (1 - kw.get("bg_frac", BG_FRAC)) * N_total
    if cov is None:
        return dict(sigma_pO2=np.inf, sigma_f=np.inf, rho=np.inf, N3=N3)
    return dict(sigma_pO2=float(np.sqrt(cov[0, 0])),
                sigma_f=float(np.sqrt(cov[1, 1])),
                rho=float(cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])),
                N3=N3)


def counts_for(target_mmHg, pO2, f, **kw):
    """N_total needed for sigma(pO2) <= target (1/sqrt(N) scaling)."""
    N0 = 1e7
    s0 = crlb(pO2, f, N0, **kw)["sigma_pO2"]
    if not np.isfinite(s0):
        return np.inf
    return N0 * (s0 / target_mmHg) ** 2


# --- nuisance-marginalized (PROFILED) CRLB: the truly rigorous bound ---
_NUIS = {"fast": ("tau_fast", 0.01), "sigma": ("sigma", 0.005),
         "t0": ("t0", 0.005), "bg": ("bg_frac", 0.01)}


def fim_full(pO2, f, N_total, profile=("bg", "fast"),
             kappa_lipid_ratio=KAPPA_LIPID_RATIO_DEFAULT,
             dI3_dpO2=DI3_DPO2_DEFAULT, i3_contrast=None, t=None):
    """FIM over (pO2, f, *profiled nuisances). Profiling = treat those spectral
    nuisances as also-fitted, so the (pO2,f) CRLB inflates honestly."""
    if t is None:
        t = np.linspace(-1.0, 12.0, 261)
    dt = t[1] - t[0]
    nominal = {"pO2": pO2, "f": f, "tau_fast": TAU_FAST, "sigma": SIGMA_IRF,
               "t0": T0, "bg_frac": BG_FRAC}
    steps = {"pO2": 1.0, "f": 1e-3}
    names = ["pO2", "f"]
    for key in profile:
        nm, st = _NUIS[key]; names.append(nm); steps[nm] = st

    def dens(pvec):
        v = dict(nominal)
        for nm, val in zip(names, pvec):
            v[nm] = val
        tau = fwd.tau3(v["pO2"], v["f"], kappa_lipid_ratio)
        i3 = fwd.I3(v["f"], v["pO2"], dI3_dpO2, i3_contrast)
        return density(t, tau, i3, v["tau_fast"], v["sigma"], v["t0"], v["bg_frac"])

    p0 = np.array([nominal[nm] for nm in names])
    m = dens(p0) * N_total * dt
    grads = []
    for i, nm in enumerate(names):
        pp = p0.copy(); pp[i] += steps[nm]
        pm = p0.copy(); pm[i] -= steps[nm]
        grads.append((dens(pp) - dens(pm)) / (2 * steps[nm]) * N_total * dt)
    k = len(names); msk = m > 1e-9
    F = np.zeros((k, k))
    for i in range(k):
        for j in range(i, k):
            F[i, j] = F[j, i] = np.sum(grads[i][msk] * grads[j][msk] / m[msk])
    return F, names


def crlb_profiled(pO2, f, N_total, profile=("bg", "fast"), **kw):
    """(pO2,f) CRLB with the chosen nuisances marginalized."""
    F, names = fim_full(pO2, f, N_total, profile=profile, **kw)
    try:
        cov = np.linalg.inv(F)
    except np.linalg.LinAlgError:
        cov = np.linalg.pinv(F)
    sp, sf = cov[0, 0], cov[1, 1]
    return dict(sigma_pO2=float(np.sqrt(sp)) if sp > 0 else np.inf,
                sigma_f=float(np.sqrt(sf)) if sf > 0 else np.inf,
                profiled=list(profile))
