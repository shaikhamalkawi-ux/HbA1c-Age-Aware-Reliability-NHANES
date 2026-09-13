"""Validate the final adjudicated scientific-summary contract without private inputs."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = ROOT / 'verification' / 'scientific_checks_final.json'
    if not p.is_file():
        print('FAIL: verification/scientific_checks_final.json missing')
        return 1
    r = json.loads(p.read_text(encoding='utf-8'))
    errors = []
    checks = r.get('checks', [])
    if len(checks) != 16:
        errors.append(f'expected 16 check families, found {len(checks)}')
    if len({c.get('id') for c in checks}) != len(checks):
        errors.append('duplicate scientific check id')
    counts = {s: sum(c.get('status') == s for c in checks) for s in ('PASS', 'HOLD', 'FAIL')}
    if counts != {'PASS': 16, 'HOLD': 0, 'FAIL': 0}:
        errors.append(f'unexpected final status counts: {counts}')
    if r.get('overall_status') != 'PASS':
        errors.append('overall_status must be PASS')
    if r.get('locked_science_changed') is not False:
        errors.append('locked_science_changed must be false')
    if r.get('full_primary_training_refit_performed') is not False:
        errors.append('full_primary_training_refit_performed must be false')
    ids = {c.get('id') for c in checks}
    required = {
        'reconstructed_cohort','corrected_cohort','age_group_counts','point_model_rmse',
        'paired_contrasts','bootstrap_ci','global_q','mondrian_q','age_coverage',
        'interval_metrics','temporal_counts','temporal_metrics','tg_bridge','original_cqr',
        'frozen_hashes','anfis_parameters'
    }
    if ids != required:
        errors.append('scientific check-family set is not the locked 16-family contract')
    print(json.dumps({
        'status': 'FAIL' if errors else 'PASS',
        'scope': 'Final adjudicated summary structure/status only; no private scientific inputs are rerun.',
        'counts': counts,
        'errors': errors,
    }, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
