# Oxygenation versus tissue composition in positronium-lifetime PET: an identifiability limit for hypoxia imaging

**Article type:** Original article

**Author:** Ernest Darell Zermeño

**Affiliations**

1. Universidad Panamericana, Mexico City, Mexico.
2. Universidad de Guadalajara, Guadalajara, Mexico.

**Corresponding author:** Ernest Darell Zermeño, 0244552@up.edu.mx

## Abstract

**Purpose.** Positronium lifetime imaging with long-axial-field-of-view PET/CT has been proposed as a biomarker of tissue oxygenation. The same lifetime, however, also depends on tissue composition. We quantified whether oxygenation and composition can be separated from positronium observables and what bias arises if composition is ignored.

**Methods.** A rate-additivity model mapped pO$_2$ and lipid fraction to the ortho-positronium lifetime $\tau_3$ and intensity $I_3$. We derived the apparent-pO$_2$ bias of a water-calibrated reader, analysed structural identifiability by Fisher information, computed Cramér-Rao bounds (CRLBs) for $(pO_2,f)$ from $(\tau_3,I_3)$ using a Poisson lifetime-spectrum model with nuisance profiling, and translated the bounds into counts and region-of-interest volumes.

**Results.** From $\tau_3$ alone, oxygenation and composition are structurally non-identifiable because both enter a single summed decay rate. Ignoring composition produced apparent-pO$_2$ errors of -178, -439 and -860 mmHg at 2%, 5% and 10% lipid for a tissue at 20 mmHg. Adding $I_3$ restored identifiability in principle, but the pO$_2$ CRLB remained 330-760 mmHg at $10^5$ ortho-positronium counts. A 10 mmHg target required litres of pooled signal even in the best-yield scenario and was not achievable at 4 mm voxel scale.

**Conclusion.** Positronium-lifetime hypoxia imaging is limited by an oxygenation-versus-composition identifiability problem. Lifetime-only maps should not be interpreted as oxygenation maps without composition control and a second observable.

**Keywords:** positronium lifetime imaging; PET/CT; hypoxia; oxygenation; identifiability; Cramér-Rao bound

## Introduction

Ortho-positronium (o-Ps), the triplet bound state formed in a fraction of positron-electron annihilations, localises in nanometre-scale free-volume regions and annihilates in matter predominantly through pick-off processes. Its lifetime is therefore sensitive to tissue microstructure and composition. Molecular oxygen provides an additional paramagnetic quenching channel through spin conversion, making the o-Ps lifetime an attractive candidate biomarker for oxygenation and tumour hypoxia [1, 2]. This is clinically relevant because hypoxic tumour regions are more resistant to radiotherapy and systemic therapy, while established nuclear-medicine hypoxia tracers have practical limitations.

The technical basis for in-vivo positronium lifetime imaging (PLI) has advanced rapidly. Dedicated multi-photon systems and long-axial-field-of-view PET/CT scanners now support in-vivo positronium measurements and regional lifetime estimates [3-6]. These developments make the oxygenation question timely. However, the o-Ps lifetime is not oxygen-specific. Across soft tissues, composition-driven lifetime variation is on the order of hundreds of picoseconds, whereas the oxygen-specific term implied by aqueous quenching calibrations is on the order of picoseconds across physiological pO$_2$ differences [1, 7]. Calibrations performed in water or aqueous samples control composition by design and therefore do not test the in-vivo confound.

The positronium literature recognises this qualitatively: o-Ps lifetime reflects several phenomena, including oxygen, free radicals and free-volume structure [7]. What has been missing is a quantitative statement of whether oxygenation and composition are identifiable as separate variables, how large the apparent hypoxia bias can be, and how many counts would be needed to overcome the degeneracy with a second observable. Here we formulate the problem as an identifiability and CRLB analysis for an emerging nuclear-medicine biomarker. We quantify the bias produced by a lifetime-only, water-calibrated interpretation; test the structural rank of the lifetime-only inverse problem; evaluate whether adding o-Ps intensity $I_3$ or a related $3\gamma/2\gamma$ observable can break the degeneracy; and translate the resulting precision limits into clinically interpretable count and volume requirements.

