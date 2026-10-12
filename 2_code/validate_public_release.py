#!/usr/bin/env python3
"""Validate the numbered, aggregate-only v1.5 public tree (standard library only).

The previous v1.4 snapshot is checked independently, not rewritten to make it pass.
This validator checks public artifacts, not author approval or clinical validity.
"""
from pathlib import Path
import ast, csv, hashlib, json, math, re, sys
from collections import Counter
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]
ARCH=ROOT/'8_archive/legacy_public_snapshot_v1.4'
MANIFEST=ROOT/'MANIFEST_SHA256.tsv'
EXCLUDE={'.git','__pycache__','.pytest_cache','.venv','node_modules','generated_v1_5'}
TEXT={'.cff','.csv','.json','.md','.ps1','.py','.r','.svg','.tsv','.txt','.yaml','.yml'}
TEXT_NAMES={'.gitignore','.gitattributes','LICENSE'}
SECRET=re.compile(r'\b(?:gh[opusr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b')
PRIVATE_PATH=re.compile(r'(?i)(?:(?<![A-Za-z0-9])[A-Z]:[\\/]|/mnt/data/|Users\\Administrator|sandbox:/mnt/data)')
FORBIDDEN={'raw_data','participant_level','patient_level','restricted_internal','node_modules','.venv','private','secrets'}
ID_HEADERS={'patient_id','participant_id','sample_id','subject_id','mrn'}
checks=[]
def add(name,ok,detail): checks.append({'name':name,'pass':bool(ok),'detail':detail})
def canonical(p):
    b=p.read_bytes()
    return b.replace(b'\r\n',b'\n') if p.suffix.lower() in TEXT or p.name in TEXT_NAMES else b
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter='\t' if p.suffix.lower()=='.tsv' else ','))
def files_at(root):
    return [p for p in root.rglob('*') if p.is_file() and not any(x in EXCLUDE for x in p.relative_to(root).parts) and p.suffix.lower()!='.pyc']
def manifest_at(root):
    path=root/'MANIFEST_SHA256.tsv';rows=table(path);bad=[]
    for r in rows:
        p=root/r['relative_path']
        if not p.is_file():bad.append('missing:'+r['relative_path']);continue
        b=canonical(p)
        if len(b)!=int(r['size_bytes']) or hashlib.sha256(b).hexdigest()!=r['sha256']:bad.append(r['relative_path'])
    actual={p.relative_to(root).as_posix() for p in files_at(root) if p!=path}
    listed={r['relative_path'] for r in rows}
    return not bad and actual==listed and len(listed)==len(rows),{'rows':len(rows),'bad':bad[:15],'unlisted':sorted(actual-listed)[:15],'missing':sorted(listed-actual)[:15]}

if not MANIFEST.is_file():raise SystemExit('Run python 2_code/build_manifest.py first')
required=['0_admin','1_data','2_code','3_results','4_figures','5_manuscript','6_release','7.Report','8_archive','8_reference','9_version']
add('numbered_folder_structure',all((ROOT/d/'README.md').is_file() for d in required),required)
ok,detail=manifest_at(ROOT);add('complete_current_manifest',ok,detail)
ok,detail=manifest_at(ARCH);add('coherent_unchanged_v1_4_archive',ok,detail)
allfiles=files_at(ROOT)
blocked=[p.relative_to(ROOT).as_posix() for p in allfiles if any(x.lower() in FORBIDDEN for x in p.relative_to(ROOT).parts)]
add('no_forbidden_private_or_runtime_trees',not blocked,blocked[:20])
path_hits=[];secret_hits=[];header_hits=[]
for p in allfiles:
    if p.suffix.lower() in TEXT or p.name in TEXT_NAMES:
        text=p.read_text(encoding='utf-8-sig',errors='replace')
        if p.name!='validate_public_release.py' and PRIVATE_PATH.search(text):path_hits.append(p.relative_to(ROOT).as_posix())
        if SECRET.search(text):secret_hits.append(p.relative_to(ROOT).as_posix())
    if p.suffix.lower() in {'.csv','.tsv'}:
        with p.open(encoding='utf-8-sig',newline='') as f:head=next(csv.reader(f,delimiter='\t' if p.suffix.lower()=='.tsv' else ','),[])
        if ID_HEADERS.intersection(x.lower() for x in head):header_hits.append(p.relative_to(ROOT).as_posix())
