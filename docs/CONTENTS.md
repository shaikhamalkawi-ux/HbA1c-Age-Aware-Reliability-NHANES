# Included and excluded materials

## Public scientific/reproducibility contents

The release candidate publishes public-safe documentation, verification code, exact source identities, aggregate outputs, and frozen certificates. Participant-level material remains excluded.

### Core documentation and metadata

- `README.md`
- `CITATION.cff`
- `RELEASE_NOTES_v1.0.0.md`
- `LICENSE` — MIT for original code where the author has authority to grant it
- `CONTENT_LICENSE.md` — CC BY 4.0 for original documentation, original figures, and original aggregate derived materials where the applicable rightsholder has authority to grant it
- `docs/CLAIM_BOUNDARIES.md`
- `docs/REPRODUCIBILITY.md`
- `docs/ENVIRONMENT.md`
- `docs/SCIENTIFIC_VERIFICATION.md`
- `docs/PUBLIC_SAFETY.md`
- `docs/LICENSE_DECISION.md`

### Data/source provenance

- `data/README.md` — exact official CDC component URLs, access date, downloaded hashes, variables and assay roles
- `data/NHANES_Assay_Source_Ledger.csv` — analysis-facing assay/harmonization ledger
- `source_reconstruction/source_reconstruction_certificate.csv` — aggregate reconstruction/cohort certificate
- `verification/data_provenance.json`, `verification/evidence_inputs.json`, and related identity records

### Aggregate verified outputs

- `derived_outputs/point_model_metrics.csv`
- `derived_outputs/point_model_paired_bootstrap.csv`
- `derived_outputs/primary_interval_metrics.csv`
- `derived_outputs/temporal_metrics.csv`
- `derived_outputs/recovered_original_cqr_metrics.csv`
- `derived_outputs/legacy_anfis_verification.csv`
- `frozen_objects/frozen_temporal_ols_conformal_certificate.json`

### Verification code and reports

- repository manifest/content/history checks
- CDC retrieval and evidence-materialization helpers
- read-only scientific verifier plus the narrowly adjudicated final wrapper
- `verification/scientific_checks_final.json` — final 16/16 PASS summary
- `verification/fasting_weight_adjudication.json` — explicit resolution of the WTSAF2YR representation difference

## Intentionally excluded from public distribution

- raw NHANES XPT files (retrieved from official CDC URLs instead)
- participant-level cohorts and reconstructed participant tables
- participant-level OOF predictions and interval endpoints
- split/role ledgers containing participant identifiers
- private/nested research archives and machine-specific paths
- manuscript PDFs/source, journal correspondence, reviewer packages and chat-transfer archives
- publisher/literature PDFs and other third-party copyrighted material
- credentials, tokens and private contact files
- unreconciled duplicate/historical outputs

The public repository is intended to expose enough aggregate evidence, code, source hashes and provenance to inspect the reported analysis without republishing participant-level records.

## Remaining production gates

The license gate is complete. Before `v1.0.0`:

1. close the documented Git-history contact-metadata finding and rerun the all-history scan;
2. regenerate the exact allowlist, manifest and public-content report for the final production commit;
3. add the verified release date to `CITATION.cff` at the time of the actual production release;
4. create the GitHub release and verify Zenodo ingestion/DOI metadata.
