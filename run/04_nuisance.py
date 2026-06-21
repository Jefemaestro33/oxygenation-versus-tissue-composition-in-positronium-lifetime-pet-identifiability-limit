"""The truly rigorous bound: CRLB on pO2 as spectral nuisances are profiled."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import spectrum_fim as sfim

L = "=" * 72
print(L); print("NUISANCE-PROFILED CRLB (rigorous bound)"); print(L)
print("scenario: pO2=20, f_lipid=0.10; N_total=1.1e6 (<=> N3~1e5 o-Ps)\n")
N = 1.1e6

cases = [
    ("nuisances FIXED (optimistic)", []),
    ("profile bg + fast comp (realistic)", ["bg", "fast"]),
    ("profile bg+fast+t0 (conservative)", ["bg", "fast", "t0"]),
    ("profile ALL incl IRF sigma (pessimistic)", ["bg", "fast", "t0", "sigma"]),
]
base = None
for label, prof in cases:
    if not prof:
        s = sfim.crlb(20.0, 0.10, N)["sigma_pO2"]
    else:
        s = sfim.crlb_profiled(20.0, 0.10, N, profile=tuple(prof))["sigma_pO2"]
    if base is None:
        base = s
    fac = s / base
    print(f"  {label:42s}: sigma(pO2) = {s:8.1f} mmHg   ({fac:4.1f}x)")
print("\n  -> profiling the per-spectrum nuisances (bg, fast comp) inflates the bound;")
print("     IRF (sigma,t0) is normally CALIBRATED from the prompt -> keep it fixed.")
print("     Realistic rigorous number = the 'profile bg+fast' row.")
print(L)
