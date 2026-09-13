# Temporal transport verification

Both frozen temporal evaluations are closed **PASS** for the locked analysis outputs and cohort/count checks.

- Backward NHANES 2015–2016: N=2,235; age counts 712 / 970 / 553; RMSE 0.6579939892; calibration slope 1.0421080503.
- Forward NHANES 2021–2023: N=2,808; age counts 670 / 1,203 / 935; RMSE 0.5676959498; calibration slope 1.0472880843.
- No target retraining or primary target recalibration.
- The prespecified forward TG bridge `TG_old = -12.19 + 0.9785 * TG_new` replayed with maximum absolute difference 0.0 mg/dL.

Public aggregate output:

- [`derived_outputs/temporal_metrics.csv`](../derived_outputs/temporal_metrics.csv)
- [`data/NHANES_Assay_Source_Ledger.csv`](../data/NHANES_Assay_Source_Ledger.csv)
- [`frozen_objects/frozen_temporal_ols_conformal_certificate.json`](../frozen_objects/frozen_temporal_ols_conformal_certificate.json)

These are temporal evaluations of independent cross-sectional NHANES samples, not longitudinal follow-up and not validation in an independent health system.

See [scientific verification](../docs/SCIENTIFIC_VERIFICATION.md) and [input identities](../verification/evidence_inputs.json).
