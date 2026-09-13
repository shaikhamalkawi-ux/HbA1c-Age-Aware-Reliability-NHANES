# Reproducibility and replay

Checkpoint 2 scientific verification is **16 PASS / 0 HOLD / 0 FAIL** after explicit adjudication of a single `WTSAF2YR` decimal-representation discrepancy. See [the final report](SCIENTIFIC_VERIFICATION.md), [final machine-readable checks](../verification/scientific_checks_final.json), and [the adjudication record](../verification/fasting_weight_adjudication.json).

No training objective, cohort rule, model, calibration rule, locked result, or claim boundary was changed. No target retraining or recalibration was performed.

## Public package checks

The repository-integrity layer uses Python 3.9+ and the standard library:

```sh
python scripts/verify_manifest.py
python scripts/check_public_content.py
python scripts/check_verification_report.py
python scripts/check_final_scientific_summary.py
python scripts/scan_git_history.py
```

The manifest/content/report checks validate public-package bookkeeping. `scan_git_history.py` is intentionally separate because the existing public Git history still contains a documented author/committer contact-metadata finding that must be resolved before `v1.0.0`.

## Independently replay the scientific QA

The read-only verifier requires the privately held locked research archive and the official CDC components. The repository does not redistribute participant-level inputs.

```sh
python -m venv .venv
# Activate .venv using the normal command for your shell.
python -m pip install -r requirements-analysis.txt
python scripts/prepare_evidence.py --archive <locked-research-archive.zip> --output-dir .local/evidence
python scripts/retrieve_nhanes.py --output-dir .local/evidence/nhanes --manifest .local/retrieved_components.json --verify-against verification/data_provenance.json
python scripts/verify_science_final.py --evidence-root .local/evidence --output .local/replayed_scientific_checks.json
```

`verify_science_final.py` imports the locked read-only arithmetic verifier and changes only the adjudicated survey-weight representation check. Zero-versus-positive fasting-weight membership must agree exactly. The numeric `WTSAF2YR` field is allowed the documented `5.0001e-5` representation increment because the CDC-published maximum `944153.24975` is stored in the archived CSV as `944153.2498`. All other scientific tolerances remain unchanged.

The verifier contains no model training or retuning. It recomputes metrics from stored predictions/intervals, checks frozen objects and hashes, verifies source/target cohort identities, replays the TG bridge, and evaluates the historical fixed FIS models. The recovered original CQR PASS is limited to stored-output arithmetic; original fitted CQR learner objects were not recovered and no complete original learner refit is claimed.

## Public aggregate outputs

The repository exposes only public-safe aggregate verification artifacts, including:

- `source_reconstruction/source_reconstruction_certificate.csv`
- `derived_outputs/point_model_metrics.csv`
- `derived_outputs/point_model_paired_bootstrap.csv`
- `derived_outputs/primary_interval_metrics.csv`
- `derived_outputs/temporal_metrics.csv`
- `derived_outputs/recovered_original_cqr_metrics.csv`
- `derived_outputs/legacy_anfis_verification.csv`
- `frozen_objects/frozen_temporal_ols_conformal_certificate.json`
- `data/NHANES_Assay_Source_Ledger.csv`

Raw NHANES XPT files, participant-level analytic cohorts, participant predictions, split ledgers, and private research archives are deliberately excluded from the public release candidate.

## Licensing

The license gate is closed:

- original code where the author has authority to grant the license: MIT (`LICENSE`);
- original documentation, original figures, and original aggregate derived materials where the applicable rightsholder has authority to grant the license: CC BY 4.0 (`CONTENT_LICENSE.md`);
- third-party materials retain their own terms.

## Environment

The original analytical record and the independent QA environment are documented separately in [ENVIRONMENT.md](ENVIRONMENT.md) and `requirements-analysis.txt`. Missing historical versions are reported as missing rather than guessed.

## Review gates

1. Repository skeleton: complete.
2. Numerical/scientific QA: **complete PASS**.
3. License mapping: **complete PASS**.
4. Public-history privacy cleanup and final safety rerun: pending.
5. GitHub `v1.0.0`: create only after the history/public-safety gate passes.
6. Zenodo: archive the approved production release and verify DOI/metadata.

`CITATION.cff` remains the intended metadata authority. No competing `.zenodo.json` is used.
