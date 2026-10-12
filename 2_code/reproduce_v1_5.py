#!/usr/bin/env python3
"""Rebuild seven author-review figure assemblies from frozen aggregate inputs only.

No Cox/logistic fit, participant input, bootstrap rerun or manuscript edit is performed.
Default output is generated_v1_5/ (ignored by Git); published assets are not overwritten.
Arial is used when available. Font/library differences can change pixel hashes.
"""
from pathlib import Path
import argparse, csv, json, hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=ROOT/'generated_v1_5')
parser.add_argument('--png-only',action='store_true',help='Reproduce PNGs without authoring new PDF/SVG outputs')
args=parser.parse_args()
OUTPUT=args.output.resolve()
if OUTPUT==ROOT or OUTPUT.is_relative_to(ROOT/'4_figures'):
    raise SystemExit('Choose a generated output directory, not the repository root or published figures')
OUTPUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
contract=json.loads((ROOT/'0_admin/audit/source_hash_contract_v1.5.json').read_text(encoding='utf-8'))
for name,rec in contract.items():
    if sha(ROOT/rec['relative_path'])!=rec['raw_sha256']:
        raise SystemExit('Frozen source bytes changed: '+name)
data=ROOT/'1_data/aggregate/frozen_v1.5'
obj,ab,av,cross,prim=[read(data/n) for n in ['objects22.tsv','absolute23.tsv','avaglio10.tsv','cross13.tsv','primary27.tsv']]
pairs=[]
for r in range(30,39):
    for s in range(max(16,r-17),min(21,r-14)+1):
        pairs.append({'randomized_n':r,'randomized_pcr':s,'raw_pcr_fraction':s/r})
if len(pairs)!=24:raise SystemExit('TRIO aggregate compatibility enumeration failed')
def display_fields(r):
    cid=r['legacy_claim_id']
    ctx='HER2+ breast' if cid.startswith('HER2') else ('HER2− breast' if cid=='TNBC_03' else ('TNBC' if cid.startswith('TNBC') else cid.split('_')[0]))
    if cid.startswith('HER2'): src='association'; prov='formula'; fid='ungraded'; pop='mixed*'; est='mismatch'; role='qualified'
    elif cid=='TNBC_01': src='trial context'; prov='bridge'; fid='F1 hist.'; pop='trial'; est='dependent'; role='reframed'
    elif cid=='TNBC_03': src='trial context'; prov='score reuse'; fid='F0 hist.'; pop='platform'; est='source only'; role='reframed'
    elif cid=='TNBC_04': src='trial context'; prov='approx.'; fid='F2 hist.'; pop='trial'; est='approx.'; role='reframed'
    elif cid in ['RCC_01','RCC_02','RCC_03']: src='exploratory'; prov='aggregate'; fid='F0 hist.'; pop='aggregate'; est='subgroup only' if cid=='RCC_03' else 'not located'; role='reframed'
    elif cid=='RCC_04': src='unresolved'; prov='open source'; fid='ungraded'; pop='aggregate'; est='audit'; role='not evaluable'
    elif cid=='RCC_05': src='association'; prov='open source'; fid='ungraded'; pop='aggregate'; est='audit'; role='not evaluable'
    elif cid.startswith('GBM'): src='adj. interact.'; prov='label reuse'; fid='F1 hist.'; pop='trial'; est='aligned / medium'; role='reanalysed'
    elif cid=='RT_01': src='pooled model'; prov='aggregate'; fid='F0 hist.'; pop='pooled'; est='OS, not utility'; role='reframed'
    elif cid=='BCI_01': src='trial interact.'; prov='partial'; fid='F3 hist.'; pop='nested'; est='limited'; role='limited'
    else: raise ValueError(cid)
    # Explicit adjudication: separators in machine labels are NOT claim polarity.
    polarity = {'HER2_01':'positive','HER2_02':'negative','HER2_03':'negative',
        'HER2_04':'exploratory','HER2_05':'exploratory','HER2_06':'exploratory','HER2_07':'exploratory',
        'HER2_08':'negative','HER2_09':'negative','HER2_10':'negative',
        'TNBC_01':'mixed','TNBC_03':'positive','TNBC_04':'mixed',
        'RCC_01':'exploratory','RCC_02':'exploratory','RCC_03':'exploratory',
        'RCC_04':'association','RCC_05':'negative','GBM_01':'positive','GBM_02':'positive',
        'RT_01':'mixed','BCI_01':'positive'}[cid]
    return dict(display_context=ctx,display_source_evidence=src,display_provenance=prov,display_historical_fidelity=fid,display_population=pop,display_estimand=est,display_role=role,display_claim_polarity=polarity)
