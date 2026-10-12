# Full workspace audit summary

Snapshot date: 2026-10-11.

The private workspace was rescanned before the current public synchronization.
Every traversed file was assigned a relative path, size, modification time,
SHA-256 hash, semantic role, initial release-risk class and format-aware
content status. Six Windows junctions were recorded but not followed to prevent
recursive double-counting. The new audit-output directory was excluded from its
own source snapshot.

| Item | Result |
|---|---:|
| Files hashed and classified | 64,977 |
| Total size | 3.749 GiB |
| Core files after dependency and Git exclusion | 9,235 |
| Core size | 2.125 GiB |
| Dependency/Git/build files | 55,742 |
| Core unreadable or corrupt files | 0 |
| ZIP files / CRC failures | 53 / 0 |
| PDFs / read errors / pages | 334 / 0 / 1,154 |
| DOCX files / read errors | 89 / 0 |
| XLSX/XLSM files / read errors / formula-error cells | 30 / 0 / 0 |
| CSV/TSV files / parsed data rows | 1,797 / 930,251 |
| Exact duplicate groups, all files | 10,611 |
| Potential duplicate storage, all files | 0.756 GiB |
| Core duplicate groups | 1,191 |
| Potential core duplicate storage | 202.7 MiB |
| Manifest files directly clean | 44/48 |

Thirteen parser alerts were confined to dependency test fixtures; no core
project file was unreadable or corrupt. Seven core secret-pattern candidates
were copies of code that reads an API key from the environment; no credential
value was embedded.

The four non-clean raw manifest checks were explained rather than silently
discarded: two Git working copies use canonical line-ending hashes, one copied
upstream manifest is a provenance-only record without its payload, and one is
an obsolete pre-patch historical manifest. The current public repository uses
its own canonical manifest and passes 19/19 fail-closed checks.

Exact duplicates were not deleted. Much of the duplication is intentional
version history, archived delivery material or bundled runtime content, so any
space reclamation must be a separate, recoverable, provenance-aware action.

The full path-level inventory, duplicate ledger and release-risk table remain
private because they expose local source locations and identity-review
candidates. This repository receives only the reviewed aggregate subset.
