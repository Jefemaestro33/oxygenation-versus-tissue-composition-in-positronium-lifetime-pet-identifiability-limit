"""Deliverable #4 capstone: realistic separability boundary + virtual-tumor map."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import voxel_sim as vx

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "figures")
os.makedirs(OUT, exist_ok=True)
DPI = 600
L = "=" * 72
print(L); print("SEPARABILITY BOUNDARY (realistic counts) + virtual tumor"); print(L)

# --- table: ROI volume (mL) needed for sigma(pO2)<=10 mmHg at hypoxic pO2=10 ---
print("\nROI volume needed to separate pO2 (<=10 mmHg) from composition, pO2=10:")
print(f"  {'f_lipid':>8} | {'I-124':>10} {'Ga-68':>10} {'Rb-82':>10}   (mL)")
for f in [0.05, 0.10, 0.30, 0.60]:
    vols = [vx.volume_for_precision(10.0, f, 10.0, iso) for iso in ("I-124", "Ga-68", "Rb-82")]
    s = "  ".join(f"{v:9.1f}" for v in vols)
    print(f"  {f:8.2f} |  {s}")
print("  (4 mm clinical voxel = 0.064 mL; small ROI ~5 mL; whole organ ~1000 mL)")
print("  -> at low lipid the required volume is enormous (lipid raises O2 sensitivity,")
print("     so fatty tissue is paradoxically 'easier' -- but also more biased).")

# --- Fig 5: boundary curves ---
ff = np.linspace(0.02, 0.65, 40)
fig, ax = plt.subplots(figsize=(6.2, 4.6))
for iso, c in [("I-124", "C0"), ("Ga-68", "C1"), ("Rb-82", "C3")]:
    v = [vx.volume_for_precision(10.0, x, 10.0, iso) for x in ff]
    ax.semilogy(ff, v, lw=2, color=c, label=iso)
for vol, lab in [(0.064, "4 mm voxel"), (5, "small ROI"), (1000, "whole organ ~1 L")]:
    ax.axhline(vol, ls=":", color="gray")
    ax.text(0.62, vol * 1.3, lab, fontsize=7, ha="right", color="gray")
ax.set_xlabel("lipid fraction $f_{lipid}$")
ax.set_ylabel("ROI volume for $\\sigma$(pO$_2$)$\\leq$10 mmHg (mL)")
ax.legend(); fig.tight_layout(); fig.savefig(f"{OUT}/fig5_boundary.png", dpi=DPI); plt.close(fig)
print("\nwrote fig5_boundary.png")

# --- Fig 6: virtual tumor, viable/marginal/impossible at native 4 mm voxel ---
pO2, f = vx.virtual_tumor(60)
VOX_ML = 0.064   # 4 mm voxel
states = {}                      # cache sigma per unique (pO2,f)
def classify(p, x):
    key = (round(p, 2), round(x, 3))
    if key not in states:
        s = vx.sigma_pO2(VOX_ML, x, p, isotope="Ga-68", profiled=True)
        states[key] = 0 if s > 30 else (1 if s > 10 else 2)   # imposs/marg/viable
    return states[key]
cls = np.vectorize(classify)(pO2, f)
cmap = ListedColormap(["#b2182b", "#fee08b", "#1a9850"])
fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.2))
axs[0].imshow(pO2, cmap="viridis"); axs[0].axis("off")
im = axs[1].imshow(cls, cmap=cmap, norm=BoundaryNorm([-.5, .5, 1.5, 2.5], 3))
axs[1].axis("off")
cb = fig.colorbar(im, ax=axs[1], ticks=[0, 1, 2])
cb.ax.set_yticklabels(["impossible", "marginal", "viable"])
fig.tight_layout(); fig.savefig(f"{OUT}/fig6_tumor_map.png", dpi=DPI); plt.close(fig)
print("wrote fig6_tumor_map.png")
uniq, cnt = np.unique(cls, return_counts=True)
frac = {int(u): c / cls.size for u, c in zip(uniq, cnt)}
print(f"  voxel-level verdict: impossible={frac.get(0,0)*100:.0f}%  "
      f"marginal={frac.get(1,0)*100:.0f}%  viable={frac.get(2,0)*100:.0f}%")
print(L)
