# Included and excluded materials

## Newly admitted in checkpoint 2

- `.github/workflows/integrity.yml`
- `requirements-analysis.txt`
- `scripts/retrieve_nhanes.py`
- `scripts/prepare_evidence.py`
- `scripts/verify_science.py`
- `scripts/fis_arithmetic.py`
- `scripts/scan_git_history.py`
- `scripts/check_verification_report.py`
- `verification/evidence_inputs.json`
- `verification/source_intake.json`
- `verification/data_provenance.json`
- `verification/environment.json`
- `verification/history_safety_report.json`
- `verification/execution_artifacts.json`
- `verification/file_admission.json`
- `docs/ENVIRONMENT.md`
- `docs/SCIENTIFIC_VERIFICATION.md`
- `docs/CHECKPOINT_2.md`
- `docs/PUBLIC_SAFETY.md`
- `docs/LICENSE_DECISION.md`

Existing README, directory notes and verification references were updated. `CITATION.cff` retains Ghassan Malkawi alone. `verification/file_admission.json` is the explicit admission decision; the allowlist contains the complete snapshot inventory.

## Intentionally excluded

Raw CDC XPTs; participant-level cohorts, predictions, calibration/role tables and MAT arrays; complete/nested research archives; manuscripts and source; private contact details; original scripts with machine paths; correspondence and publisher PDFs. Original frozen model objects and figures remain deferred after the scientific stop. Only new read-only QA/retrieval code, safe exact input identities and aggregate audit measurements are admitted.

## Future production snapshot cleanup

Remove `docs/CHECKPOINT_1.md`, `docs/CHECKPOINT_2.md` and `docs/zenodo_metadata_draft.json` from the production tag. After approved licensing, replace `LICENSE_PENDING.md` with the approved notices. Complete scientific and history-safety review before tagging. Review notes can remain in history unless they contain a separately resolved privacy issue.
