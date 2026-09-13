# Scientific verification: checkpoint 2 — final adjudicated result

**Final result: 16 PASS / 0 HOLD / 0 FAIL across 16 registered scientific check families. Production release and Zenodo remain HOLD only for license approval and final public-release review.**

No locked scientific result, numerical value, dataset, model, calibration rule, or claim boundary was changed. No target retraining or recalibration occurred. No new model family was introduced.

## Adjudication of the initial stop

The first checkpoint run stopped because the archived reconstruction CSV and the freshly retrieved official `GLU_J.xpt` differed in `WTSAF2YR` by at most **5.000003147870302e-05**, while the initial generic metadata tolerance had been set to `1e-8`.

This discrepancy is now resolved as a representation/rounding issue, not a source-identity discrepancy:

- the official CDC codebook reports the positive `WTSAF2YR` range as **9133.518063 to 944153.24975**;
- the archived reconstruction stores the maximum as **944153.2498**;
- the decimal difference is exactly **0.00005**, matching the stop-triggering maximum discrepancy;
- all 2,325 retained records still agree exactly and uniquely on the six source-matching fields (age, BMI, fasting glucose, triglycerides, HbA1c, Friedewald LDL), with 0 unmatched and 0 ambiguous rows;
- `WTSAF2YR` missingness agrees, and the discrepancy is far too small to change a zero-versus-positive eligibility classification: the minimum positive official weight is 9133.518063.

Therefore the cohort/source identity result is **PASS**. We did **not** widen a global scientific tolerance. Exact equality remains required for identifiers, discrete memberships, source fingerprints, counts, and locked scientific outputs. The complete adjudication is machine-readable in [`verification/fasting_weight_adjudication.json`](../verification/fasting_weight_adjudication.json).

Official CDC documentation: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/GLU_J.htm

## Final family-level results

| Check family | Status | Verification basis |
|---|---|---|
| Reconstructed cohort/source identity | **PASS** | 2,325/2,325 exact unique six-field matches; WTSAF2YR rounding adjudicated separately |
| Corrected fasting cohort | **PASS** | N=2,219; unique SEQN; positive fasting weights; 480–1439 fasting minutes |
| Age-group counts | **PASS** | 666 / 991 / 562 |
| Point-model RMSE | **PASS** | Direct recomputation from 66,570 stored repeated-OOF prediction rows |
| Paired contrasts | **PASS** | Direct recomputation from paired stored OOF predictions |
| Participant bootstrap CI | **PASS** | Exact 10,000-resample replay; seed 20260912 |
| Global conformal q | **PASS** | Fresh deterministic 1,775/444 source split and residual order statistics |
| Age-Mondrian q | **PASS** | Fresh group-specific source-calibration quantiles |
| Age coverage | **PASS** | Direct recomputation from stored interval endpoints |
| Interval width/score metrics | **PASS** | Direct interval arithmetic |
| Temporal target counts | **PASS** | N=2,235 and N=2,808; age counts independently recomputed |
| Temporal metrics | **PASS** | RMSE/calibration arithmetic recomputed from frozen target predictions |
| TG bridge | **PASS** | Exact replay of `TG_old = -12.19 + 0.9785 * TG_new`; max difference 0 |
| Recovered original CQR | **PASS** | Stored-output arithmetic recomputed; max discrepancy ~4.44e-16; no learner-refit claim |
| Frozen hashes | **PASS** | Frozen source-model/calibration JSON and role-ledger SHA-256 identities match |
| Historical ANFIS parameters | **PASS** | 3 FIS, 41 rules, 533/533 parameters at 6 d.p.; prediction replay ~1.47e-12 max difference |

The final machine-readable values are in [`verification/scientific_checks_final.json`](../verification/scientific_checks_final.json).

## Key recomputed values

### Repeated OOF point prediction

- pooled OLS: `0.5732523421784678`
- hard-age OLS: `0.5774212774999247`
- glucose-only OLS: `0.5862355212293419`
- SmoothVC OLS: `0.591183742180368`
- pooled LightGBM: `0.5937450777180617`
- hard-age LightGBM: `0.6601329855676891`

Hard-age OLS minus pooled OLS: `+0.004168935321456901`; participant-bootstrap 95% CI `[-0.0026392764511016576, 0.012260032153039797]`.

### Frozen conformal calibration

Global absolute-residual quantiles:

- q90 `0.8070130279745653`
- q95 `1.1398926919235173`

Age-Mondrian q90:

- 20–39: `0.6394855277780342`
- 40–64: `0.7539988977539949`
- 65+: `1.0327313959681845`

Age-Mondrian q95:

- 20–39: `0.919630883391906`
- 40–64: `1.231843406783268`
- 65+: `2.1898158949662268`

Primary 90% coverage by age:

- global: `0.9621621621621622 / 0.8928355196770938 / 0.8562277580071175`
- age-Mondrian: `0.912012012012012 / 0.9037336024217961 / 0.893594306049822`

Overall 90% interval scores:

- global: `2.68707924518505`
- age-Mondrian: `2.6385159688983326`

### Temporal transport

Backward 2015–2016:

- N `2235`; age counts `712 / 970 / 553`
- RMSE `0.6579939891772845`
- calibration slope `1.0421080502582822`

Forward 2021–2023:

- N `2808`; age counts `670 / 1203 / 935`
- RMSE `0.567695949765773`
- calibration slope `1.047288084302036`

Forward TG bridge replay had maximum absolute difference `0.0 mg/dL`.

## CQR and ANFIS boundaries

Recovered original CQR checks are limited to the archived original interval outputs and preserved source/tuning records. Original fitted CQR learner objects were not recovered, so this PASS does **not** claim a complete original learner refit. The later fixed-configuration CQR remains post hoc exploratory and is not substituted for the recovered original analysis.

The historical ANFIS checks establish structural/computational fidelity only. They do not establish independent predictive superiority or biological meaning of rule counts.

## Environment and reproducibility boundary

The locked original analytical record identifies Python 3.13.5 with NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0 and LightGBM 4.6.0; later QA records also identify SciPy 1.17.0 and matplotlib 3.10.8. The independent arithmetic QA was also replayed in an isolated environment. Exact environment details and known limitations are in [`ENVIRONMENT.md`](ENVIRONMENT.md).

Checkpoint 2 verifies the reported analysis outputs and frozen calculation artifacts. It does **not** claim that every original model family was freshly retrained end-to-end from the raw CDC XPT files.

## Public-release gates still open

Scientific verification is closed **PASS**. The remaining release blockers are administrative/publication-engineering issues only:

1. author approval of the repository license mapping;
2. final public-content/history review;
3. clean `v1.0.0` release metadata;
4. Zenodo ingestion and DOI verification.

The historical checkpoint report that originally stopped at the survey-weight representation mismatch is retained in Git history for auditability; it was not silently deleted or rewritten.
