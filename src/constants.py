"""
Physical constants for the o-Ps oxygenation-vs-composition identifiability /
lipid-O2 bias analysis.

Units: lifetime in ns, rate in ns^-1, pO2 in mmHg, [O2] in uM.
Core numeric values are sourced. The two LOAD-BEARING UNKNOWNS are flagged explicitly --
they are exactly what the decisive experiment (deliverable #5) must measure.
"""

# --- o-Ps baseline lifetimes tau0 (MEASURED) ---
TAU_WATER  = 1.815   # ns, operational water reference; Steinberger EJNMMI Phys 2024, consistent with 124I LAFOV ~1.82 ns
TAU_LIPID  = 2.60    # ns, adipose tissue; Avachat et al., Sci Rep 2024, PMID 39256482 / PMC11387643 (range 2.5-2.7)
TAU_MUSCLE = 2.03    # ns, reference; Sci Rep 2024
TAU_LIVER  = 2.04    # ns, reference; Sci Rep 2024

# --- O2 quenching of o-Ps (MEASURED in water) ---
# Mechanism: ortho->para spin conversion (oxidation 5-10x less; Stepanov 2020).
# Rate law: 1/tau = 1/tau0 + kappa * [O2]    (Shibuya 2020; Stepanov 2020 agree <10%)
KAPPA_WATER = 0.0204e-3   # 1/(uM*ns)   [0.0204 /uM/us / 1000]

# --- O2 solubility (MEASURED) ---
ALPHA_WATER = 1.3              # uM/mmHg, dissolved O2 in water at 37C (Henry)
SOLUBILITY_RATIO_LIPID = 5.0   # O2 ~5x more soluble in bulk lipid; Battino 1968, Roppongi 2021
ALPHA_LIPID = ALPHA_WATER * SOLUBILITY_RATIO_LIPID

# === LOAD-BEARING UNKNOWN #1 (ASSUMPTION; deliverable #5 measures it) ===
# o-Ps O2 quenching constant in biological lipid-like media is unmeasured.
# Front-2 estimate: 3-10x LOWER than water (viscosity) -> sweep the ratio.
KAPPA_LIPID_RATIO_DEFAULT = 0.3        # central guess
KAPPA_LIPID_RATIO_SWEEP = (0.1, 1.0)   # honest range

# --- o-Ps intensity I3 (ILLUSTRATIVE placeholders; deliverable #5 calibrates) ---
# Composition changes I3 (number of free-volume sites); needed to break degeneracy.
I3_WATER = 0.15
I3_LIPID = 0.30

# === LOAD-BEARING UNKNOWN #2 (ASSUMPTION; deliverable #5 measures it) ===
# Formal separability requires a non-collinear Jacobian for (lambda3,I3) vs
# (pO2,f). In the pessimistic case dI3/dpO2=0, the needed handle is dI3/df != 0.
DI3_DPO2_DEFAULT = 0.0