add('no_local_absolute_paths',not path_hits,path_hits)
add('no_embedded_credentials',not secret_hits,secret_hits)
add('no_participant_identifier_columns',not header_hits,header_hits)
restricted_names={'GSE84010_sample_characteristics.tsv','V4_S2_A2_top5_influential_records_R_RESTRICTED.tsv','V4_S2_A2_top5_influential_records_lifelines_RESTRICTED.tsv'}
restricted=[p.relative_to(ROOT).as_posix() for p in allfiles if p.name in restricted_names or p.suffix.lower()=='.docx']
add('private_inputs_and_author_documents_absent',not restricted,restricted)
contract=json.loads((ROOT/'0_admin/audit/source_hash_contract_v1.5.json').read_text(encoding='utf-8'))
bad=[n for n,r in contract.items() if not (ROOT/r['relative_path']).is_file() or sha(ROOT/r['relative_path'])!=r['raw_sha256'] or (ROOT/r['relative_path']).stat().st_size!=r['raw_bytes']]
add('16_frozen_aggregate_raw_byte_contracts',len(contract)==16 and not bad,bad)
data=ROOT/'1_data/aggregate/frozen_v1.5'
objects,ab,av,cross,primary=[table(data/n) for n in ['objects22.tsv','absolute23.tsv','avaglio10.tsv','cross13.tsv','primary27.tsv']]
add('complete_source_units',list(map(len,[objects,ab,av,cross,primary]))==[22,23,10,13,27],list(map(len,[objects,ab,av,cross,primary])))
add('original_use_and_roles',Counter(r['original_use_class'] for r in objects)=={'U1':14,'U2':8} and Counter(r['current_role'] for r in objects)=={'POPULATION_UNVERIFIED':10,'ROLE_REFRAMED':7,'TARGETED_REANALYSIS':2,'NOT_CURRENTLY_EVALUABLE':2,'IMPLEMENTATION_LIMITED':1},'Use-specific claims; not a field-wide sample')
add('cross_trial_current_eligibility',all(r['current_verified_strict_denominator_member'].lower()=='false' and r['current_strict_replication_proportion']=='NOT_ESTIMABLE' for r in cross) and sorted(Counter(r['dependency_cluster_id'] for r in cross).values())==[1,2,10],'Empty eligible set, not 0%')
add('absolute_delta_RD_arithmetic',all(abs(float(r['delta_rd'])-(float(r['rd_q75'])-float(r['rd_q25'])))<1e-12 for r in ab),'All 23 rows')
add('absolute_RD_and_probability_arithmetic',all(abs(float(r[f'rd_q{q}'])-(float(r[f'risk_t1_q{q}'])-float(r[f'risk_t0_q{q}'])))<1e-12 for r in ab for q in [25,75]) and all(0<=float(r[f'risk_t{t}_q{q}'])<=1 for r in ab for t in [0,1] for q in [25,75]),'92 bounded probabilities')
add('historical_bootstrap_accounting_and_primary_labels',all(int(r['bootstrap_requested'])==5000 and int(r['bootstrap_valid'])+int(r['bootstrap_invalid'])==5000 and r['primary_label_unchanged'].lower()=='true' and r['sensitivity_can_promote_primary_label'].lower()=='false' for r in ab),'No resampling performed by validator')
nom=[r for r in ab if float(r['bootstrap_sign_p'])<.05];rob=[r for r in ab if float(r['bootstrap_bh_q_within_family'])<.05]
add('absolute_supporting_status',len(nom)==1 and nom[0]['signature']=='Stromal_FARMER' and len(rob)==0 and sum(float(r['bootstrap_valid_fraction'])<.95 for r in ab)==1,'1 nominal, 0 family robust, 1 conditional technical interval; no clinical promotion')
qdiff=[]
families=sorted({r['multiplicity_family_id'] for r in ab})
for fam in families:
    rr=sorted([r for r in ab if r['multiplicity_family_id']==fam],key=lambda r:float(r['bootstrap_sign_p']))
    last=1
    for i in reversed(range(len(rr))):
        last=min(last,float(rr[i]['bootstrap_sign_p'])*len(rr)/(i+1))
        qdiff.append(abs(last-float(rr[i]['bootstrap_bh_q_within_family'])))
