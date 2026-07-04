# SpatialAIFlow — Repository Restructuring Walkthrough

## What Was Done

Transformed a single-notebook repository into a professional, scverse-tier open-source project structure. **No scientific code was modified, split, or rewritten.**

## Final Repository Tree

```
SpatialAIFlow/
├── .github/
│   ├── workflows/ci.yml              ← Lint + test across Python 3.9–3.12
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── FUNDING.yml
├── docs/
│   ├── api/.gitkeep
│   ├── tutorials/.gitkeep
│   └── conf.py                       ← Sphinx config with scverse intersphinx
├── notebooks/
│   └── SpatialAIFlow.ipynb           ← MOVED from root (37,109 bytes, unmodified)
├── src/spatialaiflow/
│   ├── __init__.py                   ← v0.1.0, full docstring
│   ├── preprocessing/__init__.py     ← §4–7: QC, filtering, normalization, HVG
│   ├── analysis/__init__.py          ← §8–12: PCA, clustering, markers, spatial stats
│   ├── annotation/__init__.py        ← §14, §19: manual + CellTypist annotation
│   ├── communication/__init__.py     ← §15: LIANA ligand-receptor analysis
│   ├── imaging/__init__.py           ← §16–17: H&E features, histology fusion
│   ├── ml/__init__.py                ← §23–24: Random Forest, Tangram deconvolution
│   ├── plotting/__init__.py          ← §3, §11, §13: visualization helpers
│   ├── io/__init__.py                ← §2, §22: data loading + export
│   └── utils/__init__.py             ← §1: constants, config, shared helpers
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   ← Fixture stub for synthetic AnnData
│   ├── test_preprocessing.py
│   ├── test_analysis.py
│   └── test_io.py
├── examples/
│   └── quickstart.py                 ← Future API usage example
├── data/.gitkeep
├── outputs/.gitkeep
├── assets/.gitkeep
├── .gitignore                        ← Python + data + IDE + model artifacts
├── .editorconfig                     ← UTF-8, LF, 4-space indent
├── .pre-commit-config.yaml           ← ruff + file hygiene hooks
├── LICENSE                           ← MIT
├── README.md                         ← Placeholder (to be written separately)
├── CONTRIBUTING.md                   ← Full contribution workflow
├── CODE_OF_CONDUCT.md                ← Contributor Covenant v2.1
├── CHANGELOG.md                      ← Keep a Changelog format
├── CITATION.cff                      ← CFF 1.2.0 machine-readable citation
├── pyproject.toml                    ← PEP 621 metadata + ruff + mypy + pytest
├── requirements.txt                  ← Core deps with optional section-specific
├── environment.yml                   ← Conda env (conda-forge + pip fallbacks)
└── Makefile                          ← lint, format, test, test-cov, docs, clean
```

## Design Decisions Explained

### Why `src/` layout?
The [PyPA-recommended src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) prevents accidental imports from the working directory during development. This is the standard for Scanpy, Squidpy, and the scverse ecosystem.

### Why 9 submodules?
Each submodule maps directly to a logical group of notebook sections:

| Submodule | Notebook Sections | Domain |
|---|---|---|
| `preprocessing` | §4–7 | QC → normalization → HVG |
| `analysis` | §8–12 | PCA → clustering → markers → spatial stats |
| `annotation` | §14, §19 | Manual + CellTypist labels |
| `communication` | §15 | LIANA ligand-receptor |
| `imaging` | §16–17 | H&E features + fusion |
| `ml` | §23–24 | RandomForest + Tangram |
| `plotting` | §3, §11, §13 | Spatial/UMAP visualization |
| `io` | §2, §22 | Load + export |
| `utils` | §1 | Config, constants |

This makes future refactoring straightforward: each notebook section has a clear home.

### Why `pyproject.toml` as single source of truth?
PEP 621 consolidates project metadata, build config, linting (ruff), type checking (mypy), testing (pytest), and coverage into one file. No `setup.py`, `setup.cfg`, `tox.ini`, or `.flake8` needed.

### Why optional dependency groups?
The notebook uses `pip install -q liana`, `pip install -q gseapy`, etc. inline. The `pyproject.toml` optional groups (`[communication]`, `[enrichment]`, `[annotation]`, `[deconvolution]`, `[ml]`) let users install only what they need: `pip install spatialaiflow[communication]` or `pip install spatialaiflow[all]`.

### Why both `requirements.txt` and `environment.yml`?
Different users prefer different workflows. `requirements.txt` for pip users, `environment.yml` for conda users. Both track the same dependencies.

## Verification

| Check | Result |
|---|---|
| Notebook moved to `notebooks/` | ✅ 37,109 bytes, identical |
| Notebook content unmodified | ✅ Not opened for editing |
| All 60+ files/directories created | ✅ Verified via recursive listing |
| No scientific code modified | ✅ Only infrastructure files created |
| No stray artifacts in repo root | ✅ Cleaned |

## What's Next (Not Done Yet)

These are natural follow-up tasks, **not** part of the current work:

1. **Write the README.md** — project description, badges, installation, quickstart
2. **Generate documentation** — populate `docs/` with API reference and tutorials
3. **Refactor notebook into package** — extract functions from notebook into `src/spatialaiflow/` submodules
4. **Add tests** — populate `tests/` with unit tests against the extracted functions
5. **Fill CITATION.cff** — add real author names, ORCIDs, and affiliations
