#!/usr/bin/env python3
"""Four source-driven redraws plus three justified byte-identical reuse assemblies.

Only frozen/reviewed aggregate sources are read. No model is fitted.
"""
from pathlib import Path
import argparse, csv, json, hashlib, shutil, datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
from matplotlib import font_manager
from PIL import Image
from pypdf import PdfReader

BLUE='#0072B2'; GREY='#666666'; LIGHT='#EEEEEE'
REV='RPv5_v1.6_wp3_20261013'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    with Path(p).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
def write_tsv(p,rows):
    with Path(p).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output-dir',type=Path,default=Path('generated_rpv5'))
    parser.add_argument('--font',default='Arial',help='The reviewed Windows typography uses Arial; record any alternative explicitly')
    args=parser.parse_args(); repo=args.repository.resolve(); root=args.output_dir.resolve()
    require(not root.exists(),'Output directory already exists; select a new output directory')
    require(root!=repo and (repo not in root.parents or root.name=='generated_rpv5'), 'Never overwrite the published tree')
    agg=repo/'1_data/aggregate/frozen_v1.5'
    review=repo/'1_data/aggregate/reviewed_v1.6'
    out=root/'results'
    report=root/'report'
    out.mkdir(parents=True,exist_ok=True);report.mkdir(parents=True,exist_ok=True)
    watched=json.loads((repo/'0_admin/audit/rpv5_public_asset_contract.json').read_text(encoding='utf-8'))
    watched=watched['aggregate_files']+watched['figure_files']
    require(all(sha(repo/r['relative_path'])==r['raw_sha256'] for r in watched),'Published input contract changed')
    records=[review/n for n in ['figure2_source22_v1.6.tsv','Additional_file_1B_implementation27.tsv','Additional_file_4C_absolute23.tsv']]
    records += [agg/n for n in ['primary27.tsv','trioarms3.tsv','triobounds9.tsv','avaglio10.tsv','cross13.tsv','objects22.tsv']]
    before={str(p):sha(p) for p in records}
    obj=read(records[0]); impl=read(records[1]); ab=read(records[2]); prim=read(agg/'primary27.tsv')
    require((len(obj),len(impl),len(ab),len(prim))==(22,27,23,27),'Row loss or duplication')
    require(len({r['claim_estimand_id'] for r in obj})==22,'Object identity duplication')
    for r in obj[:10]:require(r['provenance_code']=='TRIO:AS / CHER:LS','HER2 merged provenance regressed')
    require(next(r for r in obj if r['legacy_claim_id']=='RCC_04')['polarity']=='positive','RCC04 polarity regressed')
    write_tsv(out/'FigureS2_plot_source23.tsv',ab)
    write_tsv(out/'FigureS3_plot_source27.tsv',prim)
    family=args.font
    font_manager.findfont(font_manager.FontProperties(family=family),fallback_to_default=False)
    plt.rcParams.update({'font.family':family,'font.size':6,'axes.titlesize':7,'axes.labelsize':6,
        'xtick.labelsize':5.7,'ytick.labelsize':5.8,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
        'axes.linewidth':.5,'lines.linewidth':.7,'text.color':'black','savefig.facecolor':'white'})
    inventory=[]; canvas_issues=[]; column_issues=[]; panels=[]
    def panel(ax,letter,title):
        ax.set_title(title,loc='left',pad=8,fontsize=7)
        ax.text(-.075,1.075,letter,transform=ax.transAxes,fontsize=7,fontweight='bold',va='bottom')
    def clean(ax):ax.spines[['top','right']].set_visible(False);ax.grid(False)
    def save(fig,folder,stem,pids,source,action='REGENERATED'):
        target=root/f'4_figures/Fig{folder}'/REV;target.mkdir(parents=True,exist_ok=True)
        fig.canvas.draw();renderer=fig.canvas.get_renderer()
        for t in fig.findobj(matplotlib.text.Text):
            if t.get_visible() and t.get_text():
                b=t.get_window_extent(renderer)
                if b.x0<-.8 or b.y0<-.8 or b.x1>fig.bbox.width+.8 or b.y1>fig.bbox.height+.8:
                    canvas_issues.append({'figure':stem,'text':t.get_text(),'bbox':list(b.bounds)})
        for ext in ['pdf','svg','png']:fig.savefig(target/f'{stem}.{ext}',dpi=600)
        pdf=PdfReader(target/f'{stem}.pdf');p=pdf.pages[0]
        inv={'figure':stem,'filing_folder':f'Fig{folder}','action':action,'panel_ids':pids,
             'width_mm':float(p.mediabox.width)*25.4/72,'height_mm':float(p.mediabox.height)*25.4/72,
             'assets':{ext:{'path':str(target/f'{stem}.{ext}'),'bytes':(target/f'{stem}.{ext}').stat().st_size,'sha256':sha(target/f'{stem}.{ext}')} for ext in ['pdf','svg','png']}}
        im=Image.open(target/f'{stem}.png');inv['png_pixels']=list(im.size);inv['png_dpi']=im.info.get('dpi');im.close()
        inventory.append(inv)
        for pid in pids:panels.append({'figure':stem,'panel':pid,'action':action,'sources':source,'plot_script_sha256':sha(__file__),'numeric_fit':'NONE_AGGREGATE_ONLY','visual_review':'PENDING_ACTUAL_INSPECTION'})
        plt.close(fig)

    # Fig2: two panels aligned on a single stable 22-object row set.
    display=[]
    roles={'POPULATION_UNVERIFIED':'pop. unverified','ROLE_REFRAMED':'reframed','NOT_CURRENTLY_EVALUABLE':'source audit','TARGETED_REANALYSIS':'reanalysed','IMPLEMENTATION_LIMITED':'limited'}
    for r in obj:
        cid=r['legacy_claim_id']
        if cid.startswith('HER2'):d,p,e='D1','TU / CR','E1'
        elif cid=='TNBC_01':d,p,e='D2','R','E2'
        elif cid=='TNBC_03':d,p,e='D3','AR','E3'
        elif cid=='TNBC_04':d,p,e='D3','R','E4'
        elif cid in ['RCC_01','RCC_02']:d,p,e='D4','AG','E5'
        elif cid=='RCC_03':d,p,e='D4','AG','E6'
        elif cid=='RCC_04':d,p,e='D5*','AG','E7'
        elif cid=='RCC_05':d,p,e='D6','AG','E7'
        elif cid.startswith('GBM'):d,p,e='D7','R','E8'
        elif cid=='RT_01':d,p,e='D8','PO','E9'
        elif cid=='BCI_01':d,p,e='D9','NR','E10'
        else:raise ValueError(cid)
        short=r['signature'].replace('JAVELIN_Renal_101_Immuno26','JAVELIN Immuno26').replace('Tumor_Inflammation_Signature18','TIS18')
        short=short.replace('_',' ')
        prov=r['provenance_code'].replace('BRIGHT:','Bright ').replace('AVA+GLAR:','AVA+GLAR ').replace('; no IPD fit',' only').replace('DOP:','DOP ').replace('TRIO:AS / CHER:LS','TRIO AS | CHER LS')
        display.append({**r,'plot_label':cid+' '+short,'design_code':d,'population_code':p,'estimand_code':e,'role_label':roles[r['current_role']],'plot_provenance':prov})
    write_tsv(out/'Figure2_plot_source22.tsv',display)
    fig=plt.figure(figsize=(183/25.4,164/25.4));ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,183),ylim=(0,164));ax.set_axis_off()
    def text(x,y,s,ha='left',fs=5.7,weight='normal'):return ax.text(x,y,s,ha=ha,va='center',fontsize=fs,fontweight=weight)
    text(4,158,'a',fs=7,weight='bold');text(9,158,'Original source question and evidence',fs=7)
    text(92,158,'b',fs=7,weight='bold');text(97,158,'Local provenance and current inference',fs=7)
    headers=[(4,'Object / signature','left'),(49,'Use','center'),(61.5,'Polarity','center'),(78,'Design','center'),(109,'Trial-specific provenance','center'),(138,'Population','center'),(154.5,'Estimand','center'),(171.5,'Role','center')]
    for x,h,ha in headers:text(x,148,h,ha,fs=5.6,weight='bold')
    ax.plot([4,180],[144,144],color='black',lw=.5);ax.plot([88,88],[53,153],color='#888888',lw=.5)
    cell_limits={'plot_label':(4,45),'original_use':(45,53),'polarity':(54,69),'design_code':(70,86),'plot_provenance':(91,127),'population_code':(130,146),'estimand_code':(147,162),'role_label':(163,180)}
    cell_text=[]
    pol_marker={'positive':'o','negative':'s','exploratory':'^','mixed':'D','unresolved':'x'}
    for i,r in enumerate(display):
        y=141-i*4.05
        if i%2==0:ax.add_patch(Rectangle((3,y-1.95),178,3.9,facecolor='#F3F3F3',edgecolor='none'))
        cell_text.append((text(4,y,r['plot_label'],fs=5.7),'plot_label',r['legacy_claim_id']))
        for x,k in [(49,'original_use'),(61.5,'polarity'),(78,'design_code'),(109,'plot_provenance'),(138,'population_code'),(154.5,'estimand_code'),(171.5,'role_label')]:
            # Literal words supplement controlled codes; no composite score.
            cell_text.append((text(x,y,r[k],'center',5.5),'%s'%k,r['legacy_claim_id']))
    legends=[
      'Use: U1, treated-condition association; U2, differential treatment effect. Polarity applies to the source question, not a validation verdict.',
      'Provenance: AS, author-score reuse; LS, local source-compatible score; DL, deposited labels; GM, gene mean; AG, aggregate only; PA, partial assay.',
      'D1 treated/mixed cohort; D2 retrospective randomized; D3 adaptive-platform biomarker analysis; D4 exploratory randomized/subgroup study;',
      'D5* conflicting historical interaction design; D6 treated-arm response; D7 adjusted randomized; D8 pooled controlled; D9 nested randomized.',
      'Population: TU, TRIO phase unverified; CR, CHER randomized context; R, trial context; AR, adaptive source; AG, aggregate; PO, pooled; NR, nested.',
      'Estimand: E1 U1/U2 mismatch; E2 aligned but dependent evaluation; E3 source-cohort association; E4 continuous/binary mismatch;',
      'E5 formal interaction not located; E6 exploratory subgroup; E7 source audit; E8 AVA aligned / GLARIUS medium transportability;',
      'E9 pooled endpoint-specific interaction, not strategy utility; E10 source interaction positive / local assay not executable.',
      '*RCC_04: positive U1 located; standalone Immuno26 U2 not located in reviewed material. Historical design conflict remains recorded.',
      'CHER final score-generation chain remains incompletely recovered. Historical fidelity grades are retained in Table 1, not reassigned here.',
      'All 22 objects shown once. Full original fields, code definitions and 27 local contexts accompany the figure. No composite score.'
    ]
    for i,line in enumerate(legends):text(4,47-i*3.8,line,fs=5.5)
    fig.canvas.draw();ren=fig.canvas.get_renderer()
    for t,key,cid in cell_text:
        bbox=t.get_window_extent(ren); coords=ax.transData.inverted().transform([[bbox.x0,bbox.y0],[bbox.x1,bbox.y1]])
        lo,hi=cell_limits[key]
        if coords[0,0]<lo-.25 or coords[1,0]>hi+.25:column_issues.append({'object':cid,'column':key,'text':t.get_text(),'expected_x':[lo,hi],'actual_x':[float(coords[0,0]),float(coords[1,0])]})
    save(fig,2,'Figure2_source_and_trial_provenance',['a','b'],'Figure2_plot_source22.tsv; figure2_source22_v1.6.tsv; trial_implementation_crosswalk27_v1.6.tsv')

    # Fig4: bars use a common event key; design/phase labels remain independent.
    pairs=[]
    for r in range(30,39):
        for s in range(max(16,r-17),min(21,r-14)+1):pairs.append({'randomized_n':r,'randomized_pcr':s,'raw_pcr_fraction':s/r})
    require(len(pairs)==24,'Compatibility count changed');write_tsv(out/'Figure4_integer_states24.tsv',pairs)
    fig=plt.figure(figsize=(183/25.4,126/25.4));gs=fig.add_gridspec(2,2,height_ratios=[1.45,.9],hspace=.65,wspace=.42)
    a=fig.add_subplot(gs[0,0]);b=fig.add_subplot(gs[0,1]);c=fig.add_subplot(gs[1,:]);c.set_axis_off()
    panel(a,'a','Public arm linkage: events and allocation identity')
    ns=[31,29,50];ev=[15,7,25]
    a.barh([2,1,0],ns,color=LIGHT);a.barh([2,1,0],ev,color=BLUE,height=.8)
    for y,n,e in zip([2,1,0],ns,ev):a.text(n+1,y,f'{e}/{n}',va='center',fontsize=6)
    a.set_yticks([2,1,0],['Arm 1: randomized by design','Arm 2: randomized by design','Arm 3: phase unresolved']);a.set_xlim(0,64);a.set_xticks([0,20,40,60]);a.set_ylim(-.7,2.8);a.set_xlabel('Participants (pCR / total at right)');clean(a)
    a.legend(handles=[Patch(facecolor=BLUE,label='pCR'),Patch(facecolor=LIGHT,label='non-pCR')],frameon=False,fontsize=5.7,ncol=2,loc='upper left',bbox_to_anchor=(0,1.03),borderaxespad=0)
    panel(b,'b','Conditional integer states, not patients')
    b.scatter([r['randomized_n'] for r in pairs],[r['randomized_pcr'] for r in pairs],color=BLUE,s=11)
    b.set(xlim=(29.5,38.5),ylim=(15.5,21.5));b.set_xticks([30,32,34,36,38]);b.set_yticks([16,17,18,19,20,21]);b.set_xlabel('Randomized public Arm 3 participants');b.set_ylabel('pCR in the randomized subset');clean(b)
    panel(c,'c','Missing joint identity prevents a corrected biomarker interaction')
    c.text(0,.84,'24 feasible integer states\n30-38 randomized participants\nRaw pCR proportion: 48.5-60.0%',va='top',linespacing=1.55)
    c.text(.51,.84,'Unresolved: phase-marker-outcome mapping\nHistorical comparison: allocation phase unverified\nNo pseudo-corrected participant subset is fitted',va='top',linespacing=1.55)
    fig.text(.045,.041,'Assumption: public Arm 3 is a subset of the reported combined arm, with the same endpoint definition.',fontsize=5.7)
    fig.text(.045,.019,'The 48.5-60.0% compatibility range is not a CI, treatment-effect bound or marker-by-treatment interaction bound.',fontsize=5.7)
    fig.subplots_adjust(left=.22,right=.97,top=.91,bottom=.18)
    save(fig,4,'Figure4_TRIO_partial_identifiability',['a','b','c'],'trioarms3.tsv; triobounds9.tsv; Figure4_integer_states24.tsv')

    # S2: descriptive historical sign-tail / BH annotations, no FDR claim.
    fig=plt.figure(figsize=(183/25.4,215/25.4));gs=fig.add_gridspec(3,1,height_ratios=[10,10,3],hspace=.62)
    for group,(trial,letter,title) in enumerate([('TRIO-US B07','a','TRIO: recorded-arm sensitivity; phase unresolved'),('CHER-LOB','b','CHER-LOB: separate trial-specific sensitivity'),('OTHER','c','Other source/implementation settings; distinct treatment contrasts')]):
        ax=fig.add_subplot(gs[group]);panel(ax,letter,title)
        rr=[r for r in ab if (r['trial']==trial if trial!='OTHER' else r['trial'] not in ['TRIO-US B07','CHER-LOB'])]
        labs=[]
        for i,r in enumerate(rr):
            y=len(rr)-1-i;h,lo,hi=[float(r[k]) for k in ['delta_rd','bootstrap_ci_low','bootstrap_ci_high']];warn=float(r['bootstrap_valid_fraction'])<.95
            ax.errorbar(h,y,xerr=[[h-lo],[hi-h]],fmt='s' if warn else 'o',color=GREY if group==0 else BLUE,markersize=2.8,capsize=1.7)
            labs.append(('DOP / ' if 'DOP' in r['trial'] else 'Bright / ' if r['trial']=='BrighTNess' else '')+r['signature']+(' *' if warn else ''))
            ax.text(1.02,y,f"{float(r['bootstrap_sign_p']):.3f} / {float(r['bootstrap_bh_q_within_family']):.3f}",transform=ax.get_yaxis_transform(),va='center',fontsize=5.5)
            ax.text(1.45,y,f"{r['bootstrap_valid']}/{r['bootstrap_requested']}",transform=ax.get_yaxis_transform(),va='center',fontsize=5.5)
        ax.text(1.02,1.045,'tail / BH-h',transform=ax.transAxes,fontsize=5.5);ax.text(1.45,1.045,'valid / requested',transform=ax.transAxes,fontsize=5.5)
        ax.set_yticks(range(len(rr)),labs[::-1]);ax.set_ylim(-.5,len(rr)-.5);ax.set_xlim(-1,1);ax.set_xticks([-1,-.5,0,.5,1]);ax.axvline(0,color=GREY,ls='--',lw=.6);clean(ax)
        if group==2:ax.set_xlabel('Delta RD = RD(Q75) - RD(Q25); percentile interval over valid fits')
    lines=[
      'Circle: technical PASS; square*: conditional interval, CHER ESR1 4736/5000 valid fits. Higher marker means higher frozen score.',
      'tail / BH-h: historical two-sided bootstrap sign-tail / within-family BH-transformed summary; confirmatory FDR control not established.',
      'T1/T0: TRIO and CHER, trastuzumab+lapatinib / trastuzumab; BrighTNess IGG14, carboplatin+paclitaxel / paclitaxel;',
      'BrighTNess CIN70, veliparib+carboplatin+paclitaxel / paclitaxel; DOP, durvalumab+olaparib+paclitaxel / FFPE paclitaxel control.',
      'Common protocol chemotherapy applies. DOP includes HR-positive and triple-negative HER2-negative disease.',
      'TRIO contrasts do not establish randomized benefit. All 23 rows and original primary labels retained; no promotion from this sensitivity.'
    ]
    for i,line in enumerate(lines):fig.text(.04,.096-i*.0145,line,fontsize=5.5)
    fig.subplots_adjust(left=.29,right=.69,top=.955,bottom=.18)
    save(fig,6,'FigureS2_all23_absolute_effect_sensitivities',['a','b','c'],'absolute23_interpretation_v1.6.tsv')

    # S3: numerical historical OR/HR values plus literal comparison keys.
    fig=plt.figure(figsize=(183/25.4,226/25.4));gs=fig.add_gridspec(3,1,height_ratios=[10,10,7],hspace=.53)
    for group,(trial,letter,title) in enumerate([('TRIO-US B07','a','TRIO: historical estimates; no verified randomized phase'),('CHER-LOB','b','CHER-LOB: historical estimates in a separate trial'),('OTHER','c','Other historical estimates; AVAglio A0, not A2/A3')]):
        ax=fig.add_subplot(gs[group]);panel(ax,letter,title)
        rr=[r for r in prim if (r['trial']==trial if trial!='OTHER' else r['trial'] not in ['TRIO-US B07','CHER-LOB'])];labs=[]
        for i,r in enumerate(rr):
            y=len(rr)-1-i;h,lo,hi=[float(r[k]) for k in ['effect_ratio','ci95_low_ratio','ci95_high_ratio']];scale='HR' if 'cox' in r['model'].lower() else 'OR'
            ax.errorbar(h,y,xerr=[[h-lo],[hi-h]],fmt='D' if scale=='HR' else 'o',color=GREY if group==0 else BLUE,markersize=2.7,capsize=1.7)
            trialshort='DOP' if 'DOP' in r['trial'] else r['trial']
            labs.append((trialshort+' / ' if group==2 else '')+r['signature'])
            ax.text(1.02,y,f"{scale}; {r['n']} / {r['events']}",transform=ax.get_yaxis_transform(),va='center',fontsize=5.5)
        ax.text(1.02,1.045,'scale; n / events',transform=ax.transAxes,fontsize=5.5)
        ax.set_yticks(range(len(rr)),labs[::-1]);ax.set_ylim(-.5,len(rr)-.5);ax.set_xscale('log');ax.set_xlim(.01,100);ax.set_xticks([.01,.1,1,10,100],['0.01','0.1','1','10','100']);ax.minorticks_off();ax.axvline(1,color=GREY,lw=.6,ls='--');clean(ax)
        if group==2:ax.set_xlabel('Historical interaction ratio with Wald 95% CI (OR/HR not pooled)')
    lines=[
      'Circle: logistic interaction OR; diamond: Cox interaction HR. Ratios compare treatment effects, not subgroup outcome ratios.',
      'Binary marker direction: higher frozen score (one historical pooled SD); GBM marker=1: deposited proneural label.',
      'T1/T0: TRIO and CHER, trastuzumab+lapatinib / trastuzumab; Bright IGG14, carboplatin+paclitaxel / paclitaxel;',
      'Bright CIN70, veliparib+carboplatin+paclitaxel / paclitaxel; DOP, durvalumab+olaparib+paclitaxel / FFPE paclitaxel control;',
      'AVAglio, bevacizumab / placebo with common RT/TMZ; GLARIUS, bevacizumab+irinotecan / TMZ with shared radiotherapy.',
      'All 27 historical rows retained; historical labels do not establish current strict replication. DOP is not exclusively TNBC.'
    ]
    for i,line in enumerate(lines):fig.text(.04,.088-i*.014,line,fontsize=5.5)
    fig.subplots_adjust(left=.365,right=.78,top=.955,bottom=.17)
    save(fig,7,'FigureS3_all27_historical_primary_estimates',['a','b','c'],'primary27.tsv; trial_implementation_crosswalk27_v1.6.tsv')

    # Reuse is a disclosed byte copy, NOT a claim of new generation/authoring.
    stems={1:('Figure1_finite_units_and_correction_paths',['a','b','c'],'objects22.tsv;primary27.tsv;absolute23.tsv;cross13.tsv;avaglio10.tsv'),
           3:('Figure3_AVAglio_shared_population_model_ladder',['a','b','c','d'],'avaglio10.tsv'),
           5:('FigureS1_cross_trial_eligibility',['a','b'],'cross13.tsv')}
    for folder,(stem,pids,source) in stems.items():
        target=root/f'4_figures/Fig{folder}'/REV;target.mkdir(parents=True,exist_ok=True)
        for ext in ['pdf','png','svg']:
            old=repo/f'4_figures/Fig{folder}/current_v1.5/{stem}.{ext}';new=target/f'{stem}.{ext}';shutil.copy2(old,new);require(sha(old)==sha(new),'Reuse bytes differ')
        p=PdfReader(target/f'{stem}.pdf').pages[0]
        inventory.append({'figure':stem,'filing_folder':f'Fig{folder}','action':'BYTE_IDENTICAL_REUSE_JUSTIFIED','panel_ids':pids,
            'width_mm':float(p.mediabox.width)*25.4/72,'height_mm':float(p.mediabox.height)*25.4/72,
            'assets':{ext:{'path':str(target/f'{stem}.{ext}'),'bytes':(target/f'{stem}.{ext}').stat().st_size,'sha256':sha(target/f'{stem}.{ext}')} for ext in ['pdf','png','svg']},
            'reason':'No numeric/source-display correction required in this assembly; manual re-review pending. Historical 8pt headings retained, not strict Nature typography certification.'})
        for pid in pids:panels.append({'figure':stem,'panel':pid,'action':'BYTE_IDENTICAL_REUSE_JUSTIFIED','sources':source,'plot_script_sha256':'d50096f3aa788d1e0661e8ea2b2a566d2f26b1260a41b77d612f1fc367705cce','numeric_fit':'NONE_AGGREGATE_ONLY','visual_review':'PENDING_ACTUAL_INSPECTION'})
    require(before=={str(p):sha(p) for p in records},'Aggregate/review inputs changed')
    write_tsv(out/'PANEL_SOURCE_MAP20.tsv',panels)
    record={'date_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'regenerated_assemblies':4,'byte_identical_reuse_assemblies':3,'panels':len(panels),
       'canvas_issues':canvas_issues,'matrix_column_issues':column_issues,'inputs_unchanged':True,'published_inputs_unchanged':all(sha(repo/r['relative_path'])==r['raw_sha256'] for r in watched),
       'font':family,'new_text_range_pt':[5.5,7],'matplotlib':matplotlib.__version__,'script_sha256':sha(__file__),
       'input_sha256':before,'inventory':sorted(inventory,key=lambda x:x['filing_folder']),'new_model_fits':0,'new_bootstrap_fits':0,'visual_QA':'PENDING_ACTUAL_INSPECTION'}
    (out/'FIGURE_EXECUTION_RECORD.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:record[k] for k in ['regenerated_assemblies','byte_identical_reuse_assemblies','panels','canvas_issues','matrix_column_issues','published_inputs_unchanged']},ensure_ascii=False,indent=2))
    require(not canvas_issues and not column_issues,'Geometry QA needs repair; generated draft retained')

if __name__=='__main__':main()
