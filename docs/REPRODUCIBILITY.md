# Reproducibility and replay

The original scientific verification is **16 PASS / 0 HOLD / 0 FAIL** across the registered scientific check families.

The verifier contains no model training or retuning. It recomputes metrics from stored predictions/intervals, checks frozen objects and hashes, verifies source/target cohort identities, replays the TG bridge, and evaluates the historical fixed FIS models. The recovered original CQR PASS is limited to stored-output arithmetic; original fitted CQR learner objects were not recovered.

The repository exposes public-safe aggregate verification artifacts under derived_outputs/, including a separate revision_r1_2/ summary for the major-revision sensitivities.

Raw NHANES XPT files, participant-level analytic cohorts, participant predictions, split ledgers, and private research archives are deliberately excluded.

## Repository status

The current manuscript uses this GitHub repository as its public reproducibility resource. CITATION.cff is the metadata authority for repository citation. No Zenodo deposit or DOI is required for the resubmission.