Prior 3$\gamma$ oxygenation experiments and recent proposals for joint lifetime and $3\gamma/2\gamma$ readouts motivate the use of a second observable [8-10]. A related single-subject cardiac PLI re-analysis reported an in-vivo lifetime contrast that was not explained by blood oxygenation, illustrating why the general identifiability problem matters in human data [11].

## Materials and methods

### Forward model

We modelled the o-Ps decay rate as a sum of independent channels:

$$ \lambda_3 = 1/\tau_3 = \lambda_{\mathrm{pickoff}}(f) + \kappa(f)\alpha(f)pO_2, $$

where $f$ is the lipid/free-volume-rich fraction of a two-compartment tissue, $\lambda_{\mathrm{pickoff}}(f)$ is the composition-dependent baseline rate, $\kappa$ is the oxygen quenching constant and $\alpha$ is oxygen solubility. The baseline lifetime $\tau_0(f)$ interpolated between water and lipid endpoints, and the lipid:water oxygen-solubility ratio was anchored to published oil/lipid measurements [12, 13]. The o-Ps intensity was modelled as

$$ I_3 = I_{3,w} + a_f f + a_p pO_2, $$

where $a_f=\partial I_3/\partial f$ and $a_p=\partial I_3/\partial pO_2$. The two load-bearing unknowns were made explicit: $\kappa_{\mathrm{lipid}}$, swept over 0.1-1.0 times the water value, and the composition slope $\partial I_3/\partial f$ (Table 1). The baseline scenario assumed the pessimistic case $\partial I_3/\partial pO_2 \approx 0$, so that oxygen affects the lifetime rate but not o-Ps formation probability.

### Apparent-pO$_2$ bias

We defined a naive reader as an estimator that assumes pure-water calibration ($f=0$) and inverts an observed lifetime to pO$_2$. The resulting apparent-pO$_2$ error was computed over true pO$_2$ and lipid fraction. This bias quantifies the oxygenation error that would arise when a composition-dependent lifetime is interpreted as oxygen-specific.

### Identifiability and CRLB analysis

For $\theta=(pO_2,f)$, Fisher information matrices were computed from $\tau_3$ alone and from the two-observable vector $(\tau_3,I_3)$. Structural non-identifiability was defined by rank deficiency of the Fisher information matrix; practical identifiability was assessed by the CRLB and parameter correlation. From $\tau_3$ alone, both parameters enter through the scalar rate $\lambda_3$, so the score vectors are collinear and the Fisher information has rank 1. With $(\tau_3,I_3)$, the problem becomes identifiable only if the Jacobian of $(\lambda_3,I_3)$ with respect to $(pO_2,f)$ is non-collinear.

### Poisson spectrum and nuisance profiling

To avoid treating $\tau_3$ and $I_3$ as independent clean measurements, we built a binned Poisson lifetime-spectrum model. The expected spectrum contained a fast exponentially modified Gaussian component, an o-Ps component with slope $\tau_3(\theta)$ and amplitude $I_3(\theta)$, and a large flat accidental background. The per-bin Fisher information was

$$F_{ab} = \sum_k m_k^{-1}\,\partial_a m_k\,\partial_b m_k,$$

where $m_k$ is the expected count in bin $k$. This includes the $\tau_3$-$I_3$ estimation covariance. We also profiled spectral nuisance parameters by extending the Fisher information matrix to include background level, fast-component lifetime, prompt offset and instrument resolution, then marginalising to $(pO_2,f)$. As an internal estimator check, Poisson spectra were simulated under the same forward model and fitted by maximum likelihood to verify attainability of the fixed-nuisance CRLB (Online Resource 1).

### Counts and volume model

For the count-to-volume translation, we used a scenario anchor from a public $^{44}$Sc PLI phantom preprint: approximately $3.6\times10^4$ o-Ps counts in a 5.57 mL region [14]. We scaled o-Ps counts by region-of-interest volume and by scenario-level effective isotope-yield factors representing prompt branching and source-to-background conditions. The scenarios were $^{124}$I (best yield), $^{68}$Ga/$^{44}$Sc (reference) and $^{82}$Rb (lower yield). For each tissue state, we computed the region volume required to reach $\sigma(pO_2)\leq10$ mmHg and classified a virtual tumour at 4 mm voxel scale as viable, marginal or not achievable.

