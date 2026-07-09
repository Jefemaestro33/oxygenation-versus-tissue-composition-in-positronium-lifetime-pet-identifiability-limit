"""Figures for the identifiability / lipid-O2 bias paper."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import forward as fwd
import identifiability as idf
import spectrum_fim as sfim

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "figures")
os.makedirs(OUT, exist_ok=True)
DPI = 600


# --- Fig 1: the naive-reader bias surface ---
def fig_bias():
    f = np.linspace(0, 0.30, 121)
    p = np.linspace(0, 60, 121)
    F, P = np.meshgrid(f, p)
    B = np.vectorize(lambda ff, pp: fwd.naive_bias_mmHg(pp, ff))(F, P)
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    im = ax.pcolormesh(F, P, B, cmap="RdBu_r", vmin=-1500, vmax=1500, shading="auto")
    cs = ax.contour(F, P, np.abs(B), levels=[10], colors="k", linewidths=2)
    ax.clabel(cs, fmt={10: "|error|=10 mmHg"}, fontsize=8)
    ax.set_xlabel("lipid fraction $f_{lipid}$"); ax.set_ylabel("true pO$_2$ (mmHg)")
    fig.colorbar(im, label="apparent pO$_2$ error (mmHg)")
    ax.text(0.012, 30, "only here\nis the read\nusable", fontsize=8, va="center")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig1_bias_surface.png", dpi=DPI); plt.close(fig)


# --- Fig 2: O2 sensitivity vs composition, kappa_lipid uncertainty band ---
def fig_sensitivity():
    f = np.linspace(0, 1, 101)
    lo = np.array([fwd.sensitivity(x, 0.1) * 1000 for x in f])
    hi = np.array([fwd.sensitivity(x, 1.0) * 1000 for x in f])
    mid = np.array([fwd.sensitivity(x, 0.3) * 1000 for x in f])
    stress3 = np.array([fwd.sensitivity(x, 3.0) * 1000 for x in f])
    stress10 = np.array([fwd.sensitivity(x, 10.0) * 1000 for x in f])
    fig, ax = plt.subplots(figsize=(6.0, 4.4))
    ax.fill_between(f, lo, hi, alpha=0.25, label=r"baseline sweep (0.1$\times$-1.0$\times$ water)")
    ax.plot(f, mid, lw=2, label=r"central ($0.3\times$)")
    ax.plot(f, stress3, lw=1.6, ls="--", label=r"high stress ($3\times$)")
    ax.plot(f, stress10, lw=1.6, ls=":", label=r"organic-liquid stress ($10\times$)")
    ax.set_xlabel("lipid fraction $f_{lipid}$"); ax.set_ylabel("O$_2$ sensitivity |d$\\tau$/dpO$_2$| (ps/mmHg)")
    ax.legend(); fig.tight_layout(); fig.savefig(f"{OUT}/fig2_sensitivity.png", dpi=DPI); plt.close(fig)


# --- Fig 3: separability -- sigma(pO2) vs counts ---
def fig_separability():
    N = np.logspace(6, 10, 30)
    sig = np.array([sfim.crlb(20.0, 0.10, n)["sigma_pO2"] for n in N])
    fig, ax = plt.subplots(figsize=(6.0, 4.4))
    ax.loglog(N, sig, lw=2, label=r"full spectrum ($\tau_3$ + $I_3$)")
    ax.axhline(10, ls="--", color="g", label="clinically useful (10 mmHg)")
    ax.axhline(1e4, ls=":", color="r", label=r"$\tau$ alone: $\infty$ (non-identifiable)")
    ax.set_xlabel("in-window events $N_{total}$"); ax.set_ylabel(r"CRLB $\sigma$(pO$_2$) (mmHg)")
    ax.legend(fontsize=8); fig.tight_layout()
    fig.savefig(f"{OUT}/fig3_separability.png", dpi=DPI); plt.close(fig)


# --- Fig 4: WHY (tau, I3) breaks the degeneracy ---
def fig_degeneracy():
    f = np.linspace(0.0, 0.30, 200)
    p = np.linspace(0, 60, 200)
    F, P = np.meshgrid(f, p)
    TAU = np.vectorize(lambda ff, pp: fwd.tau3(pp, ff))(F, P)
    I3 = np.vectorize(lambda ff: fwd.I3(ff))(F)
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    c1 = ax.contour(F, P, TAU, levels=8, colors="C0", linewidths=1)
    c2 = ax.contour(F, P, I3, levels=6, colors="C3", linewidths=1, linestyles="--")
    ax.clabel(c1, fmt="%.2f", fontsize=7)
    h1 = plt.Line2D([], [], color="C0", label=r"iso-$\tau_3$  (degenerate dir.: $\tau$ alone)")
    h2 = plt.Line2D([], [], color="C3", ls="--", label=r"iso-$I_3$  (composition handle)")
    ax.legend(handles=[h1, h2], fontsize=8, loc="upper right")
    ax.set_xlabel("lipid fraction $f_{lipid}$"); ax.set_ylabel("pO$_2$ (mmHg)")
    ax.annotate("shallow tilt = the\nonly pO$_2$ information",
                xy=(0.14, 45), xytext=(0.04, 52), fontsize=7,
                arrowprops=dict(arrowstyle="->", color="C0"))
    fig.tight_layout(); fig.savefig(f"{OUT}/fig4_degeneracy.png", dpi=DPI); plt.close(fig)


for fn in [fig_bias, fig_sensitivity, fig_separability, fig_degeneracy]:
    fn(); print("wrote", fn.__name__)
print("figures in", os.path.relpath(OUT))