add('five_family_BH_arithmetic',len(families)==5 and max(qdiff)<1e-12,'Arithmetic check, not independent proof of sign-tail FDR calibration')
add('historical_primary_exponential_arithmetic',all(abs(math.exp(float(r['beta_interaction']))-float(r['effect_ratio']))<1e-6 for r in primary),'All 27 historical estimates')
add('AVAglio_shared_population_and_full_ladder',all(int(r['current_n'])==333 and int(r['current_events'])==260 for r in av if r['model_id'] in ['A2','A3']) and all({r['model_id'] for r in av if r['claim_id']==c}=={'A0','A1','A2','A3','A4'} for c in ['GBM_01','GBM_02']),'Both deposited labels; full specifications, no P-value selection')
r_rows=table(data/'V4_S2_independent_R_cox_results.tsv');rdiffs=[]
for r in r_rows:
    py=next(x for x in av if x['claim_id']==r['claim_id'] and x['model_id']=='A2')
    rdiffs.extend([abs(float(r['interaction_hr'])-float(py['current_interaction_hr'])),abs(float(r['interaction_p'])-float(py['current_interaction_p']))])
add('existing_independent_R_A2_agreement',len(r_rows)==2 and max(rdiffs)<1e-8,'Prior aggregate R fits read; no new R fit')
trio=table(ROOT/'3_results/current_v1.5/TRIO_all_24_conditional_feasible_states.tsv')
expected={(r,s) for r in range(30,39) for s in range(max(16,r-17),min(21,r-14)+1)}
observed={(int(r['randomized_n']),int(r['randomized_pcr'])) for r in trio}
add('TRIO_full_conditional_integer_states',len(trio)==24 and observed==expected and abs(min(float(r['raw_pcr_fraction']) for r in trio)-16/33)<1e-12 and abs(max(float(r['raw_pcr_fraction']) for r in trio)-.6)<1e-12,'Conditional compatibility, not a confidence interval or interaction bound')
display=table(ROOT/'3_results/current_v1.5/Table1_22objects_full_provenance_and_display_crosswalk.tsv')
by_id={r['claim_estimand_id']:r for r in display}
add('Table1_original_fields_conserved',len(display)==22 and all(all(by_id[r['claim_estimand_id']][k]==v for k,v in r.items()) for r in objects),'Only derived display fields added')
add('DOP_context_and_RCC04_conflict_explicit',next(r for r in display if r['legacy_claim_id']=='TNBC_03')['display_context']=='HER2− breast' and next(r for r in display if r['legacy_claim_id']=='RCC_04')['display_source_evidence']=='unresolved','Stable identifiers are not population definitions; no fabricated source resolution')
pairs=[('Additional_file_1_AVAglio_A0_A4.csv','Supplementary_Table_S1_AVAglio_A0_A4_10rows.tsv'),('Additional_file_2_cross_trial_eligibility.csv','Supplementary_Table_S2_cross_trial_historical_current_13rows.tsv'),('Additional_file_3_absolute_effect_sensitivity.csv','Supplementary_Table_S3_absolute_effect_current_role_23rows.tsv')]
add('lossless_supplementary_CSVs',all(table(ROOT/'3_results/supplementary_csv'/c)==table(ROOT/'3_results/current_v1.5'/t) for c,t in pairs),'10/13/23 rows')
figure_contract=json.loads((ROOT/'0_admin/audit/current_figure_formats_and_hashes.json').read_text(encoding='utf-8'))
add('21_published_figure_format_hashes',len(figure_contract)==21 and len({r['figure'] for r in figure_contract})==7 and all((ROOT/r['relative_path']).is_file() and sha(ROOT/r['relative_path'])==r['sha256'] for r in figure_contract),'4 main + 3 supplement, each PNG/PDF/SVG')
ms=ROOT/'5_manuscript/current_v1.5/QiTeng_RPv4_author_review_candidate_v1.5_20261012.md'
manuscript=ms.read_text(encoding='utf-8')
images=re.findall(r'!\[[^\]]*\]\(([^\)]+)\)',manuscript)
add('seven_real_manuscript_image_targets',len(images)==7 and all((ms.parent/x).is_file() for x in images),images)
first=[]
for m in re.finditer(r'\[(\d+(?:,\d+)*)\]',manuscript[:manuscript.index('## References')]):
    for n in map(int,m.group(1).split(',')):
        if n not in first:first.append(n)
