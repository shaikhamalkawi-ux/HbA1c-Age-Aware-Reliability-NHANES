# Age-aware HbA1c reliability across NHANES cycles

**Does age justify separate HbA1c prediction models, or does it matter more for the reliability of their prediction intervals?**

This repository is being prepared to make the study's source reconstruction, evaluation records, calibration, and temporal transport independently inspectable.

> **Age did not consistently justify separate point-prediction models, but it mattered more strongly for predictive reliability/calibration.**

**Current status: repository skeleton for review.** Numerical reproduction has not been executed in this repository. The values below are locked reference values supplied with the study, not newly reproduced results. There is no production release or Zenodo DOI yet. Licensing is pending an author decision.

## What was audited and corrected?

The historical analysis used a table of 2,325 adults whose official source and eligibility needed reconstruction. The locked study reports an exact unique match to NHANES 2017–2018 for all 2,325 rows, with no ambiguous or unmatched rows. The historical reduction from 2,350 to 2,325 was explained by 25 missing Friedewald-LDL values; all 25 had triglycerides at least 400 mg/dL. LDL completeness was not required by the four-input HbA1c prediction question.

The corrected development cohort removed the LDL-completeness requirement and applied the specified fasting eligibility. It contains **2,219 adults**, with **666 / 991 / 562** in the age groups **20–39 / 40–64 / 65+**. This is a repeated cross-sectional study of measured HbA1c at the same examination.

## What did the locked study find?

The point-model comparison used 5 folds × 5 repeats of out-of-fold evaluation and participant-level bootstrap contrasts.

| Model | Reported repeated-OOF RMSE, HbA1c percentage units |
|---|---:|
| Pooled OLS | 0.573252 |
| Hard-age OLS | 0.577421 |
| Glucose-only OLS | 0.586236 |
| SmoothVC OLS | 0.591184 |
| Pooled LightGBM | 0.593745 |
| Hard-age LightGBM | 0.660133 |

The reported hard-age OLS minus pooled OLS difference is **+0.004169**, with **95% CI [−0.002639, +0.012260]**. This does not establish a stable improvement from hard age partitioning.

At nominal 90% coverage, the primary interval comparison reports:

| Calibration | 20–39 | 40–64 | 65+ |
|---|---:|---:|---:|
| Global residual | 0.962162 | 0.892836 | 0.856228 |
| Age-Mondrian | 0.912012 | 0.903734 | 0.893594 |

The age-Mondrian approach reduced the observed coverage imbalance. This is not a guarantee of nominal coverage in every subgroup or for every individual.

## What did temporal transport show?

The primary temporal evaluations used frozen source models and calibration, without target retraining or recalibration.

| NHANES target cycle | Reported N | Reported RMSE | Reported calibration slope |
|---|---:|---:|---:|
| 2015–2016 | 2,235 | 0.657994 | 1.042108 |
| August 2021–August 2023 | 2,808 | 0.567696 | 1.047288 |

These are same-program temporal evaluations. Linear calibration slopes alone do not establish clinical adequacy or validation in an independent health system.

## Evidence hierarchy and claim boundaries

| Evidence layer | Role |
|---|---|
| Global residual and age-Mondrian conformal intervals | Primary uncertainty analyses |
| Recovered original CQR outputs | Secondary analysis |
| Later fixed-configuration CQR | Post hoc exploratory analysis only |
| Historical ANFIS models | Legacy reproducibility case only |

The historical ANFIS record concerns 3 Sugeno FIS models, 41 rules, and 533 premise/consequent parameters. These are verification targets, not a claim of ANFIS superiority or biological meaning of rule counts.

The study does not establish laboratory-test replacement, treatment guidance, longitudinal forecasting, or individual conditional coverage. See [claim boundaries](docs/CLAIM_BOUNDARIES.md).

## What can be run now?

From the repository root, using Python 3.9 or later:

```sh
python scripts/verify_manifest.py
python scripts/check_public_content.py
```

These commands check package integrity and the current text-file inventory. They **do not reproduce scientific results**. Source-analysis commands will be added only after the original analysis files and frozen outputs have been inspected and verified. See [reproducibility status](docs/REPRODUCIBILITY.md) and the [machine-readable scientific check register](verification/scientific_checks.json).

## Repository layout

```text
README.md
CITATION.cff
LICENSE_PENDING.md
requirements.txt
SHA256SUMS.txt
data/README.md
scripts/                    Package checks; no model training
source_reconstruction/      Source-reconstruction intake requirements
analysis/                   Repeated-OOF and bootstrap intake requirements
conformal/                  Primary, secondary, exploratory boundaries
temporal_validation/        Frozen evaluation intake requirements
derived_outputs/            Reserved for verified aggregate outputs
frozen_objects/             Reserved for verified original frozen artifacts
figures/                    Reserved for audited original figures
verification/               Reference values and explicit check status
docs/                       Reproduction, dictionary, claims, release metadata
```

Only the documented scaffold files are included at this checkpoint. Original datasets, model objects, analysis implementations, and figures have not yet been admitted into this repository. The [content inventory](docs/CONTENTS.md) explains inclusion and exclusion decisions.

## Citation and licensing

Repository and planned archive author: **Ghassan Malkawi**. [CITATION.cff](CITATION.cff) describes these reproducibility materials. It does not redefine the authorship of the associated manuscript.

Associated manuscript: *Age-Aware Reliability of HbA1c Prediction Across NHANES Cycles: Leakage-Free Evaluation, Conformal Calibration, and Temporal Transport*.

No license has been selected or granted by this scaffold. See [LICENSE_PENDING.md](LICENSE_PENDING.md). The planned first production release is **v1.0.0**; it will follow scientific verification, review feedback, metadata checks, and license approval.
