# Evidence alignment of transcriptomic biomarker claims in oncology

[![Validate public release](https://github.com/1209433622cz-maker/evidence-alignment-transcriptomic-biomarkers/actions/workflows/validate.yml/badge.svg)](https://github.com/1209433622cz-maker/evidence-alignment-transcriptomic-biomarkers/actions/workflows/validate.yml)

Current research resource: **RPv5 / v1.6.2-rpv5, 13 October 2026**. Four main figures, three supplementary figures, editable manuscripts and WPS-produced PDFs. This is an open code-and-aggregate-evidence resource with a manuscript candidate, **not an accepted journal article or a submission-readiness certification**. Individual author contributions must be recorded truthfully before journal submission. Zenodo publication is requested; no DOI is asserted before a published record is verified.

本库是经过披露边界审查的公开资源，不是私人工作区的全盘镜像。RPv5 为当前有限范围回顾性实证方法学研究；RPv4、A1R2 及旧稿保留为历史版本，不再作为当前执行指令。

## Scientific question

> Reproducible numbers do not, by themselves, establish defensible clinical inference.

We link original use and source conclusion, implementation provenance, analytic population, comparator and estimand. Two complementary cases show the practical consequence:

- **AVAglio:** recoverable population/model rules support a versioned, same-trial specification comparison.
- **TRIO-US B07:** unresolved participant-level phase in Arm 3 supports a documented limit on inference, not a guessed randomized subset.

This selected set is not a systematic sample of oncology. We do not estimate field-wide failure rates, train a new classifier, optimize cut-points, certify original-assay execution or claim independently validated utility of the audit workflow. Historical outcomes were visible before the amendment; the whole project is not retrospectively called prospectively preregistered.

## Start here

1. [Current manuscript MD](5_manuscript/current_v1.6.2/QiTeng_RPv5_manuscript_v1.6.2.md), [DOCX](5_manuscript/current_v1.6.2/QiTeng_RPv5_manuscript_v1.6.2.docx), [WPS PDF](5_manuscript/current_v1.6.2/QiTeng_RPv5_manuscript_v1.6.2.pdf).
2. [Supplement MD](5_manuscript/current_v1.6.2/QiTeng_RPv5_supplement_v1.6.2.md), [DOCX](5_manuscript/current_v1.6.2/QiTeng_RPv5_supplement_v1.6.2.docx), [WPS PDF](5_manuscript/current_v1.6.2/QiTeng_RPv5_supplement_v1.6.2.pdf).
3. [Reviewed aggregate tables and chronology](1_data/aggregate/reviewed_v1.6/), [publication/licensing boundaries](LICENSING.md).
4. [Current release record](7.Report/485_RPv5_author_declarations_public_resource_release_20261013.md), [asset hash contract](0_admin/audit/rpv5_public_asset_contract.json).
5. [Historical RPv4 proposal](0_admin/protocol/RPv4_Full_Research_Proposal_20261010.md) and [version ledger](9_version/README.md). RPv5 operational scope is the bounded correction/integration study described in the current manuscript, not the historical systematic-search route.

## Results and interpretation

| Unit or case | Current record and permitted interpretation |
| --- | --- |
| Objects | 22 core claim–estimand objects from 28 historical candidates; 15 locally evaluated, 7 source-only |
| Implementations | 27 trial contexts, not 27 independent claims; TRIO author-score reuse differs from CHER-LOB locally precomputed source-compatible scores with incompletely recovered generation |
| Historical models | All 27 primary and 23 binary absolute-effect records retained unchanged; historical labels are not current validation verdicts |
| AVAglio | 349 expression-evaluable, 339 IDH1-wild-type, 333 fixed complete cases; eight A0–A3 paired-engine estimates. A4 penalty comparison not currently cross-engine verified |
| Shared-set AVAglio | Phillips interaction HR 0.612 unadjusted vs 0.516 adjusted; Verhaak 0.513 vs 0.460 on the same 333 people. Not independent validation or proof that adjustment removed confounding |
| TRIO | Arms 1/2 randomized by design; individual Arm 3 phase unverified. Conditional constraints: 24 integer states, 30–38 randomized participants, 48.5–60.0% raw pCR. Not patient mappings, CIs, causal bounds or interaction bounds |
| Cross-trial record | 13 historical units in 3 dependency clusters; current strict replication proportion **NOT_ESTIMABLE**, not 0%, 0/13, 0/0 or 0/3 |
| Absolute sensitivity | Historical sign-tail/BH transformations are descriptive; null calibration and confirmatory FDR control were not established. No sensitivity promotes a primary label. CHER-LOB ESR1_DESMEDT retains 4,736/5,000 conditional interval qualification |

## Repository map

| Folder | Contents |
| --- | --- |
| `0_admin` | Scope/protocols, publication boundaries and identity/hash contracts |
| `1_data` | Aggregate-only historical/reviewed tables; no participant rows or raw expression |
| `2_code` | Validators, manifest builder, aggregate figure recipe, official-input AVAglio reproduction, tested requirements |
| `3_results` | Aggregate AVAglio recipe outputs and historical result records |
| `4_figures` | Fig1–Fig8 filing folders: current Fig1–4 are main; Fig5–7 are S1–S3; Fig8 reserved/historical, not an eighth current figure |
| `5_manuscript` | Current v1.6.2 MD/DOCX/PDF; old drafts separately labelled |
| `6_release` | Scope and prior public receipts; source archive attached on GitHub Releases |
| `7.Report` | Disclosure-safe action/audit records; not private logs copied wholesale |
| `8_archive` | Preserved historical public snapshots |
| `8_reference` | Source index/literature metadata; no third-party full-text redistribution |
| `9_version` | Version ledger; preserved prior public README is in archive |

Folder numbers are filing identifiers; captions determine main/supplementary status. Each current assembly has PNG (600-dpi source), PDF and SVG. The main embeds actual images and editable tables; supplement tables retain all 27/13/23/27 rows. Prior v1.5 figures and frozen aggregates remain unchanged.

## Reproduction

From the repository root, Python 3.12+ for dependency-free validators:

```bash
python 2_code/validate_public_release.py
python 2_code/validate_rpv5_release.py
```

These check integrity, privacy and reporting consistency, not author identity, clinical validity or original-assay execution. The first also checks preserved v1.5/v1.4 regression contracts; historical labels do not override RPv5 interpretation.

Use a separate virtual environment for the current aggregate figure recipe. Tested direct requirements are not a complete transitive lock:

```bash
python -m pip install -r 2_code/requirements-rpv5-tested.txt
python 2_code/reproduce_rpv5_figures.py --output-dir generated_rpv5 --font Arial
```

Four assemblies are redrawn and three disclosed unchanged assemblies copied. No model or bootstrap is fitted. Arial must be installed for reviewed typography. An explicit alternative font is recorded and requires new visual checks, not a byte-identity claim. A new ignored output directory is required; published inputs and existing output directories cannot be overwritten. PDF timestamps/library versions may change bytes. Geometry success is not visual certification.

AVAglio A0–A3 reproduction uses an official GEO series matrix, **not bundled**. Obtain it under source terms:

```bash
python 2_code/ava_reproduce.py --help
python 2_code/ava_reproduce.py --series-matrix /path/to/GSE84010_series_matrix.txt.gz --frozen-ladder 1_data/aggregate/frozen_v1.5/avaglio10.tsv --output-dir /path/to/new-ava-output
```

Optional download mode requires the explicit no-redistribution acknowledgement in `--help`. Downloaded inputs must remain outside public archives. Deposited subtype labels are reused; the platform-adapted assay is not reconstructed. The historical optimizer qualification remains explicit rather than forcing estimates to a chosen threshold. Aggregate outputs do not export participant IDs.

## Authors and declarations

Zhi Chen (first author), ORCID [0009-0001-0072-5576](https://orcid.org/0009-0001-0072-5576); Teng Qi (corresponding author), ORCID [0009-0007-7648-4776](https://orcid.org/0009-0007-7648-4776). School of Medicine, The Chinese University of Hong Kong, Shenzhen, China. Supplied title: MSc student in Bioinformatics. Correspondence: tengqi@link.cuhk.edu.cn.

Information, material approval, originality and exclusive-submission statements are confirmed through the authors' representative. No conflicts, funding or acknowledgements declared. No additional ethics approval required according to the authors' determination for this secondary study; no committee ID or exemption certificate invented. These declarations do not confer rights over third-party inputs.

**Individual contributions cannot be established by random assignment.** The candidate records shared review/approval only; actual individual work history must be documented before journal submission. No journal submission or cover-letter sending has occurred.

OpenAI Codex (OpenAI; accessed 13 October 2026) assisted current file/code checks, organization and language refinement. Historical generative-AI tool/model details were not systematically recorded. We disclose this limitation, not a guessed GPT version or a claim that only Codex was used. Human authors retain verification and interpretation responsibility; AI is not an author.

## Licences, citation and archive

Code: [MIT](LICENSE). Original documents, figures, manuscript candidate and derived aggregate tables: [CC BY 4.0](LICENSE-DATA.md); see [component-level terms](LICENSING.md). Existing attribution is preserved. Third-party participant inputs, expression matrices, papers and assay resources retain their original terms and are excluded; this project cannot grant their reuse rights.

[CITATION.cff](CITATION.cff) describes a software/research resource, not a published journal paper. [Zenodo metadata](.zenodo.json) uses matching authors/title/version. Zenodo uses `.zenodo.json` when both files exist. Its primary software licence field is MIT; the component-level CC BY licence is explicit in description and documentation. A resource DOI will not mean journal acceptance or clinical validation.

## Finite next step

Verify archive publication and DOI linking, record factual individual author contributions, then finalize target-journal formatting and the author upload check. No object-set expansion, repeated unchanged bootstrap, guessed TRIO phase, restored strict rate or new systematic-review prerequisite. Actual journal submission remains separately authorized.
