# Age-aware HbA1c reliability across NHANES cycles

**Does age justify separate HbA1c prediction models, or does it matter more for the reliability of their prediction intervals?**

This repository provides public reproducibility and verification materials for the associated HbA1c reliability study without redistributing participant-level NHANES data.

> **Hard age partitioning did not show a stable point-prediction advantage, whereas age-specific predictive-reliability differences persisted across NHANES cycles.**

Scientific verification is closed PASS: **16/16 registered scientific check families PASS**. The verification covers source identity/cohort closure, repeated out-of-fold metrics and participant-bootstrap contrasts, conformal quantiles and coverage arithmetic, temporal counts/metrics, the triglyceride bridge, recovered secondary CQR outputs, frozen-object identity, and historical ANFIS structural replay. It does **not** claim fresh end-to-end retraining of every model family from raw CDC files.

## What was audited and corrected?

The historical analysis used a table of 2,325 adults whose official source and eligibility required reconstruction. All 2,325 rows were linked uniquely to NHANES 2017–2018 using exact agreement at the stored precision on age, BMI, fasting glucose, triglycerides, HbA1c, and Friedewald LDL: **2,325 exact unique matches, 0 ambiguous, 0 unmatched**.

The historical reduction from 2,350 to 2,325 is explained by 25 missing Friedewald-LDL values; all 25 had triglycerides greater than 400 mg/dL. LDL completeness is not required by the four-input HbA1c prediction question.

The corrected development cohort contains **2,219 adults**, with **666 / 991 / 562** in the age groups **20–39 / 40–64 / 65+**.

## Locked point-prediction findings

Internal evaluation used 5 folds × 5 repeats of out-of-fold testing with participant-level bootstrap contrasts.

| Model | Repeated-OOF RMSE |
|---|---:|
| Pooled OLS | 0.5732523422 |
| Hard-age OLS | 0.5774212775 |
| Glucose-only OLS | 0.5862355212 |
| SmoothVC OLS | 0.5911837422 |
| Pooled LightGBM | 0.5937450777 |
| Hard-age LightGBM | 0.6601329856 |

Hard-age OLS minus pooled OLS was **+0.0041689353**, with participant-bootstrap 95% CI **[−0.0026392765, +0.0122600322]**.

## Primary uncertainty finding

At nominal 90% coverage:

| Calibration | 20–39 | 40–64 | 65+ |
|---|---:|---:|---:|
| Global residual | 0.962162 | 0.892836 | 0.856228 |
| Age-Mondrian | 0.912012 | 0.903734 | 0.893594 |

Age-Mondrian calibration reduced the observed between-age coverage imbalance. This is an empirical subgroup result, not a guarantee of nominal coverage for every subgroup or individual.

## Temporal evaluation hierarchy

The **2021–2023 NHANES cycle is the forward temporal evaluation**. The **2015–2016 cycle is a secondary adjacent-cycle stress test**. Both use frozen source models/calibration, without target retraining or target recalibration.

| NHANES target cycle | Role | N | RMSE | Calibration slope |
|---|---|---:|---:|---:|
| 2015–2016 | Secondary adjacent-cycle stress test | 2,235 | 0.6579939892 | 1.0421080503 |
| August 2021–August 2023 | Forward temporal evaluation | 2,808 | 0.5676959498 | 1.0472880843 |

These are independent cross-sectional samples within NHANES, not longitudinal follow-up and not validation in an independent health system.

## Evidence hierarchy

| Evidence layer | Role |
|---|---|
| Global residual and age-Mondrian conformal intervals | Primary uncertainty analyses |
| Recovered original CQR outputs | Secondary analysis |
| Later fixed-configuration CQR | Post hoc exploratory analysis only |
| Historical ANFIS models | Structural/reproducibility case only |

The historical ANFIS record contains 3 Sugeno FIS models, 41 rules, and 533 premise/consequent parameters. All 533 displayed parameter values were verified at six-decimal precision, and fixed-FIS replay agreed with stored MATLAB predictions to approximately `1.47e-12`. This is not evidence of ANFIS superiority or biological meaning of rule counts.

See [`docs/CLAIM_BOUNDARIES.md`](docs/CLAIM_BOUNDARIES.md) for the complete inference boundary.

## Public data and repository policy

Raw NHANES XPT files, participant-level analytic tables, and participant-level predictions are not redistributed here. [`data/README.md`](data/README.md) records official CDC component URLs, retrieval dates, SHA-256 values, variables, assay roles, and retrieval instructions so the public source can be obtained independently.

The repository intentionally excludes literature/publisher PDFs, journal correspondence, private conversations, manuscript files, private contact files, participant-level derived tables, and internal project-transfer archives.

## Licensing

- Original code whose rights the author can grant is released under the **MIT License**; see [`LICENSE`](LICENSE).
- Original documentation, original figures, and original aggregate derived materials whose rights the applicable rightsholder can grant are released under **CC BY 4.0**; see [`CONTENT_LICENSE.md`](CONTENT_LICENSE.md).
- Third-party material retains its own terms and is not relicensed by this repository.

## Associated manuscript

**Age-Aware Reliability of HbA1c Prediction Across NHANES Cycles: Leakage-Free Evaluation, Conformal Calibration, and Temporal Transport**

Current manuscript author order:
1. Hussein AlWedyan
2. Ghassan Malkawi
3. Ahmed Abdelaziz Elsayed
4. Abdulwehab Ibrahim
5. Ashraf Shalafeh
6. Mohanad Alata
7. Mohammad AlWidian

**Repository/archive creator: Ghassan Malkawi. Repository/archive creation and associated-manuscript authorship are separate roles.**

## Archival record

- GitHub release: **v1.0.1**
- Zenodo version DOI: **10.5281/zenodo.22737921**
- DOI link: https://doi.org/10.5281/zenodo.22737921

Repository citation metadata are maintained in [`CITATION.cff`](CITATION.cff).
