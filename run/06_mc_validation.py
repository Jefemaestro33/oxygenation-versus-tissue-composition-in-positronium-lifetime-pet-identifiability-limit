"""
Monte-Carlo validation of the fixed-nuisance Poisson Cramer-Rao bound.

Closes the reviewer's first statistical attack: under the assumed spectrum
model, is the fixed-nuisance CRLB achievable, or just theory? We simulate
Poisson o-Ps spectra at a known truth, fit (pO2, f) by maximum likelihood, and
check: (1) the MLE is unbiased, (2) the empirical std matches the fixed-nuisance
CRLB, (3) the pull (theta_hat - theta_true)/sigma_CRLB ~ N(0,1).

NOTE: because the O2 likelihood is nearly flat (tiny sensitivity), the optimizer
must work in CRLB-scaled coordinates, or it stalls at the start. We optimize
z = ((pO2-truth)/sigma_pO2, (f-truth)/sigma_f) with a unit-scale simplex.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from scipy.optimize import minimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import forward as fwd
import spectrum_fim as sfim

np.random.seed(0)
OUT = os.path.join(os.path.dirname(__file__), "..", "results", "figures")
T = np.linspace(-1.0, 12.0, 261)
DT = T[1] - T[0]
PO2_TRUE, F_TRUE = 20.0, 0.10
M = 250  # MC realizations per count level
DPI = 600


def model_counts(pO2, f, N_total):
    return sfim.density(T, fwd.tau3(pO2, f), fwd.I3(f, pO2)) * N_total * DT


def fit_one(n, N_total, s_p, s_f):
    """MLE in CRLB-scaled coords z=(dpO2/s_p, df/s_f); unit-scale simplex."""
    def nll_z(z):
        m = model_counts(PO2_TRUE + z[0] * s_p, F_TRUE + z[1] * s_f, N_total)
        m = np.maximum(m, 1e-12)
        return float(np.sum(m - n * np.log(m)))
    simplex = np.array([[0.0, 0.0], [1.5, 0.0], [0.0, 1.5]])
    res = minimize(nll_z, x0=[0.0, 0.0], method="Nelder-Mead",
                   options=dict(initial_simplex=simplex, xatol=1e-3,
                                fatol=1e-6, maxiter=4000))
    return PO2_TRUE + res.x[0] * s_p, F_TRUE + res.x[1] * s_f


L = "=" * 72
print(L); print("MONTE-CARLO VALIDATION OF THE FIXED-NUISANCE POISSON CRLB"); print(L)
print(f"truth: pO2={PO2_TRUE}, f={F_TRUE};  {M} realizations per level\n")

pulls = []
for N_total in [8e7, 2e8]:
    cr = sfim.crlb(PO2_TRUE, F_TRUE, N_total)
    s_p, s_f = cr["sigma_pO2"], cr["sigma_f"]
    m_true = model_counts(PO2_TRUE, F_TRUE, N_total)
    ph, fh = [], []
    for _ in range(M):
        n = np.random.poisson(m_true)
        p_hat, f_hat = fit_one(n, N_total, s_p, s_f)
        ph.append(p_hat); fh.append(f_hat)
    ph, fh = np.array(ph), np.array(fh)
    pulls.extend(((ph - PO2_TRUE) / s_p).tolist())
    print(f"N_total={N_total:.0e}   N3={cr['N3']:.2e} "
          f"(fixed-nuisance CRLB: sigma_pO2={s_p:6.1f}, sigma_f={s_f:.4f})")
    print(f"   pO2:  mean={ph.mean():7.1f}   emp.std={ph.std(ddof=1):6.1f}   "
          f"emp/CRLB={ph.std(ddof=1)/s_p:.2f}")
    print(f"   f  :  mean={fh.mean():.4f}   emp.std={fh.std(ddof=1):.4f}   "
          f"emp/CRLB={fh.std(ddof=1)/s_f:.2f}\n")

pulls = np.array(pulls)
print(f"PULL (pO2_hat-truth)/sigma_CRLB:  mean={pulls.mean():+.3f}  std={pulls.std(ddof=1):.3f}")
print("  -> mean~0 & std~1 => MLE unbiased and efficient under the assumed fixed-nuisance spectrum model.")

fig, ax = plt.subplots(figsize=(5.6, 4.2))
ax.hist(pulls, bins=28, density=True, alpha=0.6, label="MC pulls")
xx = np.linspace(-4, 4, 200)
ax.plot(xx, np.exp(-xx ** 2 / 2) / np.sqrt(2 * np.pi), "r-", lw=2, label="$N(0,1)$ (CRLB)")
ax.set_xlabel(r"pull $(\hat{p}O_2 - pO_2)/\sigma_{CRLB}$"); ax.set_ylabel("density")
ax.legend(); fig.tight_layout(); fig.savefig(f"{OUT}/fig7_mc_validation.png", dpi=DPI); plt.close(fig)
print("\nwrote fig7_mc_validation.png"); print(L)
