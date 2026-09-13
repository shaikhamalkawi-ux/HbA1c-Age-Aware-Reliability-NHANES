# Source reconstruction

The locked source-reconstruction result is closed **PASS**:

- 2,325/2,325 retained historical rows match uniquely to NHANES 2017–2018 on the six stored matching fields;
- 0 ambiguous and 0 unmatched rows;
- 2,325 distinct recovered `SEQN` values;
- the 2,350→2,325 reduction is explained by 25 missing Friedewald-LDL results, all at TG≥400 mg/dL;
- the corrected primary cohort is N=2,219 after removing the irrelevant LDL-completeness restriction and applying the locked fasting eligibility.

The initial `WTSAF2YR` decimal-equality stop was adjudicated as representation/rounding only and cannot alter the zero-versus-positive fasting eligibility class. See [`verification/fasting_weight_adjudication.json`](../verification/fasting_weight_adjudication.json).

Public aggregate certificate:

- [`source_reconstruction_certificate.csv`](source_reconstruction_certificate.csv)

The original pre-reconstruction matching program was not recovered; source identity is verified through the preserved reconstructed table/certificate, exact official-source matching, and input hashes. This limitation is reported rather than filled by invented code.

See [scientific verification](../docs/SCIENTIFIC_VERIFICATION.md) and [input identities](../verification/evidence_inputs.json).