refs=re.findall(r'^\d+\. (.+)$',manuscript[manuscript.index('## References'):manuscript.index('## Table and additional file legends')],re.M)
add('18_reference_identities_and_order',first==list(range(1,19)) and len(refs)==18 and len(set(refs))==18,'Order check is not independent clause-support certification')
prep=json.loads((ROOT/'6_release/v1.5_author_review/PUBLIC_PREPARATION_STATUS.json').read_text(encoding='utf-8'))
add('author_review_and_WPS_boundary',len(re.findall(r'\[\[[A-Z_]+\]\]',manuscript))==11 and prep['role']=='PUBLIC_AUTHOR_REVIEW_NOT_JOURNAL_SUBMISSION' and prep['new_WPS_manuscript_render'] is False and prep['journal_submission'] is False,'Eleven actual author fields remain; no inherited WPS PASS')
selected=json.loads((ROOT/'6_release/v1.5_author_review/SELECTED_PUBLIC_FILE_INVENTORY.json').read_text(encoding='utf-8'))
add('author_review_selected_file_inventory',selected['count']==31 and len(selected['files'])==31 and all((ROOT/r['relative_path']).is_file() and len(canonical(ROOT/r['relative_path']))==r['canonical_bytes'] and hashlib.sha256(canonical(ROOT/r['relative_path'])).hexdigest()==r['canonical_sha256'] for r in selected['files']),'31 selected assets; canonical LF text plus separately enforced raw figure contracts')
revision=json.loads((ROOT/'0_admin/audit/manuscript_revision_checks.json').read_text(encoding='utf-8'))
add('published_manuscript_identity',hashlib.sha256(canonical(ms)).hexdigest()==revision['published_canonical_LF_sha256'],'Image-path publication edit explicitly separated from private source audit hash')
broken=[]
for p in allfiles:
    if p.suffix.lower()!='.md' or ARCH in p.parents:continue
    text=re.sub(r'```.*?```','',p.read_text(encoding='utf-8-sig'),flags=re.S)
    for link in re.findall(r'\[[^\]]+\]\(([^\n\)]+)\)',text):
        target=unquote(link.strip('<> ').split('#')[0])
        if not target or re.match(r'^(?:https?|mailto):',target):continue
        if not (p.parent/target).exists():broken.append(p.relative_to(ROOT).as_posix()+':'+target)
add('active_Markdown_links_and_images_resolve',not broken,broken[:25])
published_recipe=ROOT/'2_code/reproduce_v1_5.py'
tree=ast.parse(published_recipe.read_text(encoding='utf-8'))
add('portable_reproduction_script_syntax',bool(tree.body),'No hard-coded private input paths; statistical inputs frozen')
passed=sum(c['pass'] for c in checks)
print(json.dumps({'status':'PASS' if passed==len(checks) else 'FAIL','checks_passed':passed,'checks_total':len(checks),'checks':checks},ensure_ascii=False,indent=2))
if passed!=len(checks):sys.exit(1)
