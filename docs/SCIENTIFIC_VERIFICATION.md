# Scientific verification: checkpoint 2

**Result: 11 PASS / 4 HOLD / 1 FAIL across 16 scientific check families. Overall FAIL; release HOLD.** The verifier stopped at the first out-of-tolerance discrepancy. No locked numerical value, input, model or calibration was repaired. No refit, retuning or target recalibration occurred.

## Stop-triggering discrepancy

The six-field reconstructed historical table matches all 2,325 retained CDC records exactly on age, BMI, fasting glucose, triglycerides, HbA1c and LDL; there are zero unmatched, ambiguous or identifier-disagreeing candidates. The official historical core has 2,350 rows before LDL completeness, with 25 missing LDL results, all TG >=400.

However, the additional metadata comparison found a maximum absolute `WTSAF2YR` difference of **5.000003147870302e-05** between the stored reconstruction and the current official J-cycle fasting weights. Expected difference: 0. Declared tolerance: **1e-08**, chosen before execution for decimal serialization of large survey weights. The test therefore **FAILS**. The cause and consequences have not been adjudicated; a rounding explanation is not assumed and the tolerance was not widened.

Exact compared inputs, relative to the private evidence root:

| Input | SHA-256 |
| --- | --- |
| `reconstruction.csv` | `83d83fde9b20efc951984ff619f7f9d5d877b17f299edfe9b58e6a39a380fcac` |
| `nhanes/GLU_J.xpt` | `5b38897d0d7bfbc69dd9ca74ffdaf2f6a9bed5a91d4a7bf46e07f1332cc3379e` |

Full dependencies, expected/observed measurements, differences, tolerances and commands are in [scientific_checks.json](../verification/scientific_checks.json). All 52 selected archived inputs and 18 CDC components have recorded identities. Planned inputs of stopped checks are marked separately; their observed values remain null.

## Family results and every nonzero difference

There are 1734 executed comparisons: 1733 pass and 1 fails. 663 comparisons have nonzero differences; none are hidden by formatting. The JSON includes each one at full serialized precision. Maxima below combine unlike quantities and must not be compared as effect sizes.

| Family | Status | Executed comparisons | Maximum absolute difference |
| --- | --- | --- | --- |
| `reconstructed_cohort` | **FAIL** | 33 | 5.000003147870302e-05 |
| `corrected_cohort` | **HOLD** | 0 | not run |
| `age_group_counts` | **HOLD** | 0 | not run |
| `point_model_rmse` | **PASS** | 55 | 4.787706581188544e-07 |
| `paired_contrasts` | **PASS** | 22 | 6.46785430985855e-08 |
| `bootstrap_ci` | **PASS** | 63 | 2.7645110165777295e-07 |
| `global_q` | **PASS** | 207 | 1.7763568394002505e-15 |
| `mondrian_q` | **PASS** | 211 | 1.7763568394002505e-15 |
| `age_coverage` | **PASS** | 294 | 4.8032290611566e-07 |
| `interval_metrics` | **PASS** | 352 | 5.329070518200751e-15 |
| `temporal_counts` | **HOLD** | 0 | not run |
| `temporal_metrics` | **PASS** | 302 | 4.002667466362908e-07 |
| `tg_bridge` | **HOLD** | 0 | not run |
| `original_cqr` | **PASS** | 164 | 3.552713678800501e-15 |
| `frozen_hashes` | **PASS** | 13 | 0 |
| `anfis_parameters` | **PASS** | 18 | 4.987272998798614e-07 |

Six-decimal manuscript numbers use a 5e-7 half-unit rounding tolerance. Stored metric and quantile arithmetic uses absolute 1e-12, with no relative tolerance. FIS-versus-MATLAB fixed evaluation uses the original verifier's 1e-10 tolerance; printed FIS parameters must agree after six-decimal rounding. All tolerances and exact differences are recorded per measurement.

## What PASS establishes

The repeated-OOF RMSEs were computed from stored predictions. Paired contrasts and 10,000-replicate participant bootstrap intervals were recomputed using the original seed 20260912, participant-level SSE across five repeats, fixed contrast/group order and 250-draw batches. Frozen global/age calibration quantiles were recomputed from calibration-only residuals; internal calibration/test separation and stored quantiles were checked.

Coverage, widths and scores were recomputed from stored intervals. Original CQR checks use recovered original internal/forward outputs and preserve their secondary status. Temporal prediction, point/interval metrics and descriptive calibration arithmetic were recomputed from stored frozen predictions. Calibration regression is diagnostic only; no predictor or interval was updated. Three historical FIS models, 41 rules and 533 parameters were checked with fixed-model evaluation.

## Remaining limits

- Corrected-cohort reconstruction, its separate age-count check, official temporal target counts and the TG bridge check were not executed after the stop. Their HOLD status does not imply a demonstrated discrepancy in those results.
- The locked archive contains a reconstructed six-field table and a matching certificate. Its original MAT arrays have five data columns. The pre-reconstruction six-column legacy table and original matching implementation were not found. The further five-field MAT-to-source check was not reached before the stop.
- Original fitted CQR objects and complete calibration quantile predictions were not found. PASS is limited to original stored-output arithmetic and freeze consistency; later exploratory models were not substituted.
- Known original library versions are recorded, but the full original environment remains incomplete. See [environment record](ENVIRONMENT.md).
- A history-wide scan found personal contact metadata in existing commits. The report redacts the address and keeps the issue open. See [public safety](PUBLIC_SAFETY.md).

## Provenance and reproduction

The root archive matches the previously supplied SHA-256 `7df5030e47723024eaa835a40e07d680db7a7ccabc323f2adc09907be43dc056`. Ten nested archive identities are linked to their parents; 43 root-manifest entries and 57 original-core manifest entries pass. No externally located older archive was substituted. [Source intake](../verification/source_intake.json) records this chain.

`scripts/verify_science.py` is a transparent read-only audit adapter, not the original training program. Its bootstrap formulas follow the hashed recovered postprocess script. The inspected FIS parser/evaluator was extracted without its executable generation routine. The original scripts remain private evidence inputs with hashes; they are not run or publicly redistributed with their machine paths.

The executable/reference byte hashes from the actual run are preserved. Public LF normalization changes only line endings; [execution_artifacts.json](../verification/execution_artifacts.json) maps executed and repository byte hashes. No observed number or scientific status was changed during packaging. [Reproduction instructions](REPRODUCIBILITY.md) explain independent replay and its expected stop.

**Requested review decision:** adjudicate the fasting-weight discrepancy and missing original provenance/environment evidence before resuming scientific work. Production v1.0.0, license adoption and Zenodo remain HOLD.
