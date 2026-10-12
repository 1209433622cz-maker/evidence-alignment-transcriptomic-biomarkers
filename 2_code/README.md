# Portable public code

- `validate_public_release.py`: standard-library integrity/privacy/semantic checks.
- `build_manifest.py`: canonical-LF manifest; the separate raw-source contract is
  not rebuilt or weakened by this command.
- `reproduce_v1_5.py`: seven assemblies from aggregate sources; no model fits or
  bootstrap reruns. Default output `generated_v1_5/` is ignored by Git.

Run from the repository root. The local authoring pipeline, full private path
scanner and real-author document finalizer are not redistributed here. Their
curated results are preserved in `0_admin/audit/` and `7.Report/`. Historical code
is kept with its coherent v1.4 archive and is not the default current recipe.
