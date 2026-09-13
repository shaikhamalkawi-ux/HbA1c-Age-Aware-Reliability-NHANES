"""Download official NHANES components privately and record exact retrieved bytes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

COMPONENTS = {
    'DEMO': (['SEQN','RIDAGEYR','SDMVSTRA','SDMVPSU','WTMEC2YR'], 'Join identifier, age/top coding, survey design and MEC sensitivity weight.'),
    'BMX': (['SEQN','BMXBMI'], 'BMI predictor, kg/m2.'),
    'GLU': (['SEQN','LBXGLU','WTSAF2YR'], 'Fasting glucose predictor, mg/dL; fasting-subsample eligibility and sensitivity weight.'),
    'TRIGLY': (['SEQN','LBXTR','LBDLDL'], 'Triglyceride predictor, mg/dL; Friedewald LDL for historical missingness reconstruction only.'),
    'GHB': (['SEQN','LBXGH'], 'HbA1c outcome, percent; never a target-training input.'),
    'FASTQX': (['SEQN','PHAFSTHR','PHAFSTMN'], 'Fasting duration. Explicit source-cycle gate; auxiliary provenance for temporal cycles, which use the frozen positive-weight gate.'),
}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--verify-against',type=Path)
    a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
    expected={r['filename']:r['sha256'] for r in json.loads(a.verify_against.read_text())['files']} if a.verify_against else {}
    def get(task):
        year,suffix,cycle,comp=task; filename=f'{comp}_{suffix}.xpt'
        url=f'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year}/DataFiles/{filename}'
        req=urllib.request.Request(url,headers={'User-Agent':'NHANES-reproducibility-check/1.0'})
        with urllib.request.urlopen(req,timeout=60) as response:
            data=response.read(); final_url=response.url
        if not data.startswith(b'HEADER RECORD*******LIBRARY HEADER RECORD!!!!!!!'):
            raise ValueError(f'{filename}: response is not a SAS XPORT file')
        sha=hashlib.sha256(data).hexdigest()
        if filename in expected and sha!=expected[filename]:raise ValueError(f'{filename}: official download changed; HOLD, do not overwrite locked evidence')
        (a.output_dir/filename).write_bytes(data)
        variables,role=COMPONENTS[comp];variables=list(variables)
        if suffix=='L' and comp=='TRIGLY':
            variables[1]='LBXTLG';role='New triglyceride assay; frozen backward bridge: old-scale TG = -12.19 + 0.9785 * LBXTLG. LDL is not an eligibility gate.'
        if suffix=='I' and comp=='GLU':role+=' Released glucose values already incorporate the CDC instrument adjustment; no second bridge.'
        return dict(filename=filename,cycle=cycle,url=url,resolved_url=final_url,documentation_url=url[:-4]+'.htm',accessed_at_utc=datetime.now(timezone.utc).isoformat(),sha256=sha,bytes=len(data),variables=variables,role=role,status='DOWNLOADED_AND_XPORT_SIGNATURE_VERIFIED')
    tasks=[(y,s,c,k) for y,s,c in [(2015,'I','2015-2016'),(2017,'J','2017-2018'),(2021,'L','2021-2023')] for k in COMPONENTS]
    with ThreadPoolExecutor(max_workers=4) as pool:files=list(pool.map(get,tasks))
    a.manifest.parent.mkdir(parents=True,exist_ok=True)
    a.manifest.write_text(json.dumps(dict(scope='Official files downloaded during verification; hashes describe these retrieved bytes, not unrecorded historical download hashes.',raw_files_public=False,files=files),indent=2)+'\n')
    print(f'PASS: {len(files)} official components downloaded; raw files kept in the requested private directory.')

if __name__=='__main__':main()
