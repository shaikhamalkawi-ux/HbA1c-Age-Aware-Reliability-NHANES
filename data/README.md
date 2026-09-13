# Data access and eligibility

Raw NHANES files and participant-level extracts are not included in this scaffold. Data should be obtained from the official CDC/NCHS NHANES website. Exact component download URLs and retrieved file hashes will be locked during source intake.

Official entry point: https://www.cdc.gov/nchs/nhanes/

| Cycle | Role | Components identified in the locked study |
|---|---|---|
| 2017–2018 (J) | Source reconstruction and development | DEMO_J, BMX_J, GHB_J, GLU_J, TRIGLY_J |
| 2015–2016 (I) | Backward temporal evaluation | DEMO_I, BMX_I, GHB_I, GLU_I, TRIGLY_I |
| August 2021–August 2023 (L) | Forward temporal evaluation | Corresponding demographic, body-measurement, HbA1c, glucose, and triglyceride components |

The locked development eligibility is age at least 20 years; complete BMI, fasting glucose, TG and HbA1c; fasting duration at least 8 and less than 24 hours; and positive fasting-subsample weight. LDL completeness is not an eligibility requirement. Age groups are 20–39, 40–64, and 65+. A public age value of 80 denotes 80+.

Component variable names, cycle-specific weight/time fields, import types, unit conversions, and join validation must be checked against the original implementation and official component documentation before an executable retrieval/reconstruction command is published. This file is not a substitute reconstruction algorithm.

Do not mix raw and assay-harmonized triglycerides, or raw and already harmonized glucose. Preserve the original cycle-specific assay rules. See [the data dictionary](../docs/DATA_DICTIONARY.md).
