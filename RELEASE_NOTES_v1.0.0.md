# v1.0.0 release notes

## Scope

This release packages the public-safe reproducibility materials for the study:

**Age-Aware Reliability of HbA1c Prediction Across NHANES Cycles: Leakage-Free Evaluation, Conformal Calibration, and Temporal Transport**

The release does not change any locked scientific result, cohort, model, calibration rule, dataset definition, or claim boundary.

## Scientific verification status

All 16 registered scientific check families are closed PASS in `verification/scientific_checks_final.json`.

The release includes public-safe aggregate verification outputs for:

- exact source reconstruction and corrected cohort closure;
- repeated out-of-fold point-model metrics;
- paired participant bootstrap contrasts;
- primary global and age-Mondrian conformal metrics;
- backward and forward temporal transport metrics;
- the prespecified triglyceride bridge;
- recovered original secondary CQR stored-output arithmetic;
- frozen model/calibration identity certificates;
- historical ANFIS structural verification.

No fresh end-to-end retraining of every learner family from raw CDC files is claimed.

## Licensing

- Original code whose rights the author can grant: **MIT License** (`LICENSE`).
- Original documentation, original figures, and original aggregate derived materials whose rights the applicable rightsholder can grant: **CC BY 4.0** (`CONTENT_LICENSE.md`).
- Third-party components/materials retain their own terms and are not relicensed.

## Public-data policy

Raw NHANES XPT files and participant-level analytic tables are not redistributed. Exact official CDC component URLs, retrieval dates, hashes, variables, assay roles, and retrieval instructions are provided in `data/README.md` and `verification/data_provenance.json`.

## Evidence hierarchy

- Global residual and age-Mondrian conformal analyses: primary.
- Recovered original CQR: secondary.
- Later fixed-configuration CQR: post hoc exploratory only.
- Historical ANFIS: structural/reproducibility case only.

## Intentionally excluded

- raw NHANES XPT files;
- participant-level cohorts, predictions, split/role ledgers, and interval endpoints;
- private research archives and machine-specific paths;
- manuscript files, journal correspondence, reviewer packages, and chat-transfer archives;
- publisher/literature PDFs and other third-party copyrighted materials;
- credentials and private contact files.

## Remaining blockers before publication

1. Git-history privacy cleanup for the documented historical contact-metadata finding.
2. Final public-release QA after the cleaned history is in place.
3. GitHub release creation and Zenodo ingestion/DOI verification.

Repository/archive creator: **Ghassan Malkawi**.

Associated-manuscript authorship is separate and unchanged.
