# Included and excluded materials

## Public scientific/reproducibility contents

The repository publishes public-safe documentation, verification code, exact source identities, and aggregate outputs. Participant-level material remains excluded.

### Core documentation and metadata

- `README.md`
- `CITATION.cff`
- `LICENSE_PENDING.md` until the author approves the production license mapping
- `docs/CLAIM_BOUNDARIES.md`
- `docs/REPRODUCIBILITY.md`
- `docs/ENVIRONMENT.md`
- `docs/SCIENTIFIC_VERIFICATION.md`
- `docs/PUBLIC_SAFETY.md`
- `docs/LICENSE_DECISION.md`
- checkpoint notes retained during review but removed from the production tag

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

## Production snapshot cleanup

Before `v1.0.0`:

1. remove `docs/CHECKPOINT_1.md`, `docs/CHECKPOINT_2.md` and `docs/zenodo_metadata_draft.json` from the tagged source snapshot;
2. replace `LICENSE_PENDING.md` with the author-approved license notices and material mapping;
3. update `CITATION.cff` with the approved license, version `1.0.0`, and verified release date;
4. close the documented Git-history contact-metadata finding and rerun the all-history scan;
5. regenerate the exact allowlist, manifest and public-content report for the production commit.
