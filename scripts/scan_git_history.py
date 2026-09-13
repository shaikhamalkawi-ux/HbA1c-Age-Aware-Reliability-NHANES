"""Scan every reachable commit tree and commit metadata with bounded public-safety rules."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from check_public_content import RULES

FORBIDDEN_EXTENSIONS={'.pdf','.docx','.doc','.xlsx','.xls','.xpt','.sas7bdat','.mat','.zip','.7z','.gz','.pkl','.pickle','.joblib'}
PRIVATE_PATH=re.compile(r'(^|/)(?:\.local|\.env(?:\.[^/]*)?|raw|node_modules|__pycache__)(?:/|$)',re.I)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--output',type=Path);a=p.parse_args()
    def git(*args):return subprocess.check_output(['git','-C',str(a.repo),*args],stderr=subprocess.DEVNULL)
    commits=git('rev-list','--all').decode().splitlines();findings=[];seen=set();paths=set()
    for commit in commits:
        try:allowed=set(json.loads(git('show',commit+':verification/public_allowlist.json')))
        except (subprocess.CalledProcessError,ValueError):allowed=None
        for entry in git('ls-tree','-r','-z',commit).split(b'\0'):
            if not entry:continue
            meta,rawpath=entry.split(b'\t',1);mode,kind,oid=meta.decode().split();path=rawpath.decode('utf-8');paths.add(path)
            key=(path,oid)
            if key in seen:continue
            seen.add(key)
            def flag(rule):findings.append(dict(commit=commit,path=path,blob_sha=oid,rule=rule))
            if mode!='100644' or kind!='blob':flag('unexpected_git_object_type');continue
            if PRIVATE_PATH.search(path) or Path(path).suffix.lower() in FORBIDDEN_EXTENSIONS:flag('private_or_unreviewed_file_type')
            if allowed is not None and path not in allowed:flag('not_in_commit_allowlist')
            body=git('cat-file','blob',oid)
            try:text=body.decode('utf-8')
            except UnicodeError:flag('non_text_blob');continue
            for name,rule in RULES.items():
                if rule.search(text):flag(name)
            if path.lower().endswith('.csv') and re.search(r'(?im)^\s*(?:SEQN|GlobalRow)(?:,|$)',text):flag('participant_level_csv')
        # Platform noreply identities are allowed; personal commit contacts are reported without disclosure.
        raw=git('show','-s','--format=%an%x00%ae%x00%cn%x00%ce%x00%B',commit).decode('utf-8')
        fields=raw.split('\0',4)
        for i,label in [(1,'author'),(3,'committer')]:
            email=fields[i];domain=email.rsplit('@',1)[-1].lower()
            if email and domain not in {'users.noreply.github.com','noreply.github.com','github.com'}:
                findings.append(dict(commit=commit,path='commit metadata',rule='personal_'+label+'_contact',value_sha256=hashlib.sha256(email.encode()).hexdigest()))
        for name,rule in RULES.items():
            if rule.search(fields[4]):findings.append(dict(commit=commit,path='commit message',rule=name))
    report=dict(status='PASS' if commits and not findings else 'FAIL',scope='All commits reachable from fetched local/remote refs and tags; all unique path/blob pairs, plus commit messages and contacts. This bounded lexical/type/allowlist review is not a proof that arbitrary secrets cannot exist.',head=git('rev-parse','HEAD').decode().strip(),commits_scanned=len(commits),commit_shas=commits,unique_path_blob_pairs_scanned=len(seen),unique_paths=len(paths),findings=findings)
    if a.output:a.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(report,indent=2));return 0 if report['status']=='PASS' else 1

if __name__=='__main__':sys.exit(main())
