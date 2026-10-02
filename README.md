# Subgroup calibration of HbA1c predictions across NHANES cycles

This repository provides public reproducibility and verification materials for the associated HbA1c study without redistributing participant-level NHANES data.

> **Hard age partitioning showed no demonstrated point-prediction benefit under the evaluated restricted model, while subgroup calibration conclusions depended on the calibration partition, interval width, summary metric, and source split.**

Scientific verification of the original submitted analysis remains closed PASS: **16/16 registered scientific check families PASS**. It does not claim fresh end-to-end retraining of every model family from raw CDC files.

## Source reconstruction

The historical analysis used a table of 2,325 adults. All 2,325 rows were linked uniquely to NHANES 2017-2018 using exact agreement at the stored precision on age, BMI, fasting glucose, triglycerides, HbA1c, and Friedewald LDL: **2,325 exact unique matches, 0 ambiguous, 0 unmatched**.

The corrected development cohort contains **2,219 adults**, with **666 / 991 / 562** in the age groups **20-39 / 40-64 / 65+**.

## Original point-prediction findings

| Model | Repeated-OOF RMSE |
|---|---:|
| Pooled OLS | 0.5732523422 |
| Hard-age OLS | 0.5774212775 |
| Glucose-only OLS | 0.5862355212 |
| SmoothVC OLS | 0.5911837422 |
| Pooled LightGBM | 0.5937450777 |
| Hard-age LightGBM | 0.6601329856 |

Hard-age OLS minus pooled OLS was **+0.0041689353**, with participant-bootstrap 95% CI **[-0.0026392765, +0.0122600322]**. This is not interpreted as an equivalence test.

## R1.2 sensitivity summary

The major-revision sensitivity analyses are post hoc and are not described as prospectively prespecified.

Across 200 common source fitting/calibration splits, mean forward age-coverage spread was:
- global residual: **7.40 percentage points**;
- age-Mondrian: **4.27 percentage points**;
- fasting-glucose Mondrian: **2.51 percentage points**;
- predicted-HbA1c bins: **4.18 percentage points**.

In the fixed forward evaluation, the paired spread change was **-2.66 percentage points** with a 95% participant-bootstrap interval of **-6.15 to +0.32**, while the minimum-group-coverage change was **-0.33 points** with a 95% interval of **-1.75 to +2.30**.

Across 200 point-model refitting partitions, the mean hard-minus-pooled OLS RMSE difference was **+0.003523**; hard-age OLS had higher RMSE in **91%** of runs. In the masked-PSU grouped sensitivity, the mean difference was **+0.003935** and hard-age OLS had higher RMSE in **98.5%** of runs.

A public-safe machine-readable summary is provided under derived_outputs/revision_r1_2/.

## Temporal evaluation hierarchy

The **2021-2023 NHANES cycle is the forward temporal evaluation**. The **2015-2016 cycle is a secondary adjacent-cycle stress test**. Both use frozen source models/calibration, without target retraining or target recalibration.

These are independent cross-sectional samples within NHANES, not longitudinal follow-up and not validation in an independent clinical system.

## Public data and repository policy

Raw NHANES XPT files, participant-level analytic tables, and participant-level predictions are not redistributed here. The repository intentionally excludes journal correspondence, private conversations, manuscript files, private contact files, participant-level derived tables, and internal project-transfer archives.

## Associated manuscript

**Subgroup Calibration of HbA1c Predictions Across NHANES Cycles: Partition Choice and Temporal Transport**

Current manuscript author order:
1. Hussien Alwedyan
2. Ghassan Malkawi
3. Ahmed Abdelaziz Elsayed
4. Abdulwehab Ibrahim
5. Ashraf AlShalalfeh
6. Rafiq Manna
7. Mohanad Alata
8. Mohammad AlWedian

Repository creator: Ghassan Malkawi. Repository creation and associated-manuscript authorship are separate roles.

## Citation and repository record

For the current manuscript, the public reproducibility route is this **GitHub repository only**. No Zenodo DOI is cited or required for the resubmission.

Repository citation metadata are maintained in CITATION.cff.
