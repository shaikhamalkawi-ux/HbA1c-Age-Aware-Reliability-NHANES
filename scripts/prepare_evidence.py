"""Materialize exact selected files from the locked archive into a private directory.

Selection uses SHA-256 identity, not an older archive's filename or version label.
Nothing in an archive is executed. Raw NHANES files are retrieved separately.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
def digest(data):return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    m=json.loads((ROOT/'verification/evidence_inputs.json').read_text());data=a.archive.read_bytes()
    if digest(data)!=m['root_archive_sha256']:raise ValueError('HOLD: supplied archive does not match the locked root SHA-256')
    wanted={r['path']:r for r in m['inputs']};found={};visited=set();total=0
    def visit(raw,depth=0):
        nonlocal total
        h=digest(raw)
        if h in visited:return
        if depth>8:raise ValueError('Archive nesting limit exceeded')
        visited.add(h)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for info in z.infolist():
                if info.is_dir():continue
                total+=info.file_size
                if total>2_000_000_000 or info.file_size>500_000_000:raise ValueError('Archive size limit exceeded')
                selected=[r for r in wanted.values() if r['archive_sha256']==h and r['archive_member']==info.filename]
                if selected or info.filename.lower().endswith('.zip'):
                    b=z.read(info)
                    for r in selected:
                        if digest(b)!=r['sha256']:raise ValueError('HOLD: selected source hash mismatch')
                        found[r['path']]=b
                    if info.filename.lower().endswith('.zip'):visit(b,depth+1)
    visit(data)
    if set(found)!=set(wanted):raise ValueError('HOLD: not every required locked input was recovered')
    out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    for name,b in found.items():
        target=(out/name).resolve()
        if not target.is_relative_to(out):raise ValueError('Invalid evidence alias')
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and target.read_bytes()!=b:raise ValueError('Refusing to overwrite different evidence')
        target.write_bytes(b)
    print(f'PASS: {len(found)} exact locked inputs materialized privately; no scientific code executed.')

if __name__=='__main__':main()
