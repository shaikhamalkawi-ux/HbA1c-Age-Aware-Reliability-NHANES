"""Read-only arithmetic QA against locked evidence. Never trains or retunes a model.

Private evidence is materialized by prepare_evidence.py. Missing inputs produce
HOLD; a numerical disagreement outside the declared tolerance stops later checks.
"""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import sys
import numpy as np
import pandas as pd
from scipy.io import loadmat
from fis_arithmetic import parse_fis, predict_fis

ROOT=Path(__file__).resolve().parents[1]
GROUPS=['Age 20-39','Age 40-64','Age 65+']
TOL=1e-12
ROUND_TOL=5e-7
JUST='Floating-point arithmetic and CSV parsing; absolute tolerance 1e-12, no relative tolerance.'
ROUND_JUST='Locked manuscript values are rounded to six decimals: half of one last-place unit.'
DESCRIPTIONS={
 'reconstructed_cohort':'Historical reconstruction and exact-match counts',
 'corrected_cohort':'Corrected primary fasting cohort', 'age_group_counts':'Fixed source age strata',
 'point_model_rmse':'Stored repeated-OOF point prediction RMSE',
 'paired_contrasts':'Paired participant RMSE contrasts', 'bootstrap_ci':'Original participant bootstrap confidence intervals',
 'global_q':'Global calibration-only conformal quantiles', 'mondrian_q':'Age-Mondrian calibration-only quantiles',
 'age_coverage':'Age-specific coverage of stored primary intervals', 'interval_metrics':'Stored primary interval widths and scores',
 'temporal_counts':'Frozen temporal eligibility and counts', 'temporal_metrics':'Stored frozen temporal prediction and calibration arithmetic',
 'tg_bridge':'Prespecified triglyceride backward bridge', 'original_cqr':'Recovered original secondary CQR stored-output arithmetic',
 'frozen_hashes':'Frozen objects and original certificate hashes', 'anfis_parameters':'Historical fixed FIS parameter and prediction checks'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scalar(x):return x.item() if isinstance(x,np.generic) else x
class Discrepancy(Exception):pass
class MissingEvidence(Exception):pass

class Audit:
    def __init__(self,evidence):
        self.root=evidence
        self.manifest=json.loads((ROOT/'verification/evidence_inputs.json').read_text())
        self.expected={r['path']:r for r in self.manifest['inputs']}
        data=json.loads((ROOT/'verification/data_provenance.json').read_text())
        self.expected.update({'nhanes/'+r['filename']:r for r in data['files']})
        self.checks=[];self.cache={};self.current=None
    def note_input(self,path,expected_hash=None):
        if not any(r['path']==path for r in self.current['inputs']):
            p=self.root/path; got=sha(p) if p.is_file() else None
            self.current['inputs'].append(dict(path=path,sha256=got,expected_sha256=expected_hash,exists=p.is_file()))
            if not p.is_file():raise MissingEvidence('Missing input: '+path)
            if expected_hash and got!=expected_hash:raise Discrepancy('Input hash mismatch: '+path)
        return self.root/path
    def path(self,name):return self.note_input(name,self.expected[name]['sha256'])
    def csv(self,name):
        p=self.path(name)
        if name not in self.cache:self.cache[name]=pd.read_csv(p)
        return self.cache[name].copy()
    def obj(self,name):return json.loads(self.path(name).read_text())
    def compare(self,label,expected,observed,tol=TOL,just=JUST):
        expected,observed=scalar(expected),scalar(observed)
        if isinstance(expected,(str,bool)) or expected is None:
            diff=0 if expected==observed else 1;tol=0;just='Exact identity or logical equality.'
        else:diff=float(abs(observed-expected))
        good=math.isfinite(diff) and diff<=tol
        self.current['measurements'].append(dict(name=label,expected=expected,observed=observed,absolute_difference=diff,tolerance=tol,tolerance_justification=just,status='PASS' if good else 'FAIL'))
        if not good:raise Discrepancy(label)
    def exact(self,label,expected,observed):self.compare(label,expected,observed,0,'Counts, memberships or discrete identities require exact equality.')
    def zero_array(self,label,x,tol=TOL):self.compare(label,0,float(np.max(np.abs(np.asarray(x)))) if np.size(x) else 0,tol)
    def hold(self,reason):self.current['limitations'].append(reason);self.current['status']='HOLD'
    def run(self,name,fn,stopped=False):
        self.current=dict(id=name,description=DESCRIPTIONS[name],status='HOLD',executed=False,
          command='python scripts/verify_science.py --evidence-root <private-evidence> --output <report.json>',
          script_sha256=sha(ROOT/'scripts/verify_science.py'),inputs=[],measurements=[],limitations=[])
        self.current['reference_inputs']=[dict(path='verification/locked_reference.json',sha256=sha(ROOT/'verification/locked_reference.json')),dict(path='verification/evidence_inputs.json',sha256=sha(ROOT/'verification/evidence_inputs.json')),dict(path='verification/data_provenance.json',sha256=sha(ROOT/'verification/data_provenance.json'))]
        if stopped:self.current['limitations']=['Not executed: a preceding scientific discrepancy triggered the stop rule.']
        else:
            try:
                self.current.update(executed=True,status='PASS');fn()
            except MissingEvidence as e:self.hold(str(e))
            except Discrepancy as e:self.current.update(status='FAIL');self.current['limitations'].append('STOP: '+str(e));stopped=True
        self.checks.append(self.current);print(name,self.current['status'],len(self.current['measurements']),flush=True)
        return stopped
    def nhanes(self,suffix):
        use={'DEMO':['SEQN','RIDAGEYR','SDMVSTRA','SDMVPSU','WTMEC2YR'],'BMX':['SEQN','BMXBMI'],'GLU':['SEQN','LBXGLU','WTSAF2YR'],'TRIGLY':['SEQN','LBXTLG' if suffix=='L' else 'LBXTR','LBDLDL'],'GHB':['SEQN','LBXGH'],'FASTQX':['SEQN','PHAFSTHR','PHAFSTMN']}
        frames=[]
        for component,cols in use.items():
            name=f'nhanes/{component}_{suffix}.xpt';p=self.path(name)
            if name not in self.cache:self.cache[name]=pd.read_sas(p,format='xport')
            d=self.cache[name][cols].copy();self.exact(f'{component}_{suffix}: duplicate identifiers',0,int(d.SEQN.duplicated().sum()));frames.append(d)
        d=frames[0]
        # Preserve the complete laboratory intersection, using fasting questionnaire as metadata.
        for f in frames[1:-1]:d=d.merge(f,on='SEQN',how='inner',validate='one_to_one')
        d=d.merge(frames[-1],on='SEQN',how='left',validate='one_to_one')
        d=d.rename(columns={'RIDAGEYR':'Age','BMXBMI':'BMI','LBXGLU':'FastingGlucose','LBXTR':'Triglycerides','LBXTLG':'Triglycerides','LBXGH':'HbA1c','LBDLDL':'LDL'})
        d['FastingMinutes']=60*d.PHAFSTHR+d.PHAFSTMN
        d['AgeGroup']=pd.cut(d.Age,[19,39,64,np.inf],labels=GROUPS).astype(str)
        return d
    def cohort_match(self,label,left,right,cols):
        self.exact(label+': identifier symmetric difference',0,len(set(left.SEQN)^set(right.SEQN)))
        left=left.sort_values('SEQN').reset_index(drop=True);right=right.sort_values('SEQN').reset_index(drop=True)
        for c in cols:
            self.exact(label+': '+c+' missingness mismatch',0,int((left[c].isna()!=right[c].isna()).sum()))
            valid=left[c].notna();gap=float(np.max(abs(left.loc[valid,c].to_numpy()-right.loc[valid,c].to_numpy())))
            if c=='WTSAF2YR':self.compare(label+': '+c+' max difference',0,gap,1e-8,'Survey weights reach hundreds of thousands; 1e-8 bounds decimal CSV serialization of approximately 15 significant digits.')
            else:self.compare(label+': '+c+' max difference',0,gap)

def point_metrics(d,pred='Predicted',obs='Observed'):
    y=d[obs].to_numpy();p=d[pred].to_numpy();w=d.WTSAF2YR.to_numpy();e=p-y
    wm=lambda x:np.average(x,weights=w)
    return dict(RMSE=np.sqrt(np.mean(e*e)),MAE=np.mean(abs(e)),Bias=np.mean(e),R2=1-np.sum(e*e)/np.sum((y-y.mean())**2),WeightedRMSE=np.sqrt(wm(e*e)),WeightedMAE=wm(abs(e)),WeightedBias=wm(e))
def interval_metrics(d,nom):
    y=d.Observed.to_numpy();l=d.Lower.to_numpy();u=d.Upper.to_numpy();w=d.WTSAF2YR.to_numpy();alpha=1-nom
    cov=(y>=l)&(y<=u);width=u-l;score=width+2/alpha*np.maximum(l-y,0)+2/alpha*np.maximum(y-u,0)
    return dict(Coverage=cov.mean(),WeightedCoverage=np.average(cov,weights=w),MeanWidth=width.mean(),MedianWidth=np.median(width),WeightedMeanWidth=np.average(width,weights=w),IntervalScore=score.mean(),WeightedIntervalScore=np.average(score,weights=w),LowerMiss=(y<l).mean(),UpperMiss=(y>u).mean())
def qvalue(v,alpha):
    k=math.ceil((len(v)+1)*(1-alpha));return float(np.sort(v)[k-1]) if k<=len(v) else float('inf')
def subset(d,g):return d if g=='Overall' else d[d.AgeGroup==g]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--evidence-root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    a=Audit(args.evidence_root);locked=json.loads((ROOT/'verification/locked_reference.json').read_text())
    def point():
        d=a.csv('oof.csv');ref=a.csv('point_metrics.csv');a.path('original_primary.py')
        names=['Pooled_OLS','HardAge_OLS','GlucoseOnly_OLS','SmoothVC_OLS','Pooled_LightGBM','HardAge_LightGBM']
        a.exact('Number of point models',6,d.model.nunique())
        for m in names:
            s=d[d.model==m];a.exact(m+': participants',2219,s.SEQN.nunique());a.exact(m+': repeated OOF rows',11095,len(s))
            a.exact(m+': duplicate participant/repeat',0,int(s.duplicated(['SEQN','repeat']).sum()))
            a.exact(m+': each participant has five repeats',True,bool(s.groupby('SEQN')['repeat'].nunique().eq(5).all()))
            for g in ['Overall']+GROUPS:
                r=ref[(ref.model==m)&(ref.group==g)].iloc[0];computed=point_metrics(subset(s,g))
                a.compare(f'{m}/{g}/RMSE',r.RMSE,computed['RMSE'])
            a.compare(m+': manuscript RMSE',locked['repeated_oof']['rmse'][dict(Pooled_OLS='pooled_ols',HardAge_OLS='hard_age_ols',GlucoseOnly_OLS='glucose_only_ols',SmoothVC_OLS='smoothvc_ols',Pooled_LightGBM='pooled_lightgbm',HardAge_LightGBM='hard_age_lightgbm')[m]],point_metrics(s)['RMSE'],ROUND_TOL,ROUND_JUST)
    def contrasts(bootstrap=False):
        pred=a.csv('oof.csv');ref=a.csv('bootstrap.csv');a.path('original_postprocess.py')
        models=sorted(pred.model.unique());base=pred[['SEQN','AgeGroup','repeat','fold','Observed']].drop_duplicates()
        for m in models:base=base.merge(pred[pred.model==m][['SEQN','repeat','fold','Predicted']].rename(columns={'Predicted':m}),on=['SEQN','repeat','fold'],validate='one_to_one')
        persons=base[['SEQN','AgeGroup']].drop_duplicates().sort_values('SEQN').reset_index(drop=True)
        for m in models:persons['SSE_'+m]=persons.SEQN.map(base.assign(sq=(base[m]-base.Observed)**2).groupby('SEQN',sort=False).sq.sum())
        persons['nrep']=persons.SEQN.map(base.groupby('SEQN').size());a.exact('Five stored appearances per participant',True,bool(persons.nrep.eq(5).all()))
        pairs=[('HardAge_OLS','Pooled_OLS'),('HardAge_LightGBM','Pooled_LightGBM'),('SmoothVC_OLS','Pooled_OLS'),('Pooled_LightGBM','Pooled_OLS'),('Pooled_OLS','GlucoseOnly_OLS')]
        rng=np.random.default_rng(20260912)
        for g in ['Overall']+GROUPS:
            pools=[np.where(persons.AgeGroup.to_numpy()==z)[0] for z in (GROUPS if g=='Overall' else [g])];scope=np.concatenate(pools);nr=persons.nrep.to_numpy(float)
            for aa,bb in pairs:
                ssa=persons['SSE_'+aa].to_numpy(float);ssb=persons['SSE_'+bb].to_numpy(float)
                target=ref[(ref.group==g)&(ref.model_A==aa)&(ref.model_B==bb)].iloc[0];label=f'{g}/{aa}-{bb}'
                delta=math.sqrt(ssa[scope].sum()/nr[scope].sum())-math.sqrt(ssb[scope].sum()/nr[scope].sum())
                if not bootstrap:
                    a.compare(label,target.DeltaRMSE_A_minus_B,delta)
                    if g=='Overall' and aa=='HardAge_OLS':a.compare('Manuscript hard-age minus pooled',.004169,delta,ROUND_TOL,ROUND_JUST)
                    continue
                diffs=np.empty(10000)
                for pos in range(0,10000,250):
                    sum_a=np.zeros(250);sum_b=np.zeros(250);sum_n=np.zeros(250)
                    for pool in pools:
                        draw=rng.choice(pool,size=(250,len(pool)),replace=True)
                        sum_a+=ssa[draw].sum(axis=1);sum_b+=ssb[draw].sum(axis=1);sum_n+=nr[draw].sum(axis=1)
                    diffs[pos:pos+250]=np.sqrt(sum_a/sum_n)-np.sqrt(sum_b/sum_n)
                for q,col in [(.025,'CI2.5'),(.975,'CI97.5')]:a.compare(label+'/'+col,target[col],np.quantile(diffs,q))
                a.exact(label+'/bootstrap replicates',int(target.BootstrapN),10000)
                if g=='Overall' and aa=='HardAge_OLS':
                    a.compare('Manuscript CI lower',-.002639,np.quantile(diffs,.025),ROUND_TOL,ROUND_JUST);a.compare('Manuscript CI upper',.012260,np.quantile(diffs,.975),ROUND_TOL,ROUND_JUST)
    def quantiles(calibration):
        d=a.csv('cohort.csv');roles=a.csv('freeze_roles.csv');f=a.obj('frozen.json');a.path('original_freeze.py')
        a.exact('Frozen role counts: TRAIN',1775,int(roles.Role.eq('TRAIN').sum()));a.exact('Frozen role counts: CALIBRATION',444,int(roles.Role.eq('CALIBRATION').sum()));a.exact('Frozen unique role assignments',0,int(roles.SEQN.duplicated().sum()))
        d=d.merge(roles,on='SEQN',validate='one_to_one');d=d[d.Role=='CALIBRATION'].copy()
        x=d[f['predictor_order']].to_numpy();p=f['linear_intercept']+((x-np.array(f['scaler_mean']))/np.array(f['scaler_scale'])).dot(np.array(f['linear_coef_standardized']))
        d['residual']=np.abs(d.HbA1c.to_numpy()-p)
        for group in (['global'] if calibration=='global' else GROUPS):
            s=d if group=='global' else d[d.AgeGroup==group]
            for alpha in [.1,.05]:a.compare(f'frozen/{group}/alpha={alpha}',f['conformal_quantiles_abs_residual'][group][str(alpha)],qvalue(s.residual.to_numpy(),alpha))
        cal=a.csv('calibration.csv');intervals=a.csv('intervals.csv');oof=a.csv('oof.csv');ledger=a.csv('split_ledger.csv');a.path('original_primary.py')
        max_gap=0.;comparisons=0
        for (model,repeat,fold),s in cal.groupby(['model','repeat','fold']):
            if model not in intervals.model.unique():continue
            test=oof[(oof.model==model)&(oof['repeat']==repeat)&(oof.fold==fold)]
            a.exact(f'{model}/r{repeat}/f{fold}: calibration/test overlap',0,len(set(s.SEQN)&set(test.SEQN)))
            led=ledger[(ledger['repeat']==repeat)&(ledger.fold==fold)].iloc[0]
            a.exact(f'{model}/r{repeat}/f{fold}: calibration count',int(led.n_cal),len(s))
            ints=intervals[(intervals.model==model)&(intervals['repeat']==repeat)&(intervals.fold==fold)&(intervals.Calibration==calibration)]
            for nom in [.9,.95]:
                for group in (['global'] if calibration=='global' else GROUPS):
                    r=s if group=='global' else s[s.AgeGroup==group]
                    q=qvalue(np.abs(r.Observed-r.Predicted).to_numpy(),1-nom)
                    target=ints[ints.Nominal==nom]
                    if group!='global':target=target[target.AgeGroup==group]
                    gap=float(np.max(abs(target.Q.to_numpy()-q)));max_gap=max(max_gap,gap);comparisons+=1
        a.compare('Maximum stored internal Q difference',0,max_gap);a.exact('Internal calibration quantiles checked',200 if calibration=='global' else 600,comparisons)
    def interval_check(coverage):
        d=a.csv('intervals.csv');ref=a.csv('interval_metrics.csv');a.path('original_primary.py')
        for (m,cal,nom),s in d.groupby(['model','Calibration','Nominal']):
            a.zero_array(f'{m}/{cal}/{nom}: lower construction',s.Lower-(s.Predicted-s.Q));a.zero_array(f'{m}/{cal}/{nom}: upper construction',s.Upper-(s.Predicted+s.Q))
            for g in ['Overall']+GROUPS:
                r=ref[(ref.model==m)&(ref.Calibration==cal)&(ref.Nominal==nom)&(ref.group==g)].iloc[0];metrics=interval_metrics(subset(s,g),nom)
                keys=['Coverage','WeightedCoverage','LowerMiss','UpperMiss'] if coverage else ['MeanWidth','MedianWidth','WeightedMeanWidth','IntervalScore','WeightedIntervalScore']
                for k in keys:a.compare(f'{m}/{cal}/{nom}/{g}/{k}',r[k],metrics[k])
                if coverage and m=='Pooled_OLS' and nom==.9 and g!='Overall':a.compare(f'Manuscript 90% {cal}/{g}',locked['primary_coverage']['global_residual_by_age' if cal=='global' else 'age_mondrian_by_age'][GROUPS.index(g)],metrics['Coverage'],ROUND_TOL,ROUND_JUST)
    def original_cqr():
        for layer,pp,mp,code in [('internal','cqr_internal.csv','cqr_internal_metrics.csv','original_cqr_internal.py'),('forward','cqr_forward.csv','cqr_forward_metrics.csv','original_cqr_forward.py')]:
            d=a.csv(pp);ref=a.csv(mp);a.path(code)
            for nom,s in d.groupby('Nominal'):
                n=2219 if layer=='internal' else 2808;a.exact(f'{layer}/{nom}/participants',n,s.SEQN.nunique());a.exact(f'{layer}/{nom}/rows',n*(5 if layer=='internal' else 1),len(s))
                a.zero_array(f'{layer}/{nom}/lower correction',s.Lower-(s.BaseLower-s.Qhat));a.zero_array(f'{layer}/{nom}/upper correction',s.Upper-(s.BaseUpper+s.Qhat))
                for g in ['Overall']+GROUPS:
                    r=ref[(ref.Nominal==nom)&(ref.group==g)].iloc[0]
                    for k,v in interval_metrics(subset(s,g),nom).items():
                        if k in ref.columns:a.compare(f'{layer}/{nom}/{g}/{k}',r[k],v)
        f=a.csv('cqr_sourcefreeze.csv');d=a.csv('cqr_forward.csv')
        for r in f.itertuples(index=False):
            a.zero_array(f'forward/{r.Nominal}/source Qhat consistency',d[d.Nominal==r.Nominal].Qhat-r.Qhat)
            a.exact(f'forward/{r.Nominal}/source order statistic',math.ceil((r.n_cal+1)*r.Nominal),int(r.k))
        a.current['limitations'].append('PASS covers recovered original stored-output arithmetic and source-freeze consistency. Original fitted CQR objects/calibration quantile predictions are absent; no fit or fresh CQR quantile reconstruction is claimed. Later exploratory CQR objects were not substituted.')
    def reconstructed():
        d=a.nhanes('J');r=a.csv('reconstruction.csv');a.csv('matching_certificate.csv');cols=['Age','BMI','FastingGlucose','Triglycerides','HbA1c','LDL']
        full=d.dropna(subset=cols);a.exact('Official complete six-variable rows',2757,len(full));a.exact('Official duplicate six-variable fingerprints',0,int(full.duplicated(cols).sum()))
        joined=r.merge(full[['SEQN']+cols],on=cols,how='left',suffixes=('_stored','_official'))
        a.exact('Reconstructed rows',2325,len(r));a.exact('Reconstructed unique identifiers',2325,r.SEQN.nunique());a.exact('Exact six-field candidate matches',2325,int(joined.SEQN_official.notna().sum()));a.exact('Unmatched reconstructed rows',0,int(joined.SEQN_official.isna().sum()));a.exact('Ambiguous reconstructed rows',0,len(joined)-len(r));a.exact('Fingerprint/identifier disagreements',0,int((joined.SEQN_stored!=joined.SEQN_official).sum()))
        historical=d[(d.Age>=20)&(d.Age<=80)].dropna(subset=cols[:-1]);a.exact('Historical complete core before LDL',2350,len(historical));missing=historical[historical.LDL.isna()];a.exact('Missing Friedewald LDL',25,len(missing));a.exact('All 25 TG at or above 400',True,bool((missing.Triglycerides>=400).all()))
        stored_missing=a.csv('missing_ldl.csv');a.exact('Missing-LDL identifier agreement',0,len(set(missing.SEQN)^set(stored_missing.SEQN)))
        a.cohort_match('Historical retained rows',r,historical.dropna(subset=['LDL']),cols+['WTSAF2YR','FastingMinutes'])
        valid=(r.WTSAF2YR>0)&(r.FastingMinutes>=480)&(r.FastingMinutes<1440);a.exact('Legacy invalid fasting or weight',131,int((~valid).sum()))
        # Independently link every original numeric MAT row on its five retained fields.
        mats=[]
        for g in ['20_39','40_64','65_80']:
            mat=loadmat(a.path(f'legacy/{g}/ANFIS_Complete_Output.mat'),variable_names=['A'],simplify_cells=True);mats.append(mat['A'])
        old=pd.DataFrame(np.vstack(mats),columns=cols[:-1]);joined5=old.merge(r[cols[:-1]],on=cols[:-1],how='left',indicator=True)
        a.exact('Original numeric MAT rows',2325,len(old));a.exact('Original five-field row matches',2325,int(joined5['_merge'].eq('both').sum()));a.exact('Original five-field ambiguous candidates',0,len(joined5)-len(old))
        a.hold('The locked package contains the six-field reconstructed table and matching certificate, plus original five-column MAT arrays. The pre-reconstruction six-column legacy table and original matching implementation are absent. Current six-field CDC matching passes, but the original LDL column cannot be independently re-established from the five-column MAT arrays.')
    def corrected(age_only=False):
        source=a.csv('cohort.csv')
        if age_only:
            computed=pd.cut(source.Age,[19,39,64,np.inf],labels=GROUPS).astype(str)
            a.exact('Age-label disagreements',0,int((computed!=source.AgeGroup).sum()))
            for g,n in zip(GROUPS,[666,991,562]):a.exact(g,n,int(computed.eq(g).sum()))
            return
        d=a.nhanes('J');d=d[(d.Age>=20)&(d.WTSAF2YR>0)&(d.FastingMinutes>=480)&(d.FastingMinutes<1440)].dropna(subset=['Age','BMI','FastingGlucose','Triglycerides','HbA1c'])
        a.exact('Official reconstructed corrected cohort',2219,len(d));a.exact('Stored cohort rows',2219,len(source));a.cohort_match('Corrected source',source,d,['Age','BMI','FastingGlucose','Triglycerides','HbA1c','LDL','WTSAF2YR','FastingMinutes'])
    def temporal_counts():
        a.path('original_freeze.py')
        for suffix,file,n,counts in [('I','backward.csv',2235,[712,970,553]),('L','forward.csv',2808,[670,1203,935])]:
            d=a.nhanes(suffix);d=d[(d.Age>=20)&(d.WTSAF2YR>0)].dropna(subset=['Age','BMI','FastingGlucose','Triglycerides','HbA1c']);stored=a.csv(file)
            a.exact(suffix+': official eligible count',n,len(d));a.exact(suffix+': stored count',n,len(stored));cols=['Age','BMI','FastingGlucose','HbA1c','WTSAF2YR']
            if suffix=='L':d=d.rename(columns={'Triglycerides':'TriglyceridesRaw'});cols+=['TriglyceridesRaw']
            else:cols+=['Triglycerides']
            a.cohort_match(suffix+': temporal cohort',stored,d,cols)
            for g,cnt in zip(GROUPS,counts):a.exact(suffix+'/'+g,cnt,int(d.AgeGroup.eq(g).sum()))
    def temporal_metrics():
        f=a.obj('frozen.json');prec=a.csv('temporal_reference.csv');a.path('original_fixed_verifier.py')
        for cycle,file,pm,im,tg in [('2015-2016','backward.csv','backward_point_metrics.csv','backward_interval_metrics.csv','Triglycerides'),('2021-2023','forward.csv','forward_point_metrics.csv','forward_interval_metrics.csv','TriglyceridesBridged')]:
            d=a.csv(file);r=a.csv(pm);ir=a.csv(im);x=d[['Age','BMI','FastingGlucose',tg]].to_numpy()
            predicted=f['linear_intercept']+((x-np.array(f['scaler_mean']))/np.array(f['scaler_scale'])).dot(np.array(f['linear_coef_standardized']))
            a.zero_array(cycle+': frozen prediction max difference',predicted-d.Prediction.to_numpy())
            for g in ['Overall']+GROUPS:
                s=subset(d,g);y=s.HbA1c.to_numpy();p=s.Prediction.to_numpy();w=s.WTSAF2YR.to_numpy();values=point_metrics(s,'Prediction','HbA1c')
                slope=np.sum((p-p.mean())*(y-y.mean()))/np.sum((p-p.mean())**2);intercept=y.mean()-slope*p.mean();wy=np.average(y,weights=w);wp=np.average(p,weights=w);ws=np.sum(w*(p-wp)*(y-wy))/np.sum(w*(p-wp)**2)
                values.update(WeightedR2=1-np.sum(w*(y-p)**2)/np.sum(w*(y-wy)**2),CalibrationInLarge=np.mean(y-p),CalibrationInterceptSlope1=np.mean(y-p),CalibrationIntercept=intercept,CalibrationSlope=slope,WeightedCalibrationInLarge=np.average(y-p,weights=w),WeightedCalibrationInterceptSlope1=np.average(y-p,weights=w),WeightedCalibrationIntercept=wy-ws*wp,WeightedCalibrationSlope=ws)
                target=r[r.Group==g].iloc[0]
                for k,v in values.items():
                    if k in r.columns:a.compare(cycle+'/'+g+'/'+k,target[k],v)
                if g=='Overall':
                    target=prec[prec.Cycle==cycle].iloc[0]
                    for k,v in [('CalibrationSlope',slope),('CalibrationIntercept',intercept),('CITL',np.mean(y-p)),('R2_PredictionError',values['R2']),('RMSE',values['RMSE']),('MAE',values['MAE'])]:a.compare(cycle+'/locked precision/'+k,target[k],v)
                    a.compare(cycle+'/manuscript RMSE',locked['temporal'][cycle]['rmse'],values['RMSE'],ROUND_TOL,ROUND_JUST);a.compare(cycle+'/manuscript slope',locked['temporal'][cycle]['calibration_slope'],slope,ROUND_TOL,ROUND_JUST)
            for cal in ['global','mondrian']:
                for alpha in [.1,.05]:
                    nom=1-alpha;q=d.AgeGroup.map({g:f['conformal_quantiles_abs_residual']['global' if cal=='global' else g][str(alpha)] for g in GROUPS}).to_numpy()
                    ints=d.rename(columns={'HbA1c':'Observed'}).assign(Lower=d.Prediction-q,Upper=d.Prediction+q)
                    for g in ['Overall']+GROUPS:
                        target=ir[(ir.Calibration==cal)&(ir.Nominal==nom)&(ir.Group==g)].iloc[0]
                        for k,v in interval_metrics(subset(ints,g),nom).items():
                            if k in ir.columns:a.compare(f'{cycle}/{cal}/{nom}/{g}/{k}',target[k],v)
    def bridge():
        d=a.csv('forward.csv');f=a.obj('frozen.json');a.path('original_freeze.py');official=a.nhanes('L')
        a.cohort_match('L original measured triglyceride',d.rename(columns={'TriglyceridesRaw':'Triglycerides'}),official[official.SEQN.isin(d.SEQN)],['Triglycerides'])
        a.zero_array('TG old-scale = -12.19 + 0.9785 * measured new scale',d.TriglyceridesBridged-(-12.19+.9785*d.TriglyceridesRaw))
        a.exact('Frozen transform retains backward equation',True,'-12.19 + 0.9785 * LBXTLG_new' in f['target_cycle_transform']['Triglycerides'])
    def hashes():
        f=a.obj('frozen.json');cert=a.obj('frozen_certificate.json');a.path('freeze_roles.csv')
        for field in cert:
            if 'sha256' in field.lower():
                if 'freeze' in field.lower() and 'ledger' not in field.lower():a.compare(field,cert[field],sha(a.path('frozen.json')))
                elif 'ledger' in field.lower():a.compare(field,cert[field],sha(a.path('freeze_roles.csv')))
        # Compare each certificate coefficient to the original immutable source freeze.
        for k in ['source_cohort_n','training_n','calibration_n']:
            if k in cert:a.exact(k,cert[k],f[k])
        a.exact('Frozen target retraining disabled',True,f['no_target_retraining']);a.exact('Frozen target recalibration disabled',True,f['no_target_recalibration_primary'])
        ref=a.csv('legacy_certificate.csv')
        for g in ['20_39','40_64','65_80']:
            row=ref[ref.LegacyGroup==g].iloc[0]
            for key,name in [('FIS_SHA256','Trained_FIS.fis'),('MAT_SHA256','ANFIS_Complete_Output.mat')]:a.compare(g+'/'+key,row[key],sha(a.path(f'legacy/{g}/{name}')))
        a.current['limitations'].append('Covers the original frozen OLS/conformal object, role ledger and three historical FIS/MAT pairs. No original fitted CQR object was found or substituted.')
    def anfis():
        a.path('original_fixed_verifier.py');a.current['reference_inputs'].append(dict(path='scripts/fis_arithmetic.py',sha256=sha(ROOT/'scripts/fis_arithmetic.py')))
        totalrules=0;totalpars=0;rows=0;maxgap=0
        for g,expectedrules in zip(['20_39','40_64','65_80'],[5,23,13]):
            f=parse_fis(a.path(f'legacy/{g}/Trained_FIS.fis'));m=loadmat(a.path(f'legacy/{g}/ANFIS_Complete_Output.mat'),variable_names=['x','y','yhat','trndata','chkdata'],simplify_cells=True)
            original=np.hstack([a.csv(f'legacy/{g}/{k}.csv').iloc[:,1:].to_numpy(float) for k in ['Premise_Age_BMI','Premise_Glucose_TG','Consequent']]);params=np.hstack([f['params'][0],f['params'][1],f['params'][2],f['params'][3],f['coeff']])
            a.exact(g+': rules',expectedrules,f['n']);a.exact(g+': mismatched parameters at six decimals',0,int((np.round(params,6)!=np.round(original,6)).sum()))
            a.compare(g+': maximum unrounded-to-printed parameter difference',0,float(np.max(abs(params-original))),ROUND_TOL,ROUND_JUST)
            p,_=predict_fis(f,m['x']);gap=float(np.max(abs(p-m['yhat'])));maxgap=max(maxgap,gap)
            a.compare(g+': fixed FIS versus MATLAB max difference',0,gap,1e-10,'Original fixed-FIS verifier uses absolute 1e-10 for different floating-point evaluation orders; no training.')
            train=set(map(tuple,m['trndata'].tolist()));a.exact(g+': checking rows contained in training',len(m['chkdata']),sum(tuple(r) in train for r in m['chkdata'].tolist()))
            totalrules+=f['n'];totalpars+=params.size;rows+=len(p)
        a.exact('Total historical rules',41,totalrules);a.exact('Total parameters checked',533,totalpars);a.exact('Total historical rows evaluated',2325,rows)
        a.current['limitations'].append('Historical structural reproducibility only. Checking rows overlap training; these are not independent validation or ANFIS superiority results.')
    jobs=[('point_model_rmse',point),('paired_contrasts',lambda:contrasts(False)),('bootstrap_ci',lambda:contrasts(True)),('global_q',lambda:quantiles('global')),('mondrian_q',lambda:quantiles('mondrian')),('age_coverage',lambda:interval_check(True)),('interval_metrics',lambda:interval_check(False)),('original_cqr',original_cqr),('temporal_metrics',temporal_metrics),('frozen_hashes',hashes),('anfis_parameters',anfis),('reconstructed_cohort',reconstructed),('corrected_cohort',lambda:corrected(False)),('age_group_counts',lambda:corrected(True)),('temporal_counts',temporal_counts),('tg_bridge',bridge)]
    stopped=False
    for name,fn in jobs:stopped=a.run(name,fn,stopped)
    a.checks.sort(key=lambda x:list(DESCRIPTIONS).index(x['id']))
    counts={s:sum(c['status']==s for c in a.checks) for s in ['PASS','HOLD','FAIL']}
    report=dict(schema_version=2,checkpoint='numerical_scientific_verification',overall_status='FAIL' if counts['FAIL'] else 'HOLD' if counts['HOLD'] else 'PASS',counts=counts,stop_on_discrepancy=True,stopped_on_discrepancy=stopped,training_refit_performed=False,target_recalibration_performed=False,scope='Stored-output arithmetic, fixed-model evaluation, official-data eligibility and provenance. No full learner refit claim.',environment=dict(python=platform.python_version(),platform=platform.system(),packages={p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy']}),checks=a.checks)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print(json.dumps(counts))
    return 1 if counts['FAIL'] else 0

if __name__=='__main__':sys.exit(main())
