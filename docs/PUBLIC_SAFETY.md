# Public safety review

**History-level gate: FAIL.** The four existing public commits through `24ffce246c755d97ec6c19ba052c94e1f98d6d01` include a personal email address in commit author/committer metadata (seven occurrences). The address is not reproduced in reports; only its one-way fingerprint identifies repeated findings. No history rewrite or deletion is authorized by this report.

The history scan inspected all reachable commit trees, 34 unique path/blob pairs, messages and contact metadata. No content-file finding was detected in that historical snapshot. The initial repository commit preceded the allowlist; its tree was still screened by the lexical/type rules. See [exact scanned commits and redacted findings](../verification/history_safety_report.json).

The current file inventory is separately checked by [check_public_content.py](../scripts/check_public_content.py), the explicit [allowlist](../verification/public_allowlist.json), and SHA256SUMS. Its generated report is [public_content_report.json](../verification/public_content_report.json). Raw NHANES, participant tables, MAT arrays, original research archives, manuscripts, publisher PDFs, credentials, private correspondence and host paths are excluded.

These are bounded lexical/type/allowlist scans supplemented by file-admission review; they cannot prove the absence of every possible secret. The current source snapshot and all historical commits have distinct status. A passing tree scan does not clear a historical contact finding.

Before a production tag, resolve the existing contact metadata and use a verified GitHub noreply commit identity for future commits. Then repeat the all-ref/all-tag scan. The minimal CI intentionally fails its history gate while a historical finding remains; scientific HOLD/FAIL findings are also explicit in the stored report, not represented as successful reproduction.

GitHub email privacy was enabled during checkpoint preparation, and the interface confirmed that future web-based Git operations use the account noreply identity. This does not remove the historical contact findings.
