# Public aggregate derived outputs

Only non-participant aggregate verification outputs are published here. Participant-level cohorts, predictions, calibration residuals, split ledgers, and private research archives remain excluded.

Published aggregate files:

- `point_model_metrics.csv` — repeated-OOF point-model metrics.
- `point_model_paired_bootstrap.csv` — paired RMSE contrasts and participant-bootstrap 95% CIs.
- `primary_interval_metrics.csv` — primary global and age-Mondrian 90% coverage, widths, and interval scores.
- `temporal_metrics.csv` — backward/forward temporal counts, age counts, RMSE, and calibration slopes.
- `recovered_original_cqr_metrics.csv` — recovered original secondary CQR aggregate interval metrics; no original learner-refit claim.
- `legacy_anfis_verification.csv` — historical fixed-FIS structural/prediction verification summary; not a superiority result.

Machine-readable scientific status is in [`verification/scientific_checks_final.json`](../verification/scientific_checks_final.json). See [scientific verification](../docs/SCIENTIFIC_VERIFICATION.md) for interpretation and claim boundaries.