display=[{**r,**display_fields(r)} for r in obj]
# Nature-like scientific formatting. This is a house review profile, not journal certification.
available_families=[]
for family in ['Arial','Liberation Sans','DejaVu Sans']:
    try:
        font_manager.findfont(font_manager.FontProperties(family=family), fallback_to_default=False)
        available_families.append(family)
    except ValueError:
        continue
if not available_families:
    raise SystemExit('Install Arial, Liberation Sans or DejaVu Sans before figure reproduction')
plt.rcParams.update({'font.family':available_families,'font.size':7,'axes.titlesize':7,'axes.labelsize':7,
    'xtick.labelsize':6,'ytick.labelsize':6,'pdf.fonttype':42,'ps.fonttype':42,
    'svg.fonttype':'none','axes.linewidth':.5,'lines.linewidth':.7,'text.color':'black',
    'axes.edgecolor':'black','savefig.facecolor':'white'})
BLUE='#0072B2'; ORANGE='#D55E00'; GREY='#777777'; LIGHT='#EEF4F8'; GREEN='#009E73'
WIDTH=183/25.4
fig_inventory=[]; panel_rows=[]; bbox_issues=[]
def panel(ax, letter, title):
    ax.set_title(title,loc='left',pad=8,fontweight='normal')
    ax.text(-.07,1.08,letter,transform=ax.transAxes,fontsize=8,fontweight='bold',va='bottom')
def clean(ax):
    ax.spines[['top','right']].set_visible(False); ax.grid(False)
def save(fig, filing, stem, job, panels):
    target=OUTPUT/f'Fig{filing}'
    target.mkdir(parents=True,exist_ok=True)
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    for t in fig.findobj(matplotlib.text.Text):
        if t.get_visible() and t.get_text():
            b=t.get_window_extent(renderer)
            if b.x0 < -1 or b.y0 < -1 or b.x1>fig.bbox.width+1 or b.y1>fig.bbox.height+1:
                bbox_issues.append({'figure':stem,'text':t.get_text(),'bounds':list(b.bounds)})
    formats=['png'] if args.png_only else ['png','pdf','svg']
    for ext in formats: fig.savefig(target/f'{stem}.{ext}',dpi=600)
    fig_inventory.append({'figure':stem,'folder':filing,'formats':formats,'png_sha256':sha(target/f'{stem}.png'),'job':job})
    plt.close(fig)

# Figure 1: units, dimensions, complementary actions. No PRISMA-style pseudo-flow.
fig=plt.figure(figsize=(WIDTH,3.75))
gs=fig.add_gridspec(2,2,height_ratios=[.85,1.25],hspace=.5,wspace=.23)
a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1]); c=fig.add_subplot(gs[1,:])
for ax in [a,b,c]: ax.set_axis_off()
panel(a,'a','Different units, not a screening denominator')
for i,(n,label) in enumerate([(28,'historical candidates'),(22,'claim–estimand objects'),(15,'objects with local estimates'),(27,'historical primary model rows')]):
    y=.88-i*.235; a.text(.02,y,str(n),fontsize=7,fontweight='bold',va='center'); a.text(.18,y,label,va='center')
panel(b,'b','Separate evidence dimensions')
for i,label in enumerate(['Published use and source claim','Evidence design and comparison','Implementation and provenance','Population and target estimand','Current inferential role']):
    b.text(.02,.90-i*.21,label,va='center')
