"""Validate the public report's arithmetic bookkeeping and byte identities, without scientific inputs."""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    r=read('verification/scientific_checks.json');errors=[]
    def check(ok,message):
        if not ok:errors.append(message)
    counts=Counter(c['status'] for c in r['checks'])
    check(len(r['checks'])==16,'Expected sixteen scientific families')
    check(len({c['id'] for c in r['checks']})==16,'Duplicate scientific family')
    check(all(r['counts'][s]==counts[s] for s in ['PASS','HOLD','FAIL']),'Family counts do not agree')
    check(r['overall_status']==('FAIL' if counts['FAIL'] else 'HOLD' if counts['HOLD'] else 'PASS'),'Overall scientific status does not agree')
    maps={x['path']:x for x in read('verification/execution_artifacts.json')['artifacts']}
    for path,x in maps.items():
        b=(ROOT/path).read_bytes();check(sha(b)==x['repository_sha256'],'Repository artifact identity: '+path)
        executed=b.replace(b'\n',b'\r\n') if x['change']=='CRLF to LF only' else b
        check(sha(executed)==x['executed_sha256'],'Executed artifact identity: '+path)
    manifest=read('verification/evidence_inputs.json');inputs={x['path']:x['sha256'] for x in manifest['inputs']}
    inputs.update({'nhanes/'+x['filename']:x['sha256'] for x in read('verification/data_provenance.json')['files']})
    for c in r['checks']:
        check(c['script_sha256']==maps['scripts/verify_science.py']['executed_sha256'],'Executed script identity: '+c['id'])
        for x in c['reference_inputs']:check(x['sha256']==maps[x['path']]['executed_sha256'],'Executed reference identity: '+x['path'])
        for x in c['inputs']:check(x['sha256']==inputs[x['path']],'Scientific input identity: '+x['path'])
        for x in c.get('planned_inputs',[]):check(x['sha256']==inputs[x['path']],'Planned input identity: '+x['path'])
        for m in c['measurements']:
            check((m['absolute_difference']<=m['tolerance'])==(m['status']=='PASS'),'Measurement classification: '+m['name'])
            e,o=m['expected'],m['observed']
            diff=(0 if e==o else 1) if isinstance(e,(str,bool)) or e is None else abs(o-e)
            check(diff==m['absolute_difference'],'Measurement difference: '+m['name'])
        if c['status']=='PASS':check(c['executed'] and len(c['measurements'])>0 and all(m['status']=='PASS' for m in c['measurements']),'Unsupported PASS: '+c['id'])
        if not c['executed']:check(c['status']=='HOLD' and not c['measurements'] and c.get('observed') is None,'Stopped check has observed data: '+c['id'])
    check(not r['training_refit_performed'] and not r['target_recalibration_performed'],'Unexpected refit/adaptation claim')
    print(json.dumps(dict(status='FAIL' if errors else 'PASS',scope='Public audit bookkeeping and serialization identities only; no scientific rerun.',scientific_status=r['overall_status'],scientific_counts=r['counts'],errors=errors),indent=2))
    return 1 if errors else 0

if __name__=='__main__':raise SystemExit(main())