All analyses were implemented in Python 3.13 using NumPy, SciPy and Matplotlib. Code, constants and generated results are available in the public repository listed in Data Availability. Use of AI-assisted tools is reported in Statements and Declarations.

## Results

### Lifetime-only interpretation produces large apparent oxygenation errors

The composition-dependent lifetime shift dominated the oxygen-specific lifetime term. For a tissue truly at pO$_2$ = 20 mmHg, a water-calibrated lifetime read produced apparent-pO$_2$ errors of -178 mmHg at 2% lipid, -439 mmHg at 5% lipid and -860 mmHg at 10% lipid (Fig. 1). These values are physiologically implausible, indicating that the uncorrected lifetime read is composition-dominated rather than oxygen-specific.

The oxygen sensitivity was also composition-dependent and uncertain because $\kappa_{\mathrm{lipid}}$ has not been measured in relevant lipid/protein environments. The model reproduced the aqueous sensitivity of approximately 0.09 ps/mmHg and predicted a net range of approximately 0.09-0.90 ps/mmHg in lipid-rich material across the $\kappa_{\mathrm{lipid}}$ sweep (Fig. 2). Thus, lipid affects both the baseline lifetime and the oxygen sensitivity.

### $\tau_3$ alone is structurally non-identifiable

From the lifetime alone, pO$_2$ and composition were not separately identifiable. Both parameters enter only through the single summed decay rate $\lambda_3$, so the two-parameter Fisher information matrix has rank 1 and the individual CRLBs diverge. This is an algebraic non-identifiability, not a shortage of counts.

Adding $I_3$ restored identifiability in principle, because composition moves both $\tau_3$ and $I_3$ while, in the pessimistic baseline model, oxygen moves only the rate. The formal condition is a non-collinear Jacobian for $(\lambda_3,I_3)$ with respect to $(pO_2,f)$ (Fig. 3). If $\partial I_3/\partial f$ approaches zero, the system again becomes degenerate. A non-zero $\partial I_3/\partial pO_2$ can help if it supplies an additional non-collinear direction, but it is not sufficient by itself if it remains aligned with the lifetime-rate response.

### The second-observable rescue is statistically weak

At $10^5$ o-Ps counts and a representative hypoxic fatty state (pO$_2$ = 20 mmHg, $f=0.10$), the pO$_2$ CRLB remained large across noise models: 332 mmHg for the fixed-nuisance Poisson spectrum, 570 mmHg for an idealised two-observable model using the field's empirical lifetime precision, 665 mmHg after profiling background and fast-component nuisances, and 758 mmHg after profiling all tested nuisances (Table 2). The spectral model also exposed substantial $\tau_3$-$I_3$ covariance, with parameter correlation $\rho=0.70$ in the optimistic Poisson model compared with $\rho=0.05$ in the idealised two-observable model.

The count scaling implied approximately $3$-$5\times10^8$ o-Ps events for a 10 mmHg target in the profiled models, depending on the noise model (Fig. 4). The spectrum calculations are expressed in total in-window events, with $N_3=I_3(1-\mathrm{background})N_{\mathrm{total}}$; at the representative state used here, $10^5$ o-Ps counts correspond to approximately $1.1\times10^6$ in-window events. Parametric Monte Carlo confirmed that the fixed-nuisance bound is statistically attainable under the assumed spectrum model: empirical standard deviations matched the CRLB at both tested count levels, and the pO$_2$ pull distribution had mean +0.05 and standard deviation 1.00 (Online Resource 1). This validates estimator behaviour under the specified model; it does not validate the unmeasured biological constants.

### Voxel-scale pO$_2$ separation is not achievable under current yield assumptions