panel(c,'c','Recoverable rules and unresolved identity require different actions')
for x,title,body in [(0,'AVAglio: reconstruct the specified analysis','Recoverable population and covariate rules\nA2/A3: same 333 participants, different models\nSame-trial sensitivity; no independent validation'),(.53,'TRIO: qualify what can be inferred','Arms 1/2 identifiable by trial design\nArm 3 phase–marker mapping unresolved\nAggregate bounds cannot recover interaction')]:
    c.add_patch(Rectangle((x,.22),.47,.72,facecolor=LIGHT,edgecolor='none'))
    c.text(x+.02,.82,title,weight='bold',va='top')
    c.text(x+.02,.59,body,va='top',linespacing=1.7)
fig.text(.07,.055,'Historical computations retained; no outcome-driven reselection or replacement denominator.',fontsize=7)
fig.subplots_adjust(left=.07,right=.98,top=.91,bottom=.17)
save(fig,1,'Figure1_finite_units_and_correction_paths','Define the bounded study and its two source-driven correction pathways',['a','b','c'])

# Figure 2: no composite score; distinguish provenance and historical grades.
fig,ax=plt.subplots(figsize=(WIDTH,6.9)); ax.set_axis_off()
headers=['Use','Claim','Source\nevidence','Local\nprovenance','Historic\ngrade','Population','Estimand','Current\nrole']
xs=[.335,.389,.455,.552,.641,.716,.797,.895]
keys=['original_use_class','display_claim_polarity','display_source_evidence','display_provenance','display_historical_fidelity','display_population','display_estimand','display_role']
for x,h in zip(xs,headers): ax.text(x,1.015,h,ha='center',va='bottom',fontsize=6.4)
ax.text(0,1.015,'Object / context',va='bottom',fontsize=6.5)
for i,r in enumerate(display):
    y=1-(i+.5)/22
    if i%2==0: ax.add_patch(Rectangle((-.005,y-.0195),.995,.039,facecolor='#F4F4F4',edgecolor='none'))
    sig=r['signature'].replace('JAVELIN_Renal_101_Immuno26','JAVELIN Immuno26').replace('Tumor_Inflammation_Signature18','TIS18')
    label=f"{r['legacy_claim_id']}  {sig}"
    ax.text(0,y+.009,label,va='center',fontsize=5.8)
    ax.text(0,y-.011,r['display_context'],va='center',fontsize=5,color='black')
    for x,k in zip(xs,keys):
        value=r[k].split('_')[0] if k=='original_use_class' else r[k]
        ax.text(x,y,value,ha='center',va='center',fontsize=5.4)
ax.set_xlim(-.005,1); ax.set_ylim(-.08,1.10)
fig.text(.055,.074,'Historical grade and provenance are separate: score/label reuse is not independent assay execution.',fontsize=6)
fig.text(.055,.052,'*TRIO Arm 3 phase unresolved; Arms 1/2 randomized by design. RCC_04 source-design conflict remains explicit.',fontsize=6)
fig.text(.055,.03,'Complete definitions, stable IDs and original fields: Table 1. No composite readiness score.',fontsize=6)
fig.subplots_adjust(left=.055,right=.99,top=.93,bottom=.13)
save(fig,2,'Figure2_evidence_and_implementation_provenance','Separate intended use, evidence, implementation provenance and current role across every core object',['a'])

# Figure 3: identical ladder / alternative branch, all specifications retained.
fig=plt.figure(figsize=(WIDTH,5.25))
gs=fig.add_gridspec(3,2,height_ratios=[.85,1.45,1.10],hspace=.73,wspace=.5)
a=fig.add_subplot(gs[0,:]); a.set_axis_off(); panel(a,'a','Population restrictions precede the shared-set adjustment comparison')
for x,title,n,event in [(.02,'A0: expression-evaluable',349,270),(.365,'A1: IDH1-wild-type',339,265),(.71,'A2/A3: fixed complete cases',333,260)]:
    a.text(x,.72,title,fontsize=7); a.text(x,.39,f'{n} participants / {event} deaths',fontsize=7)
    if x<.7: a.annotate('',xy=(x+.315,.48),xytext=(x+.275,.48),arrowprops={'arrowstyle':'->','lw':.7,'color':'black'})
