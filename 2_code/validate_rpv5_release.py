"""Standard-library checks of the current RPv5 resource, not journal readiness."""
from pathlib import Path
import csv,hashlib,json,re,zipfile
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def add(name,ok,detail):checks.append({'name':name,'pass':bool(ok),'detail':detail})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
contract=json.loads((ROOT/'0_admin/audit/rpv5_public_asset_contract.json').read_text(encoding='utf-8'))
for group in ['aggregate_files','figure_files']:
    bad=[r['relative_path'] for r in contract[group] if not (ROOT/r['relative_path']).is_file() or sha(ROOT/r['relative_path'])!=r['raw_sha256'] or (ROOT/r['relative_path']).stat().st_size!=r['raw_bytes']]
    add(group+'_raw_byte_identity',not bad,bad)
expected={'1A_objects22':22,'1B_implementation27':27,'1C_source_only7':7,'2A_AVAglio10':10,'2B_AVA_recipe8':8,'3A_TRIO_counts6':6,'3B_TRIO_bounds9':9,'3C_TRIO_states24':24,'4A_primary27':27,'4B_cross13':13,'4C_absolute23':23,'4D_clause_support12':12,'5B_assertion22':22}
data=ROOT/'1_data/aggregate/reviewed_v1.6'
observed={k:len(table(data/f'Additional_file_{k}.tsv')) for k in expected}
add('13_companion_tables_210_rows',observed==expected and sum(observed.values())==210,observed)
ab=table(data/'Additional_file_4C_absolute23.tsv')
add('23_descriptive_not_confirmatory_sensitivities',all(r['review_fdr_control_established'].lower()=='false' and r['review_primary_promotion_allowed'].lower()=='false' and abs(float(r['delta_rd'])-float(r['rd_q75'])+float(r['rd_q25']))<1e-12 for r in ab),'No primary promotion or claimed confirmatory FDR calibration')
source=table(data/'figure2_source22_v1.6.tsv')
add('trial_specific_provenance_and_RCC04_polarity',len(source)==22 and all(r['provenance_code']=='TRIO:AS / CHER:LS' for r in source[:10]) and next(r for r in source if r['legacy_claim_id']=='RCC_04')['polarity']=='positive','Merged HER2 provenance is not original-assay execution')
cross=table(data/'Additional_file_4B_cross13.tsv')
add('current_replication_not_estimable',all(r['current_strict_replication_proportion']=='NOT_ESTIMABLE' for r in cross),'Not an estimated 0% rate')
man=ROOT/'5_manuscript/current_v1.6.2'
text=(man/'QiTeng_RPv5_manuscript_v1.6.2.md').read_text(encoding='utf-8')
add('truthful_declaration_limit',"Individual roles in study design" in text and 'have not yet been documented' in text and 'historical tool and model versions were not systematically recorded' in text and 'This study received no funding' in text and 'no competing interests' in text and '[[' not in text,'No invented CRediT, ethics ID, historical AI identity or DOI')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for stem,rows,media_count in [('QiTeng_RPv5_manuscript_v1.6.2',[22,22,10,6,9],4),('QiTeng_RPv5_supplement_v1.6.2',[27,13,23,27],3)]:
    with zipfile.ZipFile(man/(stem+'.docx')) as z:
        xml=ET.fromstring(z.read('word/document.xml'));actual=[len(t.findall('w:tr',ns))-1 for t in xml.findall('.//w:tbl',ns)]
        media=[n for n in z.namelist() if n.startswith('word/media/')]
        sensitive=[]
        for n in z.namelist():
            if n.endswith(('.xml','.rels')) and re.search(r'(?i)(?<![A-Za-z0-9])[A-Z]:[\\/]|Users[\\/]Administrator',z.read(n).decode('utf-8',errors='replace')):sensitive.append(n)
    add(stem+'_editable_tables_and_figures',actual==rows and len(media)==media_count,{'rows':actual,'images':len(media)})
    add(stem+'_no_local_package_paths',not sensitive,sensitive)
    add(stem+'_pdf_signature',(man/(stem+'.pdf')).read_bytes().startswith(b'%PDF-'),'WPS export; visual review separately recorded')
meta=json.loads((ROOT/'.zenodo.json').read_text(encoding='utf-8'))
add('software_metadata_authors_licence_version',meta['upload_type']=='software' and meta['version']=='1.6.2' and [c['orcid'] for c in meta['creators']]==['0009-0001-0072-5576','0009-0007-7648-4776'] and meta['license']=='mit','Component CC BY licence separately specified')
report={'checks':checks,'all_pass':all(c['pass'] for c in checks),'scope':'Public research resource; not journal-submission readiness'}
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['all_pass'] else 1)
