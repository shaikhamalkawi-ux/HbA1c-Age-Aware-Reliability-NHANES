# Reproducibility and replay

Checkpoint 2 executed stored-output arithmetic and stopped at a reconstructed-table `WTSAF2YR` disagreement. Scientific family counts are **11 PASS / 4 HOLD / 1 FAIL**. See [the report](SCIENTIFIC_VERIFICATION.md). No training or recalibration was run.

## Public package checks

Python 3.9+ and the standard library:

```sh
python scripts/verify_manifest.py
python scripts/check_public_content.py
python scripts/check_verification_report.py
python scripts/scan_git_history.py
```

The first three check package/report integrity, not scientific success. The history command returns nonzero for the documented existing contact metadata. CI runs these checks on pushes and tags. It does not pretend that private scientific inputs are present in a public runner.

## Independently replay the stopped scientific run

This is a reproducibility instruction, not authorization to resume the study's pending scientific work. Use the exact privately held root archive whose identity is recorded in `verification/evidence_inputs.json`. The public repository does not distribute it.

```sh
python -m venv .venv
# Activate .venv using the normal command for your shell.
python -m pip install -r requirements-analysis.txt
python scripts/prepare_evidence.py --archive <locked-research-archive.zip> --output-dir .local/evidence
python scripts/retrieve_nhanes.py --output-dir .local/evidence/nhanes --manifest .local/retrieved_components.json --verify-against verification/data_provenance.json
python scripts/verify_science.py --evidence-root .local/evidence --output .local/replayed_scientific_checks.json
```

The verifier recomputes from stored predictions first, then evaluates fixed objects and official-source identities. It contains no `.fit()` calls. The expected current outcome is a nonzero exit at the documented metadata discrepancy; later scientific checks stay HOLD. Never widen a tolerance or change a reference merely to obtain PASS.

All actual scientific input paths are relative to the `--evidence-root` directory, and each has an exact SHA-256. Public aliases map to exact archive SHA/member paths. Missing files yield HOLD; an input hash mismatch or out-of-tolerance scientific comparison yields FAIL and stops subsequent families. The legacy six-column original table and full historical environment are missing provenance requirements; archived certificates alone do not recreate them.

The published report adds planned-input and LF-normalization metadata to the stopped execution output without altering any measurement or status. `verification/execution_artifacts.json` records the executed/reference file identities. SHA256SUMS records the final repository bytes.

## Review gates

1. Skeleton: approved for numerical QA at commit `24ffce246c755d97ec6c19ba052c94e1f98d6d01`.
2. Numerical QA: this stopped-run report requires independent feedback.
3. Release candidate: resolve science, provenance, safety and license; review the candidate snapshot.
4. GitHub v1.0.0: create only after explicit release approval, with final metadata and asset hashes.
5. Zenodo: verify metadata, archive linkage and DOI only after its review gate.

`CITATION.cff` remains the metadata authority. [Zenodo documents CFF support](https://help.zenodo.org/docs/github/describe-software/citation-file/) and gives `.zenodo.json` precedence when both exist; no second authority has been added.