b=fig.add_subplot(gs[1,0]); c=fig.add_subplot(gs[1,1]); d=fig.add_subplot(gs[2,:])
for ax,cid,letter,title in [(b,'GBM_01','b','Phillips deposited labels'),(c,'GBM_02','c','Verhaak deposited labels')]:
    panel(ax,letter,title); rr=[r for r in av if r['claim_id']==cid and r['model_id']!='A4']
    for i,r in enumerate(rr):
        y=3-i; h,lo,hi=[float(r[k]) for k in ['current_interaction_hr','current_ci95_low','current_ci95_high']]
        ax.errorbar(h,y,xerr=[[h-lo],[hi-h]],fmt='o',color=BLUE,markersize=3,capsize=2)
    ax.set_yticks(range(4),['A3: adjusted, 333','A2: unadjusted, 333','A1: unadjusted, 339','A0: unadjusted, 349']); ax.set_ylim(-.5,3.5)
    ax.set_xscale('log'); ax.set_xlim(.2,1.3); ax.set_xticks([.25,.5,1],['0.25','0.5','1']); ax.minorticks_off()
    ax.axvline(1,color=GREY,lw=.6,ls='--'); ax.set_xlabel('Interaction HR (95% CI)'); clean(ax)
panel(d,'d','A4 is a separate missing-category / penalized sensitivity branch')
for y,cid in [(1,'GBM_01'),(0,'GBM_02')]:
    for offset,mid,m,col in [(.12,'A3','o',BLUE),(-.12,'A4','D',GREY)]:
        r=next(r for r in av if r['claim_id']==cid and r['model_id']==mid)
        h,lo,hi=[float(r[k]) for k in ['current_interaction_hr','current_ci95_low','current_ci95_high']]
        d.errorbar(h,y+offset,xerr=[[h-lo],[hi-h]],fmt=m,color=col,markersize=3,capsize=2,label=mid if y==1 else None)
d.set_yticks([0,1],['Verhaak','Phillips']); d.set_ylim(-.4,1.4); d.set_xscale('log'); d.set_xlim(.2,1.3)
d.set_xticks([.25,.5,1],['0.25','0.5','1']); d.minorticks_off(); d.axvline(1,color=GREY,lw=.6,ls='--')
d.set_xlabel('Interaction HR (95% CI)'); d.legend(frameon=False,loc='upper right',fontsize=6,ncol=2); clean(d)
fig.text(.08,.015,'All estimates: same trial, reused subtype labels. HR is a ratio of treatment HRs, not a subgroup HR.',fontsize=6)
fig.subplots_adjust(left=.22,right=.96,top=.93,bottom=.105)
save(fig,3,'Figure3_AVAglio_shared_population_model_ladder','Show the source-defined change in estimand/model specification without selecting by significance',['a','b','c','d'])

# Figure 4: discrete compatibility / information boundary, not a fabricated randomized estimate.
fig=plt.figure(figsize=(WIDTH,4.6))
gs=fig.add_gridspec(2,2,height_ratios=[1.3,.8],hspace=.60,wspace=.35)
a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1]); c=fig.add_subplot(gs[1,:]); c.set_axis_off()
panel(a,'a','Public TRIO arm linkage')
ns=[31,29,50]; ev=[15,7,25]
a.barh([2,1,0],ns,color=['#E0EDF5','#E0EDF5','#DDDDDD'],edgecolor='none')
a.barh([2,1,0],ev,color=[BLUE,BLUE,GREY],height=.8)
for y,n,e in zip([2,1,0],ns,ev): a.text(n+1,y,f'{e}/{n} pCR',va='center',fontsize=6)
a.set_yticks([2,1,0],['Arm 1: randomized','Arm 2: randomized','Arm 3: phase unresolved']); a.set_xlim(0,72); a.set_xticks([0,20,40,60]); a.set_xlabel('Participants'); clean(a)
panel(b,'b','Report-compatible randomized Arm 3 states')
b.scatter([x['randomized_n'] for x in pairs],[x['randomized_pcr'] for x in pairs],s=12,color=BLUE)
b.set_xticks([30,32,34,36,38]); b.set_yticks([16,17,18,19,20,21]); b.set_xlim(29.5,38.5); b.set_ylim(15.5,21.5)
b.set_xlabel('Randomized participants in public Arm 3'); b.set_ylabel('pCR among those participants'); clean(b)
panel(c,'c','Aggregate compatibility does not identify a biomarker interaction')
c.text(.01,.84,'24 feasible integer states\n30–38 randomized participants\nRaw pCR fraction: 48.5–60.0%',va='top',linespacing=1.55)
c.text(.48,.84,'Missing: joint phase–marker–outcome mapping\nRetain all ten historical comparisons\nDo not fit a pseudo-corrected randomized interaction',va='top',linespacing=1.55)
fig.text(.04,.035,'Conditional on the public Arm 3 set being a subset of the reported combined arm with the same pCR definition.',fontsize=6)
fig.text(.04,.013,'Dots are feasible counts, not participants. The compatibility range is neither a CI nor a treatment-effect bound.',fontsize=6)
fig.subplots_adjust(left=.17,right=.97,top=.91,bottom=.17)
save(fig,4,'Figure4_TRIO_partial_identifiability','Make the completed information-limited correction pathway visible without inventing participant phase labels',['a','b','c'])