When translated to region-of-interest volumes, clinically useful separation required litre-scale pooling. At pO$_2$ = 10 mmHg and 5% lipid, the required pooled volumes were approximately 20 L for the best-yield $^{124}$I scenario, 78 L for $^{68}$Ga and 130 L for $^{82}$Rb (Fig. 5). At 60% lipid, where oxygen sensitivity is higher, the best-yield scenario still required approximately 5 L. At a native 4 mm clinical voxel (0.064 mL), pO$_2$ separation was not achievable anywhere in the virtual tumour phantom (Fig. 6).

## Discussion

This analysis identifies a fundamental limitation for positronium-lifetime hypoxia imaging. Oxygen quenching of o-Ps is real, but a lifetime map is not an oxygenation map unless composition is controlled. From $\tau_3$ alone, oxygenation and composition collapse into a single measured decay rate, making the inverse problem structurally non-identifiable. This remains true even with arbitrarily many counts. The practical consequence is large apparent-pO$_2$ bias when composition is ignored.

The analysis is also constructive. It shows that a second observable, such as o-Ps intensity $I_3$ or a related $3\gamma/2\gamma$ ratio, is required to break the degeneracy. This requirement is analogous to adding an independent contrast dimension to separate two physical sources of signal, as in established multi-parameter imaging models [15]. In the pessimistic baseline model, the key separability handle is the composition dependence of $I_3$. Therefore, PLI oxygenation studies should report the lifetime together with $I_3$ or $3\gamma/2\gamma$, and should treat co-registered CT/MRI-derived composition as a correction variable rather than a nuisance to ignore.

However, identifiability in principle does not imply clinical feasibility. The CRLBs show that current count yields are far from sufficient for voxel-level pO$_2$ separation. The relevant design target is not merely estimating a single lifetime, for which photon-limited precision scaling is well established [16], but separating oxygenation from composition in a two-parameter model. Under the yield scenarios used here, that target requires regional pooling at volumes incompatible with focal tumour hypoxia imaging. This does not preclude regional or ex-vivo studies, nor future systems with substantially higher effective o-Ps yields, but it sets a quantitative bar for claims of voxel-scale hypoxia imaging.

The decisive experiment is a controlled PALS matrix over O$_2$ by medium: water, lipid emulsion and protein/serum. Such an experiment should measure both $\tau_3$ and $I_3$ under independently measured dissolved oxygen. It would determine $\kappa_{\mathrm{lipid}}$, protein-environment quenching, $\partial I_3/\partial f$ and $\partial I_3/\partial pO_2$, converting the present conditional model into a measured one. This is a modest bench experiment compared with a full clinical imaging study and should precede strong clinical claims about PLI hypoxia.

This study has limitations. The forward model is intentionally transparent and two-compartment; it does not include richer Tao-Eldrup free-volume physics or chemical effects such as inhibition and radical scavenging. The $I_3$ values are illustrative placeholders, and the composition slope is assumed non-zero in the baseline scenario. The lipid quenching constant is unmeasured in relevant biological environments and was therefore swept. The count model is anchored to one public preprint yield and uses scenario-level isotope factors rather than scanner-specific measured yields. Nuisance profiling provides a more conservative CRLB, but the spectrum model remains idealised. Finally, the Monte Carlo validates statistical attainability under the assumed spectrum model, not the biological forward model. A PALS measurement or re-analysis of real data with $I_3$ extraction remains the key empirical anchor.

In summary, positronium-lifetime hypoxia imaging is limited by an oxygenation-versus-composition identifiability problem. Lifetime-only PLI contrasts should not be interpreted as hypoxia without composition control. A second observable can make the problem identifiable, but current count yields imply that clinically useful voxel-scale separation is not achievable without major gains in effective o-Ps statistics or strong external composition constraints.

## References

