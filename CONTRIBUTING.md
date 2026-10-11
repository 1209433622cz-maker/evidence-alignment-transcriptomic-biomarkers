# Contributing

Contributions should preserve four boundaries:

1. do not change frozen primary labels in response to sensitivity results;
2. distinguish treated-arm response association from randomized treatment-effect modification;
3. retain uncertainty, dependency clusters and multiplicity context;
4. never upload participant-level or restricted data.

Before opening a pull request, run:

```bash
python scripts/build_manifest.py
python scripts/validate_public_release.py
```

Describe the scientific reason for each material change and identify every
affected claim, estimand, table or figure.
