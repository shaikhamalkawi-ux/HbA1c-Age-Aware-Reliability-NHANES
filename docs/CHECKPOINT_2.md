# Checkpoint 2 review entry — final adjudicated

**16 PASS / 0 HOLD / 0 FAIL. Scientific verification is closed PASS. Production release and Zenodo remain HOLD for license approval and final public-release review only.**

The first verification run stopped on a `WTSAF2YR` decimal-representation discrepancy. Independent adjudication showed that the archived maximum `944153.2498` is the rounded representation of the CDC-published maximum `944153.24975`. The difference cannot change the zero-versus-positive fasting eligibility gate. No locked scientific value was changed and no general tolerance was widened.

- [Final scientific report](SCIENTIFIC_VERIFICATION.md)
- [Final machine-readable checks](../verification/scientific_checks_final.json)
- [Fasting-weight adjudication](../verification/fasting_weight_adjudication.json)
- [Exact CDC sources and hashes](../data/README.md)
- [Archived input paths and hashes](../verification/evidence_inputs.json)
- [Environment and known limits](ENVIRONMENT.md)
- [Public-content and Git-history safety](PUBLIC_SAFETY.md)
- [New admissions and exclusions](CONTENTS.md)
- [License option awaiting approval](LICENSE_DECISION.md)

Ghassan Malkawi remains the sole repository/archive creator. Associated manuscript authors are listed separately and unchanged in the README. No preferred manuscript citation, invented DOI/ORCID, production tag or Zenodo record has been added.

Before any production `v1.0.0` snapshot, remove `docs/CHECKPOINT_1.md`, this checkpoint note and `docs/zenodo_metadata_draft.json`; remove `LICENSE_PENDING.md` after license approval. Add the approved CFF license, version `1.0.0`, and verified release date only after the release gates close. `CITATION.cff` is the intended metadata authority; no competing `.zenodo.json` is used.

**Checkpoint 2 decision: GO to public-release preparation; HOLD release/Zenodo until the license and public-history decisions are resolved.**