# Supplementary S1: full current cross-trial role, independent of significance.
fig,axes=plt.subplots(1,2,figsize=(WIDTH,3.5),gridspec_kw={'width_ratios':[1,1.2]})
for ax in axes: ax.set_axis_off()
panel(axes[0],'a','Thirteen units share three resource clusters')
for i,(count,title,role) in enumerate([(10,'TRIO–CHER-LOB','TRIO phase unresolved'),(2,'AVAglio–GLARIUS','Medium transportability'),(1,'IGG14–BrighTNess','Dependent evaluation')]):
    y=.8-i*.28; axes[0].text(0,y,str(count),fontsize=7,fontweight='bold'); axes[0].text(.17,y,title); axes[0].text(.17,y-.10,role,fontsize=6)
panel(axes[1],'b','Current strict replication proportion: not estimable')
axes[1].text(.02,.82,'Requirements assessed before a replication label:',weight='bold',fontsize=6.8)
axes[1].text(.02,.69,'Verified target population\nCompatible estimand\nIndependent evaluation\nRecoverable positive source decision path',linespacing=1.8,va='top')
axes[1].text(.02,.25,'No unit meets every current prerequisite.\nAn empty eligible set is not a 0% success rate.',linespacing=1.6,va='top')
fig.subplots_adjust(left=.06,right=.97,top=.85,bottom=.08,wspace=.3)
save(fig,5,'FigureS1_cross_trial_eligibility','Separate dependent historical units from current evaluability, without a post-hoc denominator',['a','b'])

# Supplementary S2: retain all 23 rows and conditional interval warning.
fig=plt.figure(figsize=(WIDTH,7.2)); gs=fig.add_gridspec(3,1,height_ratios=[10,10,3],hspace=.62)
for group,(trial,letter,title) in enumerate([('TRIO-US B07','a','TRIO: historical recorded-arm sensitivity; phase unresolved'),('CHER-LOB','b','CHER-LOB: standalone trial-specific sensitivity'),('OTHER','c','Other trial-specific source / implementation settings')]):
    ax=fig.add_subplot(gs[group]); panel(ax,letter,title)
    rr=[r for r in ab if (r['trial']==trial if trial!='OTHER' else r['trial'] not in ['TRIO-US B07','CHER-LOB'])]
    labels=[]
    for i,r in enumerate(rr):
        y=len(rr)-1-i; h,lo,hi=[float(r[k]) for k in ['delta_rd','bootstrap_ci_low','bootstrap_ci_high']]
        warn=float(r['bootstrap_valid_fraction'])<.95
        ax.errorbar(h,y,xerr=[[h-lo],[hi-h]],fmt='s' if warn else 'o',color=GREY if group==0 else BLUE,markersize=2.7,capsize=1.6)
        labels.append(r['signature']+(' *' if warn else ''))
        ax.text(1.01,y,f"q={float(r['bootstrap_bh_q_within_family']):.3f}; {r['bootstrap_valid']}/5000",transform=ax.get_yaxis_transform(),va='center',fontsize=5.5)
    ax.set_yticks(range(len(rr)),labels[::-1]); ax.set_ylim(-.5,len(rr)-.5)
    ax.set_xlim(-1,1); ax.set_xticks([-1,-.5,0,.5,1]); ax.axvline(0,color=GREY,lw=.6,ls='--'); clean(ax)
    if group==2: ax.set_xlabel('ΔRD = RD(Q75) − RD(Q25); percentile 95% interval')
