# Reproducibility status

This checkpoint establishes a reviewable repository structure. It does not establish successful reproduction of the study.

## Available now

- The locked manuscript was available for local inspection; its byte-level identity was checked against the supplied reference hash. The manuscript itself is excluded from the repository.
- Locked numerical targets are recorded in `verification/locked_reference.json` as expected values, not observed outputs.
- Sixteen required scientific check families are registered in `verification/scientific_checks.json` with `NOT_RUN` status.
- Repository integrity and text-content checks are executable with Python 3.9 or later and the standard library.
- Citation metadata name Ghassan Malkawi as the sole repository/archive author, as instructed. Manuscript authorship is outside the scope of this metadata.

## Commands supported at this checkpoint

```sh
python scripts/verify_manifest.py
python scripts/check_public_content.py
```

Both commands exit nonzero if their stated checks fail. The content scanner is a bounded screening tool, not proof of ownership, licensing, or numerical correctness. Review the actual included files before each public update.

## Required before numerical reproduction

Original source files, split ledgers, stored predictions, calibration outputs, temporal target records, assay ledgers, CQR provenance, frozen objects, and ANFIS files must be inspected and mapped to public paths. Older bundles are candidate sources only; their presence does not establish consistency with the locked study.

No scientific scripts are invented or substituted at this checkpoint. No retraining, retuning, new cycle, changed cohort rule, or new post hoc analysis is authorized by the package checks.

For each scientific check, record input paths and hashes, executed command, actual observed value, expected value, tolerance justified by the original representation, and outcome. Mark `PASS` only after execution. A missing file or an unexecuted calculation remains `NOT_RUN` or `HOLD`. A discrepancy must be reported exactly and stops scientific release work; expected values must never be written into observed output fields.

## Review gates

1. Repository skeleton: independent review feedback required.
2. Reproducibility QA: execute checks after source intake and skeleton feedback; independent review required.
3. Public-release candidate: confirm content, metadata, license, and candidate commit; final feedback required.
4. GitHub production release v1.0.0: record commit and release-asset hashes; review before Zenodo finalization.
5. Zenodo: verify record, DOI, metadata, linkage, and final feedback.

No gate is inferred from passage of time or from a successfully created repository. The first repository snapshot is not final approval.
