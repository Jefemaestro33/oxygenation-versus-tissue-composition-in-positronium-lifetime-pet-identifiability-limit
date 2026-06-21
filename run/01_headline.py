"""Headline numbers for the identifiability paper."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import forward as fwd
import identifiability as idf

L = "=" * 72
print(L); print("PLI IDENTIFIABILITY -- HEADLINE NUMBERS"); print(L)

print("\n[A] O2 sensitivity |dtau/dpO2| (ps/mmHg), with kappa_lipid sweep 0.1x-1.0x:")
for f in [0.0, 0.1, 0.5, 1.0]:
    lo = fwd.sensitivity(f, 0.1) * 1000
    hi = fwd.sensitivity(f, 1.0) * 1000
    print(f"    f_lipid={f:.1f}:   {lo:6.3f}  -  {hi:6.3f}")
print(f"    -> water ~ {fwd.sensitivity(0.0)*1000:.3f} ps/mmHg (matches Shibuya ~0.1);"
      f" the [1x-10x] lipid spread IS the kappa_lipid uncertainty")

print("\n[B] NAIVE-READER BIAS -- composition masquerading as oxygen")
print("    true tissue at pO2 = 20 mmHg (hypoxic); reader assumes pure water:")
for f in [0.00, 0.02, 0.05, 0.10, 0.20]:
    b = fwd.naive_bias_mmHg(20.0, f)
    print(f"    f_lipid={f:.2f}:   apparent pO2 error = {b:+8.0f} mmHg")
print("    -> even 2-5% lipid drives the apparent pO2 hundreds of mmHg off (even negative):")
print("       from tau alone the hypoxia read is composition-DOMINATED, not oxygen.")

print("\n[C] IDENTIFIABILITY at a hypoxic fatty voxel (pO2=20, f_lipid=0.10), N3=1e5:")
r = idf.report_point(20.0, 0.10, N3=1e5)
for tag in ["tau-only", "tau+I3"]:
    d = r[tag]
    sp = f"{d['sigma_pO2']:10.1f}" if np.isfinite(d['sigma_pO2']) else "       inf"
    cond = f"{d['cond']:.2e}" if np.isfinite(d['cond']) else "inf"
    print(f"    {tag:9s}: det(F)={d['det']:.2e}  cond={cond:>9}  "
          f"sigma(pO2)={sp} mmHg  rho={d['rho']:+.3f}")
print("    -> tau-only: RANK-1, sigma(pO2)=inf  ==> STRUCTURALLY non-identifiable")
print("    -> tau+I3 : full-rank, finite        ==> rescued (but statistics-limited)")

print("\n[C2] Counts needed for clinically-useful pO2 precision (tau+I3):")
for tgt in [10.0, 5.0]:
    N = idf.counts_for_pO2_precision(tgt, 20.0, 0.10)
    print(f"    sigma(pO2) <= {tgt:4.1f} mmHg  ->  N3 ~ {N:.1e} o-Ps counts")
print("    -> ~1e8-1e9 counts: matches the field's ~3e8 estimate -> regional pooling only.")

print("\n[D] THE REAL LINCHPIN: does composition move I3?  (vary dI3/df)")
c0 = 0.30 - 0.15   # default I3 composition contrast (I3_LIPID - I3_WATER)
for c in [c0, c0 * 0.3, c0 * 0.1, 0.0]:
    s = idf.report_point(20.0, 0.10, N3=1e5, i3_contrast=c)["tau+I3"]["sigma_pO2"]
    s_s = f"{s:8.1f} mmHg" if np.isfinite(s) else "     inf  (degenerate again)"
    print(f"    dI3/df = {c:.3f}:   sigma(pO2) = {s_s}")
print("    -> as I3's COMPOSITION sensitivity -> 0, identifiability COLLAPSES to inf.")
print("       THIS (not dI3/dpO2~0) is the assumption the experiment must verify.")

print("\n[E] Correction: if oxygen ALSO moves I3, it can help if gradients stay non-collinear:")
for da in [0.0, 1e-4, 1e-3]:
    s = idf.report_point(20.0, 0.10, N3=1e5, dI3_dpO2=da)["tau+I3"]["sigma_pO2"]
    print(f"    dI3/dpO2 = {da:.0e}:   sigma(pO2) = {s:8.1f} mmHg")
print("    -> dI3/dpO2~0 is the PESSIMISTIC case for this baseline, not a fragile assumption.")
print("       Formally, the requirement is det(J) != 0 for observables (lambda3,I3).")
print("       (the model corrected an over-stated 'linchpin' from the planning stage.)")
print(L)
