"""Fixed Sugeno evaluation; no fitting. Source hash is in evidence_inputs.json."""
from pathlib import Path
import re
import numpy as np
from scipy.special import logsumexp

def parse_fis(path: Path) -> dict:
    text = path.read_text(encoding='utf-8-sig')
    blocks = {name: body for name, body in re.findall(r'\[([^\]]+)\]\s*\n(.*?)(?=\n\[|\Z)', text, flags=re.S)}
    system=blocks['System']
    for specification in ["Type='sugeno'", 'NumInputs=4', 'NumOutputs=1', "AndMethod='prod'", "DefuzzMethod='wtaver'"]:
        if specification not in system:
            raise ValueError(f'Unsupported FIS specification {path}: {specification}')
    n=int(re.search(r'NumRules=(\d+)',system).group(1))
    params=[]; ranges=[]
    for i in range(1,5):
        b=blocks[f'Input{i}']
        vals=re.findall(r"MF\d+='[^']+':'gaussmf',\[([^\]]+)\]",b)
        p=np.array([[float(v) for v in line.split()] for line in vals])
        if p.shape!=(n,2) or not np.isfinite(p).all() or np.any(p[:,0]<=0):
            raise ValueError(f'Invalid Gaussian parameters: {path}, Input{i}')
        params.append(p)
        ranges.append([float(v) for v in re.search(r'Range=\[([^\]]+)\]',b).group(1).split()])
    vals=re.findall(r"MF\d+='[^']+':'linear',\[([^\]]+)\]",blocks['Output1'])
    coeff=np.array([[float(v) for v in line.split()] for line in vals])
    if coeff.shape!=(n,5): raise ValueError('Unexpected consequent shape')
    rules=[l.strip() for l in blocks['Rules'].splitlines() if l.strip()]
    if len(rules)!=n: raise ValueError('Rule count mismatch')
    for k,line in enumerate(rules,1):
        z=re.fullmatch(r'(\d+) (\d+) (\d+) (\d+), (\d+) \(1\) : 1',line)
        if not z or list(map(int,z.groups()))!=[k]*5:
            raise ValueError('Only verified identity-linked, unit-weight AND rules supported')
    return {'n':n,'params':np.array(params),'ranges':np.array(ranges),'coeff':coeff}

def predict_fis(fis:dict, x:np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    x=np.asarray(x,dtype=float)
    if x.ndim!=2 or x.shape[1]!=4 or not np.isfinite(x).all():raise ValueError('Expected finite n by 4 inputs')
    sig=fis['params'][:,:,0].T
    cen=fis['params'][:,:,1].T
    logw=-0.5*np.sum(((x[:,None,:]-cen[None,:,:])/sig[None,:,:])**2,axis=2)
    normlog=logsumexp(logw,axis=1)
    weights=np.exp(logw-normlog[:,None])
    local=x@fis['coeff'][:,:4].T+fis['coeff'][:,4]
    return np.sum(weights*local,axis=1),normlog
