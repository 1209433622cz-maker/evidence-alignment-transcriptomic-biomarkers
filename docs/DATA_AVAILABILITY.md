# Data availability and redistribution boundary

This repository contains only aggregate analysis outputs, trial/claim-level
registries, templates, figures and code. It deliberately excludes:

- participant-, patient-, subject- or sample-level analysis matrices;
- sample-linkage files and individual outcomes;
- controlled-access dbGaP/EGA material;
- author rosters, signatures, contact details and conflicts-of-interest records;
- API credentials and local environment files;
- third-party article PDFs and bulk download archives.

The statistical reference scripts expect users to obtain source datasets from
their lawful original repositories and to respect each study's terms. Dataset
accessions and trial names in the aggregate tables are provenance pointers, not
redistributed datasets.

The public bootstrap file contains one row per model/replicate, validity status
and aggregate `ΔRD`; it contains no participant identifiers or resampled index
vectors.

The RPv4 S0/S1 update publishes only the aggregate 22-object role ledger,
model-stage registry, lineage table, preflight checklist and validation
summaries. The 349-row AVAglio analysis input is not redistributed. Its identity
is bound internally by checksum; the public model registry contains no
participant or sample identifiers. The public TRIO boundary reports only
aggregate counts and does not infer assignment phase for any individual row.

The S2–S6H1 update adds aggregate AVAglio coefficients and diagnostics,
design-level TRIO identifiability bounds, current manuscript tables, four main
figures and the Markdown manuscript candidate. It excludes the restricted
top-influence record listings, the WPS render and page rasters, and all source
files that contain participant, author, contact, signature or accountability
values. The public S6H1 ledger records only decision status and the categories
still requiring real author input.
