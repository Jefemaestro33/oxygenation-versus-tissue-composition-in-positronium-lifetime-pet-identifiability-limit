"""
Fisher information / CRLB for theta = (pO2, f_lipid).

Core result:
  * from tau alone  -> 1 observable, 2 params -> rank-1 Fisher -> NON-identifiable.
  * from (tau, I3)  -> 2 observables          -> full rank     -> identifiable,
                       provided the (lambda3,I3) Jacobian is not collinear. In
                       the pessimistic dI3/dpO2=0 case, I3 must carry
                       composition information (dI3/df != 0).

Noise model is illustrative (anchored to the field's count-vs-precision scaling);
the rigorous Poisson-spectrum FIM with the tau3-I3 fit covariance is the 'full
version'. Flagged inline.
"""
import numpy as np
import forward as fwd
from constants import KAPPA_LIPID_RATIO_DEFAULT, DI3_DPO2_DEFAULT


def sigma_tau_from_counts(tau, N3):
    """o-Ps lifetime precision. Anchored to Front-4 field value ~60 ps at
    N3=1e5 o-Ps counts (large effective F-value from flat bg + IRF), 1/sqrt(N)."""
    return 0.060 * np.sqrt(1e5 / N3) * (tau / 2.0)   # ns


def sigma_I3_from_counts(I3val, N3):
    """o-Ps intensity precision ~ I3/sqrt(N3) (illustrative).
    NOTE: real value is inflated by the tau3-I3 fit covariance (full version)."""
    return I3val / np.sqrt(N3)


def _jacobian(pO2, f, kr, dI3_dpO2, i3_contrast, ep=1e-3, ef=1e-4):
    """d[lambda3, I3]/d[pO2, f] by central differences; lambda3 = 1/tau3."""
    lam = lambda p, x: 1.0 / fwd.tau3(p, x, kr)
    i3 = lambda p, x: fwd.I3(x, p, dI3_dpO2, i3_contrast)
    dlam_dp = (lam(pO2 + ep, f) - lam(pO2 - ep, f)) / (2 * ep)
    dlam_df = (lam(pO2, f + ef) - lam(pO2, f - ef)) / (2 * ef)
    di3_dp = (i3(pO2 + ep, f) - i3(pO2 - ep, f)) / (2 * ep)
    di3_df = (i3(pO2, f + ef) - i3(pO2, f - ef)) / (2 * ef)
    return dlam_dp, dlam_df, di3_dp, di3_df


def fisher(pO2, f, N3, kappa_lipid_ratio=KAPPA_LIPID_RATIO_DEFAULT,
           dI3_dpO2=DI3_DPO2_DEFAULT, i3_contrast=None, use_I3=True):
    """Return (F 2x2, cov 2x2 or None if singular)."""
    tau = fwd.tau3(pO2, f, kappa_lipid_ratio)
    I3v = fwd.I3(f, pO2, dI3_dpO2, i3_contrast)
    sig_lam = sigma_tau_from_counts(tau, N3) / tau ** 2     # sigma on lambda=1/tau
    dlam_dp, dlam_df, di3_dp, di3_df = _jacobian(pO2, f, kappa_lipid_ratio,
                                                 dI3_dpO2, i3_contrast)
    rows = [(np.array([dlam_dp, dlam_df]), sig_lam)]
    if use_I3:
        rows.append((np.array([di3_dp, di3_df]), sigma_I3_from_counts(I3v, N3)))
    F = np.zeros((2, 2))
    for J, sig in rows:
        F += np.outer(J, J) / sig ** 2
    try:
        cov = np.linalg.inv(F)
        if np.any(np.diag(cov) <= 0):
            cov = None
    except np.linalg.LinAlgError:
        cov = None
    return F, cov


def report_point(pO2, f, N3, **kw):
    out = {}
    for tag, use_I3 in [("tau-only", False), ("tau+I3", True)]:
        F, cov = fisher(pO2, f, N3, use_I3=use_I3, **kw)
        det = float(np.linalg.det(F))
        ev = np.linalg.eigvalsh(F)
        cond = float(ev.max() / ev.min()) if ev.min() > 0 else np.inf
        if cov is not None:
            s_p = float(np.sqrt(cov[0, 0]))
            s_f = float(np.sqrt(cov[1, 1]))
            rho = float(cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1]))
        else:
            s_p = s_f = rho = np.inf
        out[tag] = dict(det=det, cond=cond, sigma_pO2=s_p, sigma_f=s_f, rho=rho)
    return out


def counts_for_pO2_precision(target_mmHg, pO2, f, **kw):
    """Counts N3 needed (tau+I3) for sigma(pO2) <= target, via 1/sqrt(N) scaling."""
    N0 = 1e5
    s0 = report_point(pO2, f, N0, **kw)["tau+I3"]["sigma_pO2"]
    if not np.isfinite(s0):
        return np.inf
    return N0 * (s0 / target_mmHg) ** 2