1. Shibuya K, Saito H, Nishikido F, Takahashi M, Yamaya T. Oxygen sensing ability of positronium atom for tumor hypoxia imaging. Commun Phys. 2020;3:173. https://doi.org/10.1038/s42005-020-00440-z
2. Stepanov PS, Selim FA, Stepanov SV, et al. Interaction of positronium with dissolved oxygen in liquids. Phys Chem Chem Phys. 2020;22:5123. https://doi.org/10.1039/c9cp06105c
3. Moskal P, Kisielewska D, Curceanu C, et al. Feasibility study of the positronium imaging with the J-PET tomograph. Phys Med Biol. 2019;64:055017. https://doi.org/10.1088/1361-6560/aafe20
4. Moskal P, Stępień EŁ. Positronium as a biomarker of hypoxia. Bio-Algorithms Med-Syst. 2021. https://doi.org/10.1515/bams-2021-0189
5. Moskal P, Baran J, Bass S, et al. Positronium image of the human brain in vivo. Sci Adv. 2024;10:eadp2840. https://doi.org/10.1126/sciadv.adp2840
6. Mercolli L, Steinberger WM, Sari H, et al. In vivo positronium lifetime measurements with intravenous tracer administration and a long axial field-of-view PET/CT. IEEE Trans Radiat Plasma Med Sci. 2026. https://doi.org/10.1109/TRPMS.2026.3687923
7. Avachat AV, Mahmoud KH, Leja AG, Xu JJ, Anastasio MA, Sivaguru M, Di Fulvio A. Ortho-positronium lifetime for soft-tissue classification. Sci Rep. 2024;14:21155. https://doi.org/10.1038/s41598-024-71695-7
8. Alkhorayef MA, Abuelhia EI, Chin MPW, Spyrou NM. Determination of the relative oxygenation of samples by ortho-positronium 3-gamma decay for future application in oncology. J Radioanal Nucl Chem. 2009;281:171-174. https://doi.org/10.1007/s10967-009-0123-6
9. Alkhorayef M, Sulieman A, Alsager OA, Alrumayan F, Alkhomashi N. Investigation of using positronium and its annihilation for hypoxia PET imaging. Radiat Phys Chem. 2021;188:109690. https://doi.org/10.1016/j.radphyschem.2021.109690
10. Moskal P. Quantum entanglement degree, mean positronium lifetime, and the $3\gamma$/$2\gamma$ annihilation-rate ratio as novel PET biomarkers for hypoxia: concept, challenges, and predictions. Bio-Algorithms Med-Syst. 2026;22:56. https://doi.org/10.5604/01.3001.0055.7461
11. Zermeño ED. Cardiac positronium lifetime in human PET: a reproducible right-left ventricular contrast that is not explained by blood oxygenation. medRxiv. 2026. https://doi.org/10.64898/2026.06.14.26355630
12. Battino R, Evans FD, Danforth WF. The solubilities of seven gases in olive oil. J Am Oil Chem Soc. 1968;45:830. https://doi.org/10.1007/BF02540163
13. Roppongi T, Mizuno N, Miyagawa Y, Kobayashi T, Nakagawa K, Adachi S. Solubility and mass transfer coefficient of oxygen through gas- and water-lipid interfaces. J Food Sci. 2021;86:867-873. https://doi.org/10.1111/1750-3841.15641
14. Mercolli L, Steinberger WM, Grundler PV, et al. First positronium lifetime imaging with scandium-44 on a long axial field-of-view PET/CT. arXiv. 2025. https://arxiv.org/abs/2506.13460
15. Sourbron SP, Buckley DL. Classic models for dynamic contrast-enhanced MRI. NMR Biomed. 2013;26:1004-1027. https://doi.org/10.1002/nbm.2940
16. Köllner M, Wolfrum J. How many photons are necessary for fluorescence-lifetime measurements? Chem Phys Lett. 1992;200:199-204. https://doi.org/10.1016/0009-2614(92)87068-Z

## Statements and Declarations

**Funding.** The author declares that no funds, grants or other support were received during the preparation of this manuscript.

**Competing interests.** The author has no relevant financial or non-financial interests to disclose.

**Author contributions.** E.D.Z. conceived the study, implemented the model, performed the analysis, generated the figures and wrote the manuscript.

**Data availability.** No clinical or animal datasets were analysed. The datasets generated during the current study, including code, constants, intermediate outputs and figures, are available at https://github.com/Jefemaestro33/oxygenation-versus-tissue-composition-in-positronium-lifetime-pet-identifiability-limit.

**Code availability.** The analysis code is available at https://github.com/Jefemaestro33/oxygenation-versus-tissue-composition-in-positronium-lifetime-pet-identifiability-limit under the repository licence terms.

