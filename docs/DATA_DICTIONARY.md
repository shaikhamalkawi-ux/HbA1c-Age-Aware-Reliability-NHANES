# Data dictionary: semantic specification

This dictionary records roles and units described by the locked manuscript. Mapping to exact source column names remains pending original-file and official-codebook verification. It does not claim that a public data table is already included.

| Concept | Role | Units / interpretation |
|---|---|---|
| NHANES participant identifier (SEQN) | Join key and participant-level audit key | Identifier, not a model input |
| Age (RIDAGEYR) | Predictor and predefined grouping | Years; 80 denotes 80+ |
| Body mass index | Predictor | kg/m² |
| Fasting glucose | Predictor | mg/dL; follow cycle-specific published assay handling |
| Triglycerides | Predictor | mg/dL; distinguish raw and harmonized values |
| Measured HbA1c | Same-examination outcome | Percent |
| Calculated Friedewald LDL | Legacy source-reconstruction field | mg/dL; excluded from primary predictor/eligibility requirements |
| Fasting duration | Eligibility | At least 8 and less than 24 hours |
| Fasting-subsample weight | Eligibility and weighted sensitivities | Positive; exact field depends on source cycle |
| Age group | Prespecified grouping | 20–39, 40–64, 65+ |
| Repeat and outer fold | Evaluation provenance | Participant-level repeated out-of-fold allocation |

The locked forward TG bridge is `TG_old = -12.19 + 0.9785 * LBXTLG_new`, with both quantities in mg/dL. This is a reference specification from the manuscript; its implementation and official source documentation remain to be checked. Raw TG has a distinct sensitivity role.

Predictions, calibration-only residuals, interval endpoints, and bootstrap outputs must retain their evaluation-role identifiers. Training, calibration, and test membership must never be inferred from row order alone.
