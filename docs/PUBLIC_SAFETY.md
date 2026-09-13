# Public safety review

**Current-tree gate: PASS. History-level gate: HOLD pending rewrite.**

The production-facing release-candidate tree passes the explicit public-content allowlist and lexical scan. It contains no raw NHANES XPTs, participant-level analytic tables, private research archives, manuscript files, journal correspondence, publisher PDFs, credentials, private contact files, or machine-specific paths.

The remaining privacy issue is historical only: earlier public commits contain a personal email address in commit author/committer metadata. The current branch uses GitHub noreply identities, but deleting a file or changing current metadata does not remove contact metadata already present in reachable Git history.

Before `v1.0.0`, rewrite the public Git history so the historical personal email is replaced by an approved noreply identity, force-update the relevant public refs, and rerun the all-history scan. Do not alter scientific file contents merely to rewrite commit metadata.

After the rewrite, verify all of the following on the final production commit:

1. `python scripts/verify_manifest.py` passes;
2. `python scripts/check_public_content.py` passes;
3. `python scripts/check_verification_report.py` passes;
4. `python scripts/check_final_scientific_summary.py` passes;
5. `python scripts/scan_git_history.py` passes across all production-reachable refs/tags;
6. `verification/scientific_checks_final.json` remains 16 PASS / 0 HOLD / 0 FAIL;
7. no scientific result, claim boundary, model, cohort rule, or calibration rule changes.

This is a bounded repository-safety audit, not a guarantee that every possible secret-detection pattern has been exhausted.