**Ethics approval.** Not applicable. This is a modelling and methods study using no human participants, human data, animals or animal data.

**Consent to participate.** Not applicable.

**Consent to publish.** Not applicable.

**Use of AI tools.** AI-assisted programming and editorial tools were used to help cross-check code, draft text and identify consistency issues under the author's direction. The author reviewed all outputs and takes responsibility for the final manuscript, analysis and interpretation.

## Tables

**Table 1** Forward-model constants and load-bearing unknowns

| Quantity | Value | Status | Source |
|---|---|---|---|
| $\tau_0$ water | 1.815 ns | measured | [1] |
| $\tau_0$ adipose | 2.5-2.7 ns | measured | [7] |
| $\kappa$(O$_2$) water | 0.0204 µmol$^{-1}$ µs$^{-1}$ L | measured | [1, 2] |
| O$_2$ solubility lipid:water | approximately $5\times$ | measured | [12, 13] |
| Quenching mechanism | spin conversion | measured | [2] |
| $\kappa_{\mathrm{lipid}}$ | unmeasured; swept 0.1-1.0 times water | unknown | proposed experiment |
| $\partial I_3/\partial f$ | unmeasured; assumed non-zero in baseline scenario | unknown | proposed experiment |

**Table 2** Cramér-Rao bound on pO$_2$ at pO$_2$ = 20 mmHg, $f$ = 0.10 and $10^5$ o-Ps counts

| Noise model | $\sigma(pO_2)$ (mmHg) | $\rho$ |
|---|---:|---:|
| Poisson spectrum, nuisances fixed | 332 | +0.70 |
| Idealised two-observable model | 570 | +0.05 |
| Poisson spectrum, background and fast-component nuisances profiled | 665 | -- |
| Poisson spectrum, all tested nuisances profiled | 758 | -- |

## Figure legends

**Fig. 1** Apparent pO$_2$ error produced by a water-calibrated lifetime interpretation when tissue composition is ignored. The contour marks the region where absolute error is 10 mmHg. Even low lipid fractions drive errors of hundreds of mmHg

![](figures/fig1_bias_surface.png){width=78%}

**Fig. 2** Oxygen sensitivity of the o-Ps lifetime as a function of lipid fraction. The band represents the sweep over the unmeasured lipid quenching constant $\kappa_{\mathrm{lipid}}$ from 0.1 to 1.0 times the water value

![](figures/fig2_sensitivity.png){width=70%}

**Fig. 3** Separability geometry of $(\tau_3,I_3)$. Iso-$\tau_3$ contours show the near-degenerate lifetime direction, while iso-$I_3$ contours provide the composition handle. The shallow crossing reflects identifiability in principle but weak statistical separation

![](figures/fig4_degeneracy.png){width=78%}

**Fig. 4** CRLB $\sigma(pO_2)$ versus total in-window events for the full-spectrum $(\tau_3,I_3)$ fit. The lifetime-only case is structurally non-identifiable. A 10 mmHg target requires order-$10^9$ in-window events, corresponding to order-$10^8$ o-Ps counts after the $N_3=I_3(1-\mathrm{background})N_{\mathrm{total}}$ conversion

![](figures/fig3_separability.png){width=70%}

**Fig. 5** Region-of-interest volume required to separate pO$_2$ from composition with $\sigma(pO_2)\leq10$ mmHg for three effective isotope-yield scenarios. Clinical separation requires litre-scale pooling under current assumptions

![](figures/fig5_boundary.png){width=72%}

**Fig. 6** Virtual tumour simulation. The left panel shows true pO$_2$; the right panel shows voxel-level separability at 4 mm resolution under the profiled CRLB model. pO$_2$ separation is not achievable anywhere at native voxel scale

![](figures/fig6_tumor_map.png){width=95%}

## Supplementary information

**Online Resource 1** Parametric Monte Carlo validation of the fixed-nuisance Poisson CRLB under the assumed spectrum model. Pulls of $\hat{p}O_2$ are close to $N(0,1)$, showing that the maximum-likelihood estimator reaches the fixed-nuisance CRLB when the forward model is correctly specified.