fig.text(.08,.047,'*CHER-LOB ESR1: 4736/5000 valid replicates; interval conditional on successful fits.',fontsize=6)
fig.text(.08,.028,'All 23 rows retained. No additive result changes a primary label; q summarizes the frozen sign-tail BH families.',fontsize=6)
fig.text(.08,.009,'DOP source population: high-risk HER2-negative breast cancer, including HR-positive and triple-negative disease.',fontsize=6)
fig.subplots_adjust(left=.28,right=.77,top=.95,bottom=.11)
save(fig,6,'FigureS2_all23_absolute_effect_sensitivities','Show full absolute-scale uncertainty and bootstrap limitations without promoting a nominal result',['a','b','c'])

# Supplementary S3: old numbers explicitly historical, distinct scales / populations.
fig=plt.figure(figsize=(WIDTH,7.2)); gs=fig.add_gridspec(3,1,height_ratios=[10,10,7],hspace=.50)
for group,(trial,letter,title) in enumerate([('TRIO-US B07','a','TRIO historical primary estimates: no verified randomized phase'),('CHER-LOB','b','CHER-LOB historical primary estimates: standalone trial context'),('OTHER','c','Other historical primary estimates (not the AVAglio A2/A3 fits)')]):
    ax=fig.add_subplot(gs[group]); panel(ax,letter,title)
    rr=[r for r in prim if (r['trial']==trial if trial!='OTHER' else r['trial'] not in ['TRIO-US B07','CHER-LOB'])]
    labs=[]
    for i,r in enumerate(rr):
        y=len(rr)-1-i; h,lo,hi=[float(r[k]) for k in ['effect_ratio','ci95_low_ratio','ci95_high_ratio']]
        scale='HR' if 'cox' in r['model'].lower() else 'OR'
        ax.errorbar(h,y,xerr=[[h-lo],[hi-h]],fmt='D' if scale=='HR' else 'o',color=GREY if group==0 else BLUE,markersize=2.6,capsize=1.5)
        labs.append((r['trial']+' / ' if group==2 else '')+r['signature'])
        ax.text(1.01,y,f"{scale}; n={r['n']}; events={r['events']}",transform=ax.get_yaxis_transform(),va='center',fontsize=5.3)
    ax.set_yticks(range(len(rr)),labs[::-1]); ax.set_ylim(-.5,len(rr)-.5); ax.set_xscale('log'); ax.set_xlim(.01,100)
    ax.set_xticks([.01,.1,1,10,100],['0.01','0.1','1','10','100']); ax.minorticks_off(); ax.axvline(1,color=GREY,lw=.6,ls='--'); clean(ax)
    if group==2: ax.set_xlabel('Historical interaction ratio (95% CI); OR and HR are not pooled')
fig.text(.06,.028,'All 27 historical model rows retained; these values are not current strict replication labels.',fontsize=6)
fig.text(.06,.009,'DOP: HER2-negative breast cancer. AVAglio historical A0 estimates remain separate from the corrected model ladder.',fontsize=6)
fig.subplots_adjust(left=.37,right=.78,top=.95,bottom=.10)
save(fig,7,'FigureS3_all27_historical_primary_estimates','Preserve the complete historical numerical record with current role qualifications',['a','b','c'])

(OUTPUT/'reproduction_record.json').write_text(json.dumps({'assemblies':fig_inventory,'canvas_issues':bbox_issues,'model_fits':0,'bootstrap_runs':0,'font_profile':'Arial / Liberation Sans / DejaVu Sans fallback','available_font_families':available_families,'matplotlib_version':matplotlib.__version__,'numpy_version':np.__version__},indent=2),encoding='utf-8')
print(json.dumps({'assemblies':len(fig_inventory),'canvas_issues':len(bbox_issues),'output':str(OUTPUT),'model_fits':0}))
if bbox_issues:raise SystemExit('Text outside canvas; review generated figure geometry')
