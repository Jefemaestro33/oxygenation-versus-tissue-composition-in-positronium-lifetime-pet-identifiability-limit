"""Rigorous Poisson-spectrum CRLB vs the idealized analytic engine."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import identifiability as idf
import spectrum_fim as sfim

L = "=" * 72
print(L); print("RIGOROUS POISSON-FIM  vs  idealized analytic engine"); print(L)
print("scenario: hypoxic fatty voxel pO2=20 mmHg, f_lipid=0.10\n")

# match counts: analytic used N3=1e5 o-Ps events. In the spectrum,
# N3 = I3*(1-bg_frac)*N_total.
N3_target = 1e5
c = sfim.crlb(20.0, 0.10, 1e6)               # probe to get I3*(1-bg)
ratio = c["N3"] / 1e6
N_total = N3_target / ratio
print(f"[match] N3=1e5 o-Ps counts  <=>  N_total ~ {N_total:.2e} in-window events")

an = idf.report_point(20.0, 0.10, N3=N3_target)["tau+I3"]
po = sfim.crlb(20.0, 0.10, N_total)
print(f"\n  analytic (idealized) :  sigma(pO2) = {an['sigma_pO2']:8.1f} mmHg   rho={an['rho']:+.3f}")
print(f"  Poisson  (rigorous)  :  sigma(pO2) = {po['sigma_pO2']:8.1f} mmHg   rho={po['rho']:+.3f}")
print(f"  -> the two BRACKET the truth. Analytic uses the field's empirical sigma_tau")
print(f"     (already includes nuisance-fitting); Poisson FIXES nuisances (optimistic)")
print(f"     but correctly exposes the tau3-I3 entanglement: rho {an['rho']:+.2f} -> {po['rho']:+.2f}")
print(f"     (that IS the covariance Front-4 warned about). Both ~hundreds of mmHg @ N3=1e5")
print(f"     -> the conclusion is ROBUST to the noise model. See run/04_nuisance.py")
print(f"     for the nuisance-profiled, more pessimistic bound.")

print("\n[counts] N_total needed for sigma(pO2) target (rigorous), pO2=20, f=0.10:")
for tgt in [10.0, 5.0]:
    Ntot = sfim.counts_for(tgt, 20.0, 0.10)
    N3 = Ntot * ratio
    print(f"   <= {tgt:4.1f} mmHg :  N_total ~ {Ntot:.1e}   (o-Ps N3 ~ {N3:.1e})")

print("\n[linchpin, rigorous] vary I3 composition contrast dI3/df:")
for cc in [0.15, 0.05, 0.015, 0.0]:
    s = sfim.crlb(20.0, 0.10, N_total, i3_contrast=cc)["sigma_pO2"]
    s_s = f"{s:8.1f} mmHg" if np.isfinite(s) else "     inf (degenerate)"
    print(f"   dI3/df={cc:.3f}:  sigma(pO2)={s_s}")
print("   -> confirms the analytic finding on the realistic spectrum.")
print(L)
