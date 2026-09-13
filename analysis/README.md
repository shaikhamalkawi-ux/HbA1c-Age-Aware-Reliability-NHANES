# Point-model analysis verification

Stored repeated out-of-fold metrics, paired model contrasts, and the original participant-level bootstrap arithmetic all passed independent replay. Original model training was **not** rerun and no model was retuned.

Public aggregate outputs:

- [`derived_outputs/point_model_metrics.csv`](../derived_outputs/point_model_metrics.csv)
- [`derived_outputs/point_model_paired_bootstrap.csv`](../derived_outputs/point_model_paired_bootstrap.csv)

The OOF verification used 66,570 stored prediction rows: six model configurations × 2,219 participants × five outer-test appearances. The hard-age OLS minus pooled OLS contrast and its 10,000-resample participant-bootstrap interval reproduce the locked manuscript values.

See [scientific verification](../docs/SCIENTIFIC_VERIFICATION.md), [final machine-readable checks](../verification/scientific_checks_final.json), and [input identities](../verification/evidence_inputs.json).
