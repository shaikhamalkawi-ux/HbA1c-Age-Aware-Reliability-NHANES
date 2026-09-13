# Age-aware HbA1c reliability across NHANES cycles

**Does age justify separate HbA1c prediction models, or does it matter more for the reliability of their prediction intervals?**

This repository makes the locked study's source reconstruction, leakage-free evaluation records, uncertainty calibration, and temporal transport auditable without redistributing participant-level NHANES data.

> **Age did not consistently justify separate point-prediction models, but it mattered more strongly for predictive reliability/calibration.**

**Scientific QA is closed PASS: 16/16 registered check families PASS.** The earlier `WTSAF2YR` stop was adjudicated as a decimal-representation difference that cannot alter the zero-versus-positive fasting eligibility gate; the exact evidence is recorded in [`verification/fasting_weight_adjudication.json`](verification/fasting_weight_adjudication.json). The **v1.0.1** production materials have passed the license, public-content, manifest, reporting, and reachable-history checks. See [the public-safety review](docs/PUBLIC_SAFETY.md).

## What was audited and corrected?

The historical analysis used a table of 2,325 adults whose official source and eligibility required reconstruction. All 2,325 rows were linked uniquely to NHANES 2017–2018 using exact agreement at the stored precision on age, BMI, fasting glucose, triglycerides, HbA1c, and Friedewald LDL: **2,325 exact unique matches, 0 ambiguous, 0 unmatched**.

The historical reduction from 2,350 to 2,325 is explained by 25 missing Friedewald-LDL values; all 25 had triglycerides greater than 400 mg/dL. LDL completeness is not required by the four-input HbA1c prediction question.

The corrected development cohort removes the LDL-completeness requirement and applies the locked fasting eligibility. It contains **2,219 adults**, with **666 / 991 / 562** in the age groups **20–39 / 40–64 / 65+**.

## Locked point-prediction findings

Internal evaluation used 5 folds × 5 repeats of out-of-fold testing with participant-level bootstrap contrasts.

| Model | Recomputed repeated-OOF RMSE |
|---|---:|
| Pooled OLS | 0.5732523422 |
| Hard-age OLS | 0.5774212775 |
| Glucose-only OLS | 0.5862355212 |
| SmoothVC OLS | 0.5911837422 |
| Pooled LightGBM | 0.5937450777 |
| Hard-age LightGBM | 0.6601329856 |

Hard-age OLS minus pooled OLS was **+0.0041689353**, with participant-bootstrap 95% CI **[−0.0026392765, +0.0122600322]**. This does not establish a stable point-prediction improvement from hard age partitioning.

## Primary uncertainty finding

At nominal 90% coverage:

| Calibration | 20–39 | 40–64 | 65+ |
|---|---:|---:|---:|
| Global residual | 0.962162 | 0.892836 | 0.856228 |
| Age-Mondrian | 0.912012 | 0.903734 | 0.893594 |

Age-Mondrian calibration reduced the observed age-group coverage imbalance. This is not a guarantee of nominal coverage in every subgroup or for every individual.

## Temporal transport

The primary temporal evaluations used frozen source models and calibration, with no target retraining or target recalibration.

| NHANES target cycle | N | RMSE | Calibration slope |
|---|---:|---:|---:|
| 2015–2016 | 2,235 | 0.6579939892 | 1.0421080503 |
| August 2021–August 2023 | 2,808 | 0.5676959498 | 1.0472880843 |

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

## Reproducibility status

The final machine-readable scientific check summary is [`verification/scientific_checks_final.json`](verification/scientific_checks_final.json). The detailed initial stop report is retained separately for audit history; its only failed comparison has been adjudicated rather than silently widening a global tolerance.

The scientific QA establishes:

- source identity and cohort closure;
- repeated-OOF RMSE and paired contrasts;
- exact 10,000-resample participant bootstrap replay;
- frozen global and age-Mondrian conformal quantiles;
- internal coverage/interval-score arithmetic;
- backward and forward temporal counts and metrics;
- exact forward TG bridge replay;
- recovered original CQR stored-output arithmetic;
- frozen-object hash identity;
- legacy ANFIS structural replay.

It **does not claim a fresh end-to-end retraining of every model family from raw CDC files**.

## Public data and repository policy

Raw NHANES XPT files and participant-level analytic tables are not redistributed here. [`data/README.md`](data/README.md) records exact official CDC component URLs, retrieval dates, SHA-256 values, variables, and assay roles so the public source can be retrieved independently.

The repository intentionally excludes literature/publisher PDFs, journal correspondence, private conversations, manuscripts, private contact files, participant-level derived tables, and internal project-transfer archives.

## Licensing

- Original code whose rights the author can grant is released under the **MIT License**; see [`LICENSE`](LICENSE).
- Original documentation, original figures, and original aggregate derived materials whose rights the applicable rightsholder can grant are released under **CC BY 4.0**; see [`CONTENT_LICENSE.md`](CONTENT_LICENSE.md).
- Third-party material retains its own terms and is not relicensed by this repository.

The approved mapping is recorded in [`docs/LICENSE_DECISION.md`](docs/LICENSE_DECISION.md).

## Repository checks

Current repository-integrity checks use only the Python standard library:

```sh
python scripts/verify_manifest.py
python scripts/check_public_content.py
python scripts/check_verification_report.py
python scripts/check_final_scientific_summary.py
python scripts/scan_git_history.py
```

Scientific-analysis environment information is documented separately in [`docs/ENVIRONMENT.md`](docs/ENVIRONMENT.md) and `requirements-analysis.txt`.

## Associated manuscript

**Age-Aware Reliability of HbA1c Prediction Across NHANES Cycles: Leakage-Free Evaluation, Conformal Calibration, and Temporal Transport**

Authors, in the locked manuscript order: Hussein AlWedyan; Abdulwehab Ibrahim; Ashraf Shalafeh; Puteri Fahsyar; Mohanad Alata; Mazin Abuharaz; Mohammad AlWidian.

**Repository/archive creator: Ghassan Malkawi. Associated-manuscript authorship is separate and unchanged.**

There is no final article DOI yet. Repository citation metadata are in [`CITATION.cff`](CITATION.cff); no manuscript DOI or ORCID has been invented.

## Release

Version: **v1.0.1**. See [`RELEASE_NOTES_v1.0.1.md`](RELEASE_NOTES_v1.0.1.md) for the archival patch scope. Repository citation metadata are maintained in `CITATION.cff`; the Zenodo DOI is added after archival verification.
