"""Generate the educational SpatialAIFlow notebook."""
import json, os

def md(text):
    lines = text.strip("\n").split("\n")
    if len(lines) == 1:
        return {"cell_type": "markdown", "metadata": {}, "source": [lines[0]]}
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in lines[:-1]] + [lines[-1]]}

def code(text):
    lines = text.strip("\n").split("\n")
    if len(lines) == 1:
        return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [lines[0]]}
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [l + "\n" for l in lines[:-1]] + [lines[-1]]}

cells = []

# ═══════════════════════════════════════════════════════════════════════
# TITLE & OVERVIEW
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""# 🧬 SpatialAIFlow — Spatial Transcriptomics Analysis Pipeline

<div align="center">

**A complete, reproducible, end-to-end spatial transcriptomics course notebook**

*From raw Visium data to biological insight — in a single pipeline*

</div>

---

## About This Notebook

This notebook is designed as a **self-contained educational resource** for learning spatial transcriptomics analysis. It uses the publicly available **10x Genomics Visium** *Breast Cancer Block A, Section 1* dataset as a working example to walk through every major step of a modern spatial transcriptomics workflow.

By the end of this notebook, you will have produced:

| Output | Description |
|--------|-------------|
| 🧹 QC-filtered data | Quality-controlled, normalized expression matrix |
| 🗺️ Spatial clusters | Unsupervised Leiden clusters mapped onto tissue |
| 🏷️ Cell-type labels | Both manual and automated (CellTypist) annotations |
| 📊 Spatial statistics | Neighborhood enrichment, co-occurrence, Moran's I |
| 🔗 Communication map | Ligand–receptor interactions via LIANA |
| 🔬 Histology features | Image-derived features fused with transcriptomics |
| 🤖 ML classifier | Trained Random Forest cell-type predictor |
| 🧩 Deconvolution map | Multi-omics spatial deconvolution via Tangram |

> **📌 Scope Note**
> This notebook documents and teaches a complete analytical workflow. No analysis step has been added, removed, or reordered from the original pipeline. Parameters and thresholds reflect the choices appropriate for this specific dataset.

---

## Prerequisites

| Requirement | Level |
|-------------|-------|
| **Python** | Intermediate — comfortable with NumPy, pandas, matplotlib |
| **Biology** | Basic molecular biology — what genes, RNA, and cells are |
| **Statistics** | Introductory — distributions, hypothesis testing, PCA conceptually |
| **Spatial Biology** | None — this notebook will teach you |

---

## How to Use This Notebook

Each section follows a consistent pedagogical structure:

1. **🎯 Learning Objectives** — what you will be able to do after this section
2. **🧬 Biological Background** — *why* researchers perform this analysis
3. **💻 Computational Background** — *how* the algorithm works
4. **📊 Expected Output** — what to look for before running the code
5. **🖥️ Code** — the executable analysis (kept concise and readable)
6. **🔍 Result Interpretation** — how to read the output biologically
7. **⚠️ Common Mistakes** — pitfalls to avoid
8. **📋 Section Summary** — key takeaways in bullet-point form
9. **✏️ Exercises** — practice questions (conceptual + coding)
10. **📚 Further Reading** — papers, documentation, and reviews

> **💡 Tip:** Run cells sequentially from top to bottom. Each section depends on the outputs of previous sections."""))

# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 📑 Table of Contents

### Part I — Foundation
1. [Environment Setup](#1.-Environment-Setup)
2. [Data Loading](#2.-Data-Loading)
3. [Raw Data Visualization](#3.-Raw-Data-Visualization)

### Part II — Quality Control & Preprocessing
4. [Quality Control (QC)](#4.-Quality-Control-(QC))
5. [Filtering Low-Quality Spots](#5.-Filtering-Low-Quality-Spots)
6. [Normalization & Log Transformation](#6.-Normalization-&-Log-Transformation)
7. [Feature Selection (Highly Variable Genes)](#7.-Feature-Selection-(Highly-Variable-Genes))

### Part III — Unsupervised Analysis
8. [Dimensionality Reduction (PCA)](#8.-Dimensionality-Reduction-(PCA))
9. [Clustering (Leiden)](#9.-Clustering-(Leiden))
10. [Marker Gene Identification](#10.-Marker-Gene-Identification)
11. [Spatial Expression of Key Marker Genes](#11.-Spatial-Expression-of-Key-Marker-Genes)
12. [Spatial Neighborhood Enrichment](#12.-Spatial-Neighborhood-Enrichment)
13. [UMAP Embedding](#13.-UMAP-Embedding)

### Part IV — Cell-Type Annotation & Communication
14. [Manual Cell-Type Annotation](#14.-Manual-Cell-Type-Annotation)
15. [Ligand–Receptor Communication (LIANA)](#15.-Ligand–Receptor-Communication-(LIANA))

### Part V — Multi-Modal & Advanced Analysis
16. [Histology-Based Image Feature Extraction](#16.-Histology-Based-Image-Feature-Extraction)
17. [Fusing Histology and Transcriptomics](#17.-Fusing-Histology-and-Transcriptomics)
18. [Pathway Enrichment Analysis (GSEA)](#18.-Pathway-Enrichment-Analysis-(GSEA))
19. [Automated Cell-Type Annotation (CellTypist)](#19.-Automated-Cell-Type-Annotation-(CellTypist))
20. [Spatial Co-occurrence & Autocorrelation](#20.-Spatial-Co-occurrence-&-Autocorrelation)
21. [Cell Trajectory Analysis (PAGA)](#21.-Cell-Trajectory-Analysis-(PAGA))

### Part VI — Export & Machine Learning
22. [Exporting Processed Outputs](#22.-Exporting-Processed-Outputs)
23. [Machine Learning Cell-Type Classifier](#23.-Machine-Learning-Cell-Type-Classifier)
24. [Multi-omics Spatial Deconvolution (Tangram)](#24.-Multi-omics-Spatial-Deconvolution-(Tangram))"""))

# ═══════════════════════════════════════════════════════════════════════
# PART I: FOUNDATION
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

# Part I — Foundation

> *Setting up the computational environment and loading spatial transcriptomics data*"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: ENVIRONMENT SETUP
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 1. Environment Setup

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Identify the core Python libraries used in spatial transcriptomics analysis
- Explain why reproducibility settings (random seeds, verbosity) matter
- Set up a consistent computational environment for a bioinformatics pipeline
- Understand the role of each library in the analysis workflow

---

### 🧬 Biological Context

Spatial transcriptomics experiments generate complex, high-dimensional datasets that combine gene expression measurements with spatial coordinates and tissue images. Analyzing these datasets requires a carefully orchestrated stack of computational tools that span:

- **Data handling** — storing and manipulating expression matrices with thousands of genes across thousands of spatial locations
- **Statistical analysis** — normalizing, clustering, and testing for differential expression
- **Spatial analysis** — leveraging the physical positions of measurements on tissue
- **Visualization** — overlaying results on tissue images for biological interpretation

No single tool does everything. The modern spatial transcriptomics workflow is built on the **scverse** ecosystem — an open-source community of interoperable tools centered around the `AnnData` data structure.

---

### 💻 Computational Background

| Library | Role | Docs |
|---------|------|------|
| **NumPy** | Numerical computing (arrays, linear algebra) | [numpy.org](https://numpy.org) |
| **pandas** | Tabular data manipulation | [pandas.pydata.org](https://pandas.pydata.org) |
| **Matplotlib** | Plotting and visualization | [matplotlib.org](https://matplotlib.org) |
| **Scanpy** | Single-cell/spatial analysis (QC, PCA, clustering, markers) | [scanpy.readthedocs.io](https://scanpy.readthedocs.io) |
| **Squidpy** | Spatial-specific analysis (spatial graphs, image features) | [squidpy.readthedocs.io](https://squidpy.readthedocs.io) |

**Why set a random seed?** Many algorithms in this pipeline (Leiden clustering, UMAP, train/test splits) include stochastic steps. Setting `RANDOM_STATE = 42` ensures that anyone re-running this notebook gets identical results — a cornerstone of reproducible science.

**Why suppress warnings?** Scientific Python libraries emit many informational warnings (e.g., deprecation notices) that clutter output without affecting results. We silence them for readability but recommend re-enabling them when debugging.

> **💡 Tip:** Domain-specific libraries (LIANA, gseapy, CellTypist, Tangram, scikit-learn) are installed and imported in the sections where they are first used. This keeps the top of the notebook lean and makes dependencies explicit."""))

cells.append(md(r"""### 📊 Expected Output

No visible output — this cell loads libraries, sets the random seed, and configures display settings. If it runs without errors, the environment is ready."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Core scientific stack for spatial transcriptomics analysis
# ──────────────────────────────────────────────────────────────────────
import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scanpy as sc
import squidpy as sq

warnings.filterwarnings("ignore")

# Reproducibility: fix the random seed for all stochastic steps
RANDOM_STATE = 42
sc.settings.verbosity = 1          # 0 = errors, 1 = warnings, 2 = info, 3 = hints
sc.settings.set_figure_params(dpi=100, facecolor="white")

# Central configuration — avoids hard-coding sample names in multiple cells
SAMPLE_ID = "V1_Breast_Cancer_Block_A_Section_1"
OUTPUT_DIR = "SpatialAIFlow_Outputs" """))

cells.append(md(r"""### ⚠️ Common Mistakes

> **Version conflicts:** Scanpy and Squidpy must be compatible versions. If you encounter import errors, check the [scverse version compatibility table](https://scanpy.readthedocs.io/en/stable/).

> **Missing dependencies:** If `import squidpy` fails, install it with `pip install squidpy`. The same applies to all domain-specific libraries used later.

> **Forgetting the random seed:** Without `RANDOM_STATE`, clustering and embedding results will differ between runs, making the analysis non-reproducible.

---

### 📋 Section Summary

- The pipeline uses **six core libraries**: NumPy, pandas, Matplotlib, Scanpy, Squidpy, and AnnData (imported via Scanpy)
- A **fixed random seed** (`42`) ensures full reproducibility across all stochastic steps
- **Verbosity is set to 1** (warnings only) to keep output clean during teaching
- **Figure parameters** are configured for white backgrounds at 100 DPI
- Domain-specific tools are imported later, **near the code that uses them**

---

### ✏️ Exercises

1. **Conceptual:** What would happen if two researchers ran this notebook with different random seeds? Which steps would produce different results?
2. **Coding:** Print the versions of Scanpy and Squidpy (`sc.__version__`, `sq.__version__`). Are they compatible according to the scverse documentation?
3. **Conceptual:** Why is it good practice to define `SAMPLE_ID` and `OUTPUT_DIR` as constants at the top rather than hard-coding strings in each cell?
4. **Coding:** Change `sc.settings.verbosity` to `3` and re-run the next few sections. What additional information do you see?

---

### 📚 Further Reading

- Wolf, F. A., Angerer, P. & Theis, F. J. *SCANPY: large-scale single-cell gene expression data analysis.* Genome Biol. **19**, 15 (2018). [DOI](https://doi.org/10.1186/s13059-017-1382-0)
- Palla, G. et al. *Squidpy: a scalable framework for spatial omics analysis.* Nat. Methods **19**, 171–178 (2022). [DOI](https://doi.org/10.1038/s41592-021-01358-2)
- [Scanpy tutorials](https://scanpy.readthedocs.io/en/stable/tutorials.html)
- [Squidpy tutorials](https://squidpy.readthedocs.io/en/stable/tutorials.html)
- [scverse ecosystem](https://scverse.org/)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: DATA LOADING
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 2. Data Loading

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Describe how the 10x Genomics Visium platform generates spatial transcriptomics data
- Explain the structure of an `AnnData` object and its key components
- Load a public Visium dataset using Squidpy
- Compute basic per-spot summary statistics

---

### 🧬 Biological Background

**What is spatial transcriptomics?** Traditional RNA sequencing (bulk or single-cell) measures gene expression but loses the spatial context — we know *what* genes are active, but not *where* in the tissue. Spatial transcriptomics preserves this location information.

**The 10x Visium platform** works by placing a thin tissue section onto a glass slide printed with ~5,000 barcoded spots, each ~55 μm in diameter. When mRNA is released from the tissue, it binds to the nearest spot's barcodes, creating a spatial gene expression map. Simultaneously, the tissue is stained with Hematoxylin & Eosin (H&E), producing a histology image that can be overlaid with the expression data.

**The dataset used here** — *Breast Cancer Block A, Section 1* — is a publicly available Visium dataset from 10x Genomics. It captures the spatial gene expression profile of a breast cancer tumor section, containing a mix of tumor cells, immune infiltrates, stromal tissue, and normal epithelium.

> **📌 Key Point:** Each Visium "spot" typically captures RNA from **multiple cells** (5–30 cells per spot, depending on tissue density). This is a fundamental limitation that motivates deconvolution methods covered in Section 24.

---

### 💻 Computational Background

**AnnData** (Annotated Data) is the central data structure in the scverse ecosystem. It stores everything about the dataset in one object:

```
adata.X         →  Expression matrix (spots × genes)
adata.obs       →  Per-spot metadata (QC metrics, cluster labels, cell types)
adata.var       →  Per-gene metadata (gene names, variability flags)
adata.obsm      →  Multi-dimensional spot annotations (spatial coordinates, embeddings)
adata.uns       →  Unstructured metadata (spatial images, color palettes)
```

The expression matrix `adata.X` is typically a **sparse matrix** because most genes are not expressed in most spots — storing only the non-zero values saves memory.

**Total UMI counts** (Unique Molecular Identifiers) per spot represent the total number of RNA molecules detected. This serves as a rough proxy for how much biological material was captured at each spatial location."""))

cells.append(md(r"""### 📊 Expected Output

A printed message confirming the dataset dimensions: approximately **3,798 spots × 33,538 genes** (exact numbers depend on the dataset version)."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Download and load the breast cancer Visium dataset
# ──────────────────────────────────────────────────────────────────────
print("Downloading the breast cancer Visium dataset...")
adata_bc = sq.datasets.visium(SAMPLE_ID)

# Ensure gene names are unique (duplicates can break downstream operations)
adata_bc.var_names_make_unique()

# Total UMI counts per spot — a proxy for capture quality
adata_bc.obs["total_counts"] = np.asarray(adata_bc.X.sum(axis=1)).flatten()

print(f"Loaded {adata_bc.n_obs} spots × {adata_bc.n_vars} genes.")"""))

cells.append(md(r"""### 🔍 Result Interpretation

The output shows the dataset dimensions. A typical Visium experiment captures:

- **~3,000–5,000 spots** depending on tissue size and coverage
- **~20,000–36,000 genes** depending on the reference genome

The `total_counts` column we just created will be our first quality metric — spots with very low counts may indicate empty areas or poor capture, while very high counts suggest high-quality tissue regions.

---

### ⚠️ Common Mistakes

> **Not making variable names unique:** Gene annotations sometimes contain duplicate symbols. If not resolved, downstream operations (e.g., subsetting by gene name) may silently return incorrect results. Always call `adata.var_names_make_unique()` immediately after loading.

> **Assuming one spot = one cell:** Each Visium spot covers ~55 μm and captures RNA from multiple cells. Treat spots as *spatial neighborhoods*, not single cells.

---

### 📋 Section Summary

- The 10x Visium platform generates spatially resolved gene expression data at ~55 μm resolution
- Data is loaded into an **AnnData** object — the standard container in the scverse ecosystem
- The expression matrix is **sparse** (most entries are zero)
- `total_counts` summarizes sequencing depth per spot and will be used for QC
- Each spot may contain RNA from **multiple cells**

---

### ✏️ Exercises

1. **Conceptual:** Why is spatial information lost in standard single-cell RNA sequencing? What biological questions can spatial transcriptomics answer that scRNA-seq cannot?
2. **Coding:** Inspect the AnnData object by printing `adata_bc`. What information is shown?
3. **Coding:** Examine the spatial coordinates stored in `adata_bc.obsm['spatial']`. What are the dimensions? What do the two columns represent?
4. **Conceptual:** Why does the expression matrix use a sparse format? Estimate the memory savings compared to a dense matrix for this dataset.
5. **Coding:** What is the median `total_counts` value? What is the range (min to max)?

---

### 📚 Further Reading

- Ståhl, P. L. et al. *Visualization and analysis of gene expression in tissue sections by spatial transcriptomics.* Science **353**, 78–82 (2016). [DOI](https://doi.org/10.1126/science.aaf2403)
- [10x Genomics Visium documentation](https://www.10xgenomics.com/products/spatial-gene-expression)
- [AnnData documentation](https://anndata.readthedocs.io/en/stable/)
- Marx, V. *Method of the year: spatially resolved transcriptomics.* Nat. Methods **18**, 9–14 (2021). [DOI](https://doi.org/10.1038/s41592-020-01033-y)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: RAW DATA VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 3. Raw Data Visualization

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Visualize gene expression data overlaid on tissue histology images
- Use total UMI counts as a first quality indicator
- Interpret spatial expression patterns relative to tissue morphology
- Identify potential artifacts or quality issues from raw data plots

---

### 🧬 Biological Background

Before performing any filtering or normalization, it is critical to **visualize the raw data**. This serves as the first sanity check of the experiment:

- **Tissue regions** should show higher total counts than background/empty regions
- The **spatial pattern of counts** should roughly follow tissue density visible in the H&E image
- **Artifacts** (bubbles, tears, folds in the tissue section) may appear as spatial anomalies in count distribution

This step is analogous to looking at raw sequencing quality reports before alignment — it builds intuition about the data before any statistical processing.

---

### 💻 Computational Background

`sq.pl.spatial_scatter()` overlays per-spot values (here, total counts) onto the tissue image as a colored scatter plot. Key parameters:

| Parameter | Purpose |
|-----------|---------|
| `color` | The variable to map to color (from `adata.obs` or `adata.var_names`) |
| `cmap` | Colormap — `"magma"` is perceptually uniform and colorblind-friendly |
| `size` | Dot size relative to spot spacing |
| `alpha` | Dot transparency (allows the H&E image to show through) |
| `img_alpha` | Transparency of the background tissue image |"""))

cells.append(md(r"""### 📊 Expected Output

A spatial scatter plot showing the breast cancer tissue section with each spot colored by its total UMI count. The H&E histology image should be visible underneath. Tissue-covered regions should appear brighter (higher counts), while background/empty spots should be near zero."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# First look: total counts overlaid on the tissue image
# ──────────────────────────────────────────────────────────────────────
sq.pl.spatial_scatter(
    adata_bc,
    color="total_counts",
    title="Breast Cancer Tissue — Total Counts per Spot",
    cmap="magma",
    size=0.8,
    shape="circle",
    alpha=0.85,
    img_alpha=1.0,
    figsize=(8, 8),
)
plt.axis("off")
plt.show()"""))

cells.append(md(r"""### 🔍 Result Interpretation

In a successful Visium experiment, you should observe:

- **High counts** (bright colors) concentrated over the tissue area
- **Low/zero counts** (dark colors) in spots that fall outside the tissue boundary
- **Spatial structure** — different tissue compartments (tumor core, stroma, immune infiltrates) may already show count differences

For this breast cancer dataset, the tumor-dense regions typically show higher counts because tumor cells are often highly transcriptionally active. The surrounding stroma may show moderate counts, and empty slide regions will be near zero.

> **📌 What to watch for:** If you see bright spots scattered randomly over empty regions, it could indicate contamination or a barcode assignment error. If the entire tissue appears uniformly dark, sequencing depth may be too low.

---

### ⚠️ Common Mistakes

> **Skipping raw data visualization:** Jumping straight to filtering without looking at the raw data risks missing systematic artifacts (tissue folds, air bubbles, slide edge effects).

> **Using a non-perceptually-uniform colormap:** Colormaps like `"jet"` or `"rainbow"` create visual artifacts where none exist in the data. Always prefer `"magma"`, `"viridis"`, or `"inferno"` for continuous data.

---

### 📋 Section Summary

- Raw data visualization is the **first sanity check** before any preprocessing
- Total UMI counts should correlate with tissue structure visible in the H&E image
- The `"magma"` colormap is perceptually uniform and colorblind-friendly
- Spatial scatter plots overlay quantitative data directly on tissue morphology
- Anomalies at this stage indicate experimental artifacts, not biological signal

---

### ✏️ Exercises

1. **Conceptual:** Why might tumor regions show higher total counts than stromal regions? Think about the relationship between cell density, transcriptional activity, and UMI capture.
2. **Coding:** Replace `"magma"` with `"viridis"` and re-plot. Which colormap makes it easier to distinguish tissue from background?
3. **Coding:** Try changing `alpha` to `0.3` and `1.0`. How does transparency affect the ability to correlate expression with tissue morphology?
4. **Conceptual:** If a tissue section had a fold (doubled-over tissue), how would that appear in this plot?

---

### 📚 Further Reading

- [Squidpy spatial plotting tutorial](https://squidpy.readthedocs.io/en/stable/auto_tutorials/tutorial_visium_hne.html)
- [Choosing colormaps in Matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
- Ramsay, E. C. *Colorblind-friendly visualization in bioinformatics.* (2020)"""))

# ═══════════════════════════════════════════════════════════════════════
# PART II: QUALITY CONTROL & PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

# Part II — Quality Control & Preprocessing

> *Filtering noise, normalizing signal, and selecting informative features*"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 4: QUALITY CONTROL
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 4. Quality Control (QC)

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain why quality control is essential before any biological analysis
- Define three key QC metrics: genes detected, total counts, and mitochondrial fraction
- Interpret violin plots of QC metric distributions
- Identify spots that may represent damaged or empty tissue

---

### 🧬 Biological Background

Not all spots in a Visium experiment contain high-quality data. Low-quality spots arise from:

| Issue | Biological Cause | QC Signature |
|-------|-----------------|--------------|
| **Empty spots** | Spot falls outside tissue boundary | Very low gene count and total counts |
| **Damaged tissue** | Necrosis, mechanical damage during sectioning | High mitochondrial fraction |
| **Debris** | Loose cells or ambient RNA contamination | Moderate counts but abnormal gene profiles |

**Mitochondrial genes** (prefixed `MT-` in human) are a particularly important indicator. When cells are damaged, their cytoplasmic mRNA degrades faster than mitochondrial mRNA (which is protected by the double membrane of mitochondria). This means a high percentage of mitochondrial reads signals **poor cell quality**, not high mitochondrial activity.

---

### 💻 Computational Background

Scanpy's `sc.pp.calculate_qc_metrics()` computes three key metrics in a single pass:

| Metric | Column Name | Interpretation |
|--------|-------------|----------------|
| **Genes detected** | `n_genes_by_counts` | Number of unique genes with ≥1 read |
| **Total counts** | `total_counts` | Sum of all UMI counts (sequencing depth) |
| **Mitochondrial %** | `pct_counts_mt` | Fraction of reads from MT- genes |

These metrics are visualized as **violin plots** — a combination of a box plot and a kernel density estimate that shows the full distribution shape, not just summary statistics."""))

cells.append(md(r"""### 📊 Expected Output

Three side-by-side violin plots showing the distribution of `n_genes_by_counts`, `total_counts`, and `pct_counts_mt` across all spots. Look for:
- The **main body** of each distribution (where most spots fall)
- **Outliers** — spots with extremely low gene counts or extremely high mitochondrial fractions"""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Flag mitochondrial genes and compute per-spot QC metrics
# ──────────────────────────────────────────────────────────────────────

# Human mitochondrial gene symbols start with "MT-"
adata_bc.var["mt"] = adata_bc.var_names.str.startswith("MT-")

# Compute all standard QC metrics in one pass
sc.pp.calculate_qc_metrics(adata_bc, qc_vars=["mt"], inplace=True)

sc.pl.violin(
    adata_bc,
    ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
    jitter=0.4,
    multi_panel=True,
    color="skyblue",
)"""))

cells.append(md(r"""### 🔍 Result Interpretation

**Genes detected (`n_genes_by_counts`):** Most spots should detect 2,000–6,000 genes. Spots with fewer than ~1,000 genes likely fall on empty slide or tissue edges.

**Total counts (`total_counts`):** The distribution should be unimodal with a long right tail. Very low-count spots should be removed. The median indicates typical sequencing depth.

**Mitochondrial fraction (`pct_counts_mt`):** For most healthy tissue, this should be below 10–15%. A subset of spots with >20% likely corresponds to damaged or dying tissue. The threshold depends on tissue type — tumor tissue sometimes shows naturally elevated mitochondrial content.

> **📌 Key Insight:** These three metrics are **correlated but not redundant**. A spot can have high total counts but a high mitochondrial fraction (damaged cell with intact mitochondria), or low gene count but reasonable mitochondrial levels (poor capture). Using all three provides a more complete quality picture.

---

### ⚠️ Common Mistakes

> **Using the same QC thresholds for all datasets:** QC thresholds should be **data-driven**, not universal. Always inspect the distributions before choosing cutoffs.

> **Confusing mitochondrial fraction with mitochondrial activity:** A high `pct_counts_mt` does not mean the cell has active mitochondria — it means cytoplasmic RNA has degraded, inflating the relative share of mitochondrial transcripts.

---

### 📋 Section Summary

- QC is a **mandatory first step** — it prevents damaged spots from biasing all downstream analyses
- Three key metrics: **gene count**, **total counts**, and **mitochondrial fraction**
- Mitochondrial genes serve as a **damage indicator** because their RNA is more resistant to degradation
- **Violin plots** reveal the full distribution, making outliers visible
- Thresholds should be **chosen by inspecting the data**, not applied blindly

---

### ✏️ Exercises

1. **Conceptual:** Why does cytoplasmic mRNA degrade faster than mitochondrial mRNA in damaged cells?
2. **Coding:** How many mitochondrial genes are in this dataset? Print `adata_bc.var["mt"].sum()`.
3. **Conceptual:** In a dataset from brain tissue, would you expect higher or lower baseline mitochondrial fractions compared to breast cancer tissue? Why?
4. **Coding:** Create a scatter plot of `total_counts` vs. `pct_counts_mt`. Do spots with very high mitochondrial fractions also tend to have low total counts?
5. **Conceptual:** What would a bimodal distribution in `n_genes_by_counts` suggest about the tissue?

---

### 📚 Further Reading

- Luecken, M. D. & Theis, F. J. *Current best practices in single-cell RNA-seq analysis: a tutorial.* Mol. Syst. Biol. **15**, e8746 (2019). [DOI](https://doi.org/10.15252/msb.20188746)
- [Scanpy preprocessing tutorial](https://scanpy-tutorials.readthedocs.io/en/latest/pbmc3k.html)
- Ilicic, T. et al. *Classification of low quality cells from single-cell RNA-seq data.* Genome Biol. **17**, 29 (2016). [DOI](https://doi.org/10.1186/s13059-016-0888-1)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 5: FILTERING
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 5. Filtering Low-Quality Spots

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Apply data-driven QC thresholds to filter out low-quality spatial spots
- Justify the choice of mitochondrial and gene-count thresholds
- Assess whether the filtering step removed an appropriate fraction of spots

---

### 🧬 Biological Background

Filtering removes spots that do not contain reliable biological signal. In this dataset, we apply two filters:

1. **Mitochondrial fraction < 10%** — removes spots with evidence of cell damage
2. **Minimum 1,000 genes detected** — removes spots with insufficient transcriptomic complexity (likely empty or low-quality tissue)

These thresholds were **chosen based on the violin plot distributions** in Section 4. They represent a balance between stringency (removing noise) and permissiveness (retaining biological signal).

> **⚠️ Warning:** Overly aggressive filtering can remove rare but biologically important cell populations (e.g., small immune infiltrates). Overly permissive filtering lets noise contaminate downstream clustering.

---

### 💻 Computational Background

Filtering in Scanpy works by Boolean indexing on `adata.obs`:
- `adata[adata.obs["pct_counts_mt"] < 10]` subsets to spots below the threshold
- `sc.pp.filter_cells(adata, min_genes=1000)` removes spots with fewer than 1,000 detected genes
- `.copy()` is called to create an independent object (avoiding Pandas/AnnData view warnings)"""))

cells.append(md(r"""### 📊 Expected Output

Two printed lines showing spot count before and after filtering. A moderate reduction (e.g., 5–15% of spots removed) is typical for good-quality Visium data."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Apply QC filters based on the distributions observed above
# ──────────────────────────────────────────────────────────────────────
n_before = adata_bc.n_obs

# Thresholds chosen from the violin plot distributions:
#   <10% mitochondrial content, minimum 1000 detected genes per spot
adata_bc = adata_bc[adata_bc.obs["pct_counts_mt"] < 10].copy()
sc.pp.filter_cells(adata_bc, min_genes=1000)

print(f"Spots before filtering: {n_before}")
print(f"Spots after filtering:  {adata_bc.n_obs}")"""))

cells.append(md(r"""### 🔍 Result Interpretation

Compare the before/after counts:

- **Losing <5% of spots** → very clean tissue, gentle filtering
- **Losing 5–15%** → typical for most Visium datasets
- **Losing >30%** → investigate whether thresholds are too aggressive, or the tissue quality is poor

The remaining spots should all represent high-quality tissue regions with sufficient transcriptomic information for reliable downstream analysis.

---

### ⚠️ Common Mistakes

> **Filtering before looking at the data:** Never apply QC thresholds from a paper or tutorial without first examining *your* QC distributions. Different tissues, species, and experimental protocols require different thresholds.

> **Forgetting `.copy()`:** Boolean subsetting in AnnData returns a *view*, not a copy. Modifications to a view can cause unexpected behavior. Always call `.copy()` after subsetting.

---

### 📋 Section Summary

- Two QC thresholds applied: **<10% mitochondrial** and **≥1,000 genes**
- Thresholds were **derived from violin plot inspection**, not arbitrary
- A moderate fraction of spots was removed (mostly empty/damaged)
- `.copy()` ensures the filtered object is independent of the original

---

### ✏️ Exercises

1. **Conceptual:** What would happen to downstream clustering if you set the mitochondrial threshold to 50% (essentially no filtering)?
2. **Coding:** How many spots were removed? What percentage of the original dataset was filtered out?
3. **Conceptual:** Would you use the same thresholds for a mouse brain Visium dataset? Why or why not?
4. **Coding:** Try filtering with `min_genes=500` instead. How many additional spots are retained? Would you expect those spots to be high-quality?

---

### 📚 Further Reading

- [Scanpy QC tutorial — filtering](https://scanpy-tutorials.readthedocs.io/en/latest/pbmc3k.html#Filtering-of-highly-variable-genes)
- Heumos, L. et al. *Best practices for single-cell analysis across modalities.* Nat. Rev. Genet. **24**, 550–572 (2023). [DOI](https://doi.org/10.1038/s41576-023-00586-w)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 6: NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 6. Normalization & Log Transformation

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain why raw count data must be normalized before analysis
- Describe the library-size normalization + log1p transformation procedure
- Understand the role of `adata.raw` as a pre-transformation backup
- Distinguish between technical variation (sequencing depth) and biological variation

---

### 🧬 Biological Background

Raw UMI counts are influenced by both **biological signal** (true differences in gene expression) and **technical noise** (differences in sequencing depth, capture efficiency, and library preparation). Two spots with identical biology can have vastly different raw counts simply because one had more sequencing reads.

**Normalization** removes this technical confound by scaling each spot to a common total (here, 10,000 counts). After normalization, differences between spots should primarily reflect biology, not sequencing depth.

**Log transformation** (`log1p` = log(x + 1)) compresses the large dynamic range of gene expression. Without it, a few highly expressed genes would dominate variance-based analyses (PCA, clustering), drowning out the signal from moderately expressed but biologically important genes.

---

### 💻 Computational Background

The two-step procedure:

1. **`sc.pp.normalize_total(target_sum=1e4)`** — divides each spot's counts by its total, then multiplies by 10,000
2. **`sc.pp.log1p()`** — applies `log(x + 1)` element-wise (the `+1` avoids `log(0)`)

The result is stored in `adata.X`. The pre-normalization values are saved in `adata.raw` for later use (e.g., marker gene lookups, which need the full gene set, not just the HVG subset selected in Section 7).

> **💡 Tip:** The choice of `target_sum=1e4` is conventional, not magic. Some workflows use the median total counts instead. The log transformation matters more than the exact scaling factor."""))

cells.append(md(r"""### 📊 Expected Output

No plot — a confirmation message indicating normalization is complete. The expression matrix is now normalized and log-transformed."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Normalize to a common library size and log-transform
# ──────────────────────────────────────────────────────────────────────
sc.pp.normalize_total(adata_bc, target_sum=1e4)
sc.pp.log1p(adata_bc)

# Preserve the normalized-but-not-subsetted data for later gene lookups
adata_bc.raw = adata_bc

print("Normalization complete: all spots are now on a comparable expression scale.")"""))

cells.append(md(r"""### 🔍 Result Interpretation

After this step, `adata_bc.X` contains **log-normalized expression values**. These are no longer raw counts — they are comparable across spots regardless of original sequencing depth.

The `adata_bc.raw` backup is crucial: when we later subset to highly variable genes (Section 7), `raw` still contains all genes, allowing us to look up any gene's expression even if it wasn't selected as highly variable.

---

### ⚠️ Common Mistakes

> **Normalizing before filtering:** Always filter low-quality spots *before* normalizing. Including damaged spots in the normalization distorts the scaling for healthy spots.

> **Forgetting to set `adata.raw`:** Without this backup, you lose access to non-HVG genes after feature selection. Many downstream analyses (marker gene lookups, GSEA) need the full gene set.

> **Double-normalizing:** Running this cell twice applies the transformation twice, producing incorrect values. If in doubt, reload the data and re-run from the beginning.

---

### 📋 Section Summary

- **Library-size normalization** removes technical variation in sequencing depth
- **Log transformation** compresses dynamic range, preventing highly expressed genes from dominating
- `adata.raw` stores the **pre-subsetting backup** for later gene lookups
- The conventional `target_sum=1e4` is widely used but not the only valid choice
- Always normalize **after** QC filtering, never before

---

### ✏️ Exercises

1. **Conceptual:** If spot A has 50,000 total counts and spot B has 5,000, how does normalization to 10,000 change the interpretation of a gene expressed at 500 counts in both spots?
2. **Conceptual:** Why use `log1p` (log(x+1)) instead of `log(x)`? What would happen to zero-expressed genes with `log(x)`?
3. **Coding:** Compare the mean of `adata_bc.X` before and after normalization (you'd need to re-run from data loading to test this).
4. **Conceptual:** Some methods (like `scran` pooling normalization) use a different approach. What assumption does simple library-size normalization make that might be violated?

---

### 📚 Further Reading

- Lun, A. T. L., Bach, K. & Marioni, J. C. *Pooling across cells to normalize single-cell RNA sequencing data with many zero counts.* Genome Biol. **17**, 75 (2016). [DOI](https://doi.org/10.1186/s13059-016-0947-7)
- Hafemeister, C. & Satija, R. *Normalization and variance stabilization of single-cell RNA-seq data using regularized negative binomial regression.* Genome Biol. **20**, 296 (2019). [DOI](https://doi.org/10.1186/s13059-019-1874-1)
- [Scanpy normalization docs](https://scanpy.readthedocs.io/en/stable/api/generated/scanpy.pp.normalize_total.html)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 7: FEATURE SELECTION
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 7. Feature Selection (Highly Variable Genes)

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain why feature selection is necessary before dimensionality reduction
- Distinguish between highly variable genes (HVGs) and housekeeping genes
- Interpret the HVG scatter plot (variance vs. mean expression)
- Understand the impact of `n_top_genes` on downstream resolution

---

### 🧬 Biological Background

The human genome encodes ~20,000 protein-coding genes, but not all are informative for distinguishing cell types or tissue compartments:

- **Housekeeping genes** (e.g., ribosomal proteins, GAPDH) are expressed at similar levels in all cells — they carry no information about cell identity
- **Lowly expressed genes** with sporadic detection are dominated by noise
- **Highly variable genes (HVGs)** show large expression differences across spots — these are the genes that define biological heterogeneity (e.g., immune markers, tumor-specific genes)

By selecting only the top 2,000 most variable genes, we focus the analysis on biologically informative features and reduce noise from uninformative ones.

---

### 💻 Computational Background

The **Seurat method** (`flavor="seurat"`) for HVG selection:

1. Bins genes by mean expression level
2. Within each bin, computes variance
3. Selects genes with the highest **variance-to-mean ratio** (dispersion)

This accounts for the fact that highly expressed genes naturally have higher variance (a statistical property of count data). The resulting selection is enriched for genes that vary *more than expected* given their expression level.

**Why 2,000 genes?** This is a widely used default that balances:
- **Signal** — enough genes to capture major biological differences
- **Noise** — few enough to avoid diluting signal with uninformative features
- **Computation** — PCA and clustering are faster with fewer features"""))

cells.append(md(r"""### 📊 Expected Output

An HVG scatter plot showing variance (dispersion) vs. mean expression. Selected HVGs are highlighted, while non-selected genes form the background. A printed message confirms the reduced gene count."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Select the top 2,000 most variable genes
# ──────────────────────────────────────────────────────────────────────
sc.pp.highly_variable_genes(adata_bc, n_top_genes=2000, flavor="seurat")
sc.pl.highly_variable_genes(adata_bc)

adata_bc = adata_bc[:, adata_bc.var["highly_variable"]]
print(f"Working dataset: {adata_bc.n_obs} spots × {adata_bc.n_vars} highly variable genes.")"""))

cells.append(md(r"""### 🔍 Result Interpretation

In the scatter plot:
- **Black dots (selected HVGs)** appear above the main cloud — they have higher-than-expected variance for their expression level
- **Grey dots (non-selected)** form the bulk of genes with "normal" variability
- Genes at the far right (high mean expression, moderate variance) are often housekeeping genes

After subsetting, the expression matrix shrinks from ~33,000 genes to 2,000, dramatically reducing computational cost while retaining the most informative features.

> **📌 Important:** The full gene set is still accessible via `adata_bc.raw` (set in Section 6). This is essential for later steps like marker gene identification and pathway analysis.

---

### ⚠️ Common Mistakes

> **Selecting too few HVGs:** Using <500 genes may miss important biological signal, especially in complex tissues with many cell types.

> **Selecting too many HVGs:** Using >5,000 genes re-introduces noise and diminishes the benefit of feature selection.

> **Not understanding the subsetting:** After this step, `adata_bc.var_names` only contains 2,000 genes. If you need to look up a specific gene, use `adata_bc.raw`.

---

### 📋 Section Summary

- **Highly variable genes** are the most informative features for distinguishing biological groups
- The **Seurat method** selects genes with high variance relative to their mean expression
- **2,000 HVGs** is a well-established default that balances signal, noise, and computation
- After subsetting, the **full gene set is preserved** in `adata_bc.raw`
- Feature selection is a prerequisite for PCA and clustering

---

### ✏️ Exercises

1. **Conceptual:** Would a gene like GAPDH (expressed at similar levels in all spots) be selected as highly variable? Why or why not?
2. **Coding:** List the top 10 most variable genes by printing `adata_bc.var.sort_values("dispersions_norm", ascending=False).head(10)` (run before subsetting).
3. **Conceptual:** If you increased `n_top_genes` to 5,000, how would you expect the downstream clustering to change? More clusters? Fewer?
4. **Coding:** How many of the 2,000 selected HVGs are mitochondrial genes? Should they be? (Hint: check `adata_bc.var_names.str.startswith("MT-")`)

---

### 📚 Further Reading

- Stuart, T. et al. *Comprehensive integration of single-cell data.* Cell **177**, 1888–1902 (2019). [DOI](https://doi.org/10.1016/j.cell.2019.05.031)
- [Scanpy HVG tutorial](https://scanpy.readthedocs.io/en/stable/api/generated/scanpy.pp.highly_variable_genes.html)
- Brennecke, P. et al. *Accounting for technical noise in single-cell RNA-seq experiments.* Nat. Methods **10**, 1093–1095 (2013). [DOI](https://doi.org/10.1038/nmeth.2645)"""))

# ═══════════════════════════════════════════════════════════════════════
# PART III: UNSUPERVISED ANALYSIS
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

# Part III — Unsupervised Analysis

> *Reducing dimensions, discovering clusters, and identifying their molecular signatures*"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 8: PCA
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 8. Dimensionality Reduction (PCA)

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain why dimensionality reduction is needed before clustering
- Describe how PCA transforms a high-dimensional expression matrix into principal components
- Interpret the variance ratio (elbow) plot to choose the number of components
- Understand the trade-off between retaining signal and removing noise

---

### 🧬 Biological Background

Even after feature selection, 2,000 genes is a high-dimensional space. Many of these genes are **correlated** — they tend to go up or down together because they are co-regulated by the same biological programs (e.g., genes in the same pathway, genes expressed in the same cell type).

**Principal Component Analysis (PCA)** exploits these correlations to compress 2,000 dimensions into a much smaller number of **principal components (PCs)** that capture the major axes of biological variation. The first few PCs typically correspond to the strongest biological differences (e.g., tumor vs. stroma), while later PCs capture progressively weaker signals and eventually noise.

---

### 💻 Computational Background

PCA finds a new coordinate system where:

1. **PC1** captures the direction of greatest variance in the data
2. **PC2** captures the direction of greatest variance *orthogonal to PC1*
3. And so on...

The **variance ratio plot** (also called the "elbow plot") shows how much variance each PC explains. The "elbow" — where the curve flattens — indicates the transition from signal to noise. Components beyond this point add noise without meaningful biological information.

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `svd_solver="arpack"` | Iterative solver | Efficient for sparse matrices (faster than full SVD) |
| `random_state=42` | Fixed seed | Ensures reproducibility of the iterative solver |

> **💡 Tip:** We compute 50 PCs but will only *use* 15 for clustering (Section 9). The full 50 PCs are computed to allow the elbow plot to inform the choice."""))

cells.append(md(r"""### 📊 Expected Output

A variance ratio (elbow) plot with 50 components on the x-axis and explained variance (log scale) on the y-axis. Expect a sharp drop in the first 5–10 components, then a gradual flattening after ~15 components."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# PCA on the HVG-subset expression matrix
# ──────────────────────────────────────────────────────────────────────
sc.tl.pca(adata_bc, svd_solver="arpack", random_state=RANDOM_STATE)
sc.pl.pca_variance_ratio(adata_bc, n_pcs=50, log=True)"""))

cells.append(md(r"""### 🔍 Result Interpretation

The elbow plot should show:

- **Steep descent** in the first ~5 PCs — these capture the dominant biological programs (tumor vs. stroma, immune infiltrate vs. background)
- **Gradual flattening** around PC 10–20 — diminishing returns from additional components
- **Plateau** beyond ~25 PCs — mostly noise

For this dataset, using the **first 15 PCs** strikes a good balance. This is a conservative choice that retains most biological signal while excluding noise-dominated components.

> **📌 Key Insight:** PCA is a *linear* method — it can only capture linear combinations of gene expression. Non-linear structure (e.g., branching trajectories) will be captured later by UMAP (Section 13).

---

### ⚠️ Common Mistakes

> **Using too few PCs:** Truncating at 3–5 PCs may discard subtle but important biological variation (e.g., rare immune subtypes).

> **Using too many PCs:** Including 50 PCs can introduce noise that obscures biological signal in clustering.

> **Skipping the elbow plot:** Always visualize the variance ratios — the "right" number of PCs varies between datasets.

---

### 📋 Section Summary

- PCA compresses 2,000 genes into a small number of **principal components**
- The **elbow plot** guides the choice of how many PCs to retain
- The first 15 PCs will be used for downstream clustering and neighbor graph construction
- PCA is **linear** — it complements non-linear methods like UMAP
- The `arpack` solver is efficient for the sparse matrices typical in spatial transcriptomics

---

### ✏️ Exercises

1. **Conceptual:** If PC1 separates tumor from stroma, what biological programs might PC2 and PC3 capture?
2. **Coding:** Visualize the first two PCs with `sc.pl.pca(adata_bc, color="total_counts")`. Do spots separate by sequencing depth? If so, what does that imply?
3. **Conceptual:** Why is PCA performed on log-normalized data rather than raw counts?
4. **Coding:** Print the top 5 genes with the highest loadings on PC1 using `adata_bc.varm['PCs'][:, 0]`. Do they correspond to known tumor or immune markers?

---

### 📚 Further Reading

- Jolliffe, I. T. & Cadima, J. *Principal component analysis: a review and recent developments.* Phil. Trans. R. Soc. A **374**, 20150202 (2016). [DOI](https://doi.org/10.1098/rsta.2015.0202)
- [Scanpy PCA documentation](https://scanpy.readthedocs.io/en/stable/api/generated/scanpy.tl.pca.html)
- Nguyen, L. H. & Holmes, S. *Ten quick tips for effective dimensionality reduction.* PLoS Comput. Biol. **15**, e1006907 (2019). [DOI](https://doi.org/10.1371/journal.pcbi.1006907)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 9: CLUSTERING
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 9. Clustering (Leiden)

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain the two-step process: neighbor graph construction → community detection
- Describe how the Leiden algorithm identifies clusters in a graph
- Interpret spatial cluster maps and assess whether clusters are biologically meaningful
- Understand the role of `n_neighbors` and `n_pcs` parameters

---

### 🧬 Biological Background

Tissue is not homogeneous — it is composed of distinct **compartments** (tumor epithelium, stromal connective tissue, immune infiltrates, vasculature, etc.). Clustering groups spots with similar gene expression profiles, and in spatial transcriptomics, these clusters often correspond to anatomically and functionally distinct tissue regions.

A **good clustering** produces groups that are:
- **Spatially coherent** — spots in the same cluster should form contiguous regions on the tissue, not random speckles
- **Biologically interpretable** — each cluster should correspond to a recognizable tissue type
- **Stable** — small changes in parameters should not dramatically alter the results

---

### 💻 Computational Background

Clustering in Scanpy is a two-step process:

**Step 1: k-nearest-neighbor (kNN) graph**
- For each spot, find its 15 nearest neighbors in PCA space (first 15 PCs)
- Connect spots to their neighbors, forming a graph
- This graph captures local similarities in expression space

**Step 2: Leiden community detection**
- The Leiden algorithm partitions the graph into densely connected communities (clusters)
- It optimizes **modularity** — a measure of how well the graph is divided into internally dense, externally sparse groups
- Leiden is preferred over the older Louvain algorithm because it guarantees well-connected communities

| Parameter | Value | Effect |
|-----------|-------|--------|
| `n_neighbors=15` | Neighborhood size | Larger = smoother, fewer clusters; Smaller = finer resolution |
| `n_pcs=15` | PCs used for distances | Based on elbow plot from Section 8 |
| `resolution` (default=1) | Leiden resolution | Higher = more clusters; Lower = fewer, broader clusters |"""))

cells.append(md(r"""### 📊 Expected Output

A spatial plot with each spot colored by its cluster assignment. Clusters should form **spatially coherent regions** that correspond to visible tissue structures in the H&E background."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Build a kNN graph and cluster with the Leiden algorithm
# ──────────────────────────────────────────────────────────────────────
sc.pp.neighbors(adata_bc, n_neighbors=15, n_pcs=15, random_state=RANDOM_STATE)
sc.tl.leiden(adata_bc, key_added="clusters", random_state=RANDOM_STATE)

sq.pl.spatial_scatter(
    adata_bc,
    color="clusters",
    title="Breast Cancer Tissue — Spatial Clusters (Leiden)",
    size=0.8,
    shape="circle",
    alpha=0.85,
    img_alpha=1.0,
    figsize=(8, 8),
)
plt.axis("off")
plt.show()"""))

cells.append(md(r"""### 🔍 Result Interpretation

Examine the spatial cluster map for:

- **Spatial coherence:** Clusters should form contiguous tissue regions, not random salt-and-pepper patterns. Spatial coherence confirms that transcriptomic similarity aligns with spatial proximity.
- **Number of clusters:** Typically 8–15 for a Visium breast cancer section. Too few may merge distinct tissue types; too many may over-fragment.
- **Correspondence to morphology:** Compare cluster boundaries with the H&E image. The tumor core, stromal regions, and immune-dense areas should each correspond to distinct clusters.

> **📌 Key Insight:** These cluster numbers are arbitrary labels — they carry no inherent biological meaning. Sections 10 and 14 will assign biological identities to each cluster using marker genes.

---

### ⚠️ Common Mistakes

> **Treating clusters as ground truth:** Clustering is an unsupervised approximation. Cluster boundaries are influenced by algorithm parameters and may not perfectly correspond to biological boundaries.

> **Ignoring spatial coherence:** In spatial data, spatially incoherent clusters (random speckles) often indicate over-clustering or technical artifacts.

> **Not trying multiple resolutions:** The default Leiden resolution may not be optimal. Always visualize results at different resolutions to find the right granularity.

---

### 📋 Section Summary

- Clustering is a **two-step process**: build a kNN graph in PCA space, then partition it with Leiden
- **15 neighbors** and **15 PCs** are used based on the elbow plot analysis
- Clusters should be **spatially coherent** — forming contiguous tissue regions
- Cluster labels are **arbitrary numbers** — biological interpretation comes from marker genes
- The Leiden algorithm guarantees **well-connected** communities (unlike Louvain)

---

### ✏️ Exercises

1. **Conceptual:** Why is the kNN graph built in PCA space (15 PCs) rather than the full 2,000-gene expression space?
2. **Coding:** Re-run Leiden with `resolution=0.5` and `resolution=2.0`. How does the number of clusters change?
3. **Conceptual:** If a cluster appears as scattered spots with no spatial coherence, what might be happening biologically or technically?
4. **Coding:** Print the number of spots per cluster with `adata_bc.obs["clusters"].value_counts()`. Are the clusters roughly balanced, or do some contain very few spots?
5. **Conceptual:** Could two spots that are physically adjacent on the tissue belong to different clusters? When would this be expected?

---

### 📚 Further Reading

- Traag, V. A., Waltman, L. & van Eck, N. J. *From Louvain to Leiden: guaranteeing well-connected communities.* Sci. Rep. **9**, 5233 (2019). [DOI](https://doi.org/10.1038/s41598-019-41695-z)
- [Scanpy clustering tutorial](https://scanpy-tutorials.readthedocs.io/en/latest/pbmc3k.html#Clustering-the-neighborhood-graph)
- Blondel, V. D. et al. *Fast unfolding of communities in large networks.* J. Stat. Mech. **2008**, P10008 (2008). [DOI](https://doi.org/10.1088/1742-5468/2008/10/P10008)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 10: MARKER GENES
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 10. Marker Gene Identification

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain what marker genes are and why they are essential for cluster annotation
- Describe the statistical test (t-test) used to rank genes per cluster
- Interpret a dot plot showing marker gene specificity and expression level
- Use marker genes to hypothesize cell-type identities for clusters

---

### 🧬 Biological Background

Cluster numbers are meaningless until we identify the **genes that define them**. Marker genes are genes that are significantly more expressed in one cluster compared to all others. Well-known markers link clusters to cell types:

| Marker Gene | Cell Type | Biological Role |
|-------------|-----------|-----------------|
| **EPCAM**, **KRT8** | Epithelial / Tumor | Structural proteins of epithelial cells |
| **CCND1** | Tumor (proliferating) | Cell cycle regulator, often amplified in breast cancer |
| **IGKC**, **CD79A** | B cells / Plasma cells | Immunoglobulin components |
| **COL1A1**, **DCN** | Fibroblasts / Stroma | Extracellular matrix components |
| **CD3D**, **CD8A** | T cells | T-cell receptor components |

By examining which genes are upregulated in each cluster, we can assign biological identities — transforming abstract numbers into meaningful labels.

---

### 💻 Computational Background

`sc.tl.rank_genes_groups()` performs a **differential expression test** for each cluster versus all other clusters:

- **Method:** Welch's t-test (assumes unequal variances between groups)
- **Output:** A ranked list of genes per cluster, ordered by test statistic
- **Visualization:** A dot plot where:
  - **Dot size** = fraction of spots in the cluster expressing the gene
  - **Dot color** = mean expression level (scaled per gene for comparability)"""))

cells.append(md(r"""### 📊 Expected Output

A dot plot showing the **top 3 marker genes per cluster**. Each row is a gene, each column is a cluster. Larger, darker dots indicate genes that are both widely expressed and highly specific to that cluster."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Rank genes by specificity for each cluster (t-test)
# ──────────────────────────────────────────────────────────────────────
sc.tl.rank_genes_groups(adata_bc, groupby="clusters", method="t-test")

sc.pl.rank_genes_groups_dotplot(
    adata_bc,
    n_genes=3,
    standard_scale="var",
    cmap="Blues",
    title="Top Marker Genes per Cluster",
)"""))

cells.append(md(r"""### 🔍 Result Interpretation

For each cluster, examine its top markers:

- **Cluster-specific markers** (large, dark dots in one column, small/absent elsewhere) are strong indicators of cell type
- **Shared markers** (dark dots across multiple columns) suggest related cell types or common biological programs
- Look for **known biology**: immune genes (immunoglobulins, CD markers) in immune clusters, keratins in epithelial clusters, collagens in stromal clusters

> **📌 Key Insight:** The marker genes identified here will guide the **manual cell-type annotation** in Section 14. Take note of which clusters show immune markers (e.g., IGKC) vs. tumor markers (e.g., CCND1).

---

### ⚠️ Common Mistakes

> **Relying on a single marker:** No single gene is a definitive cell-type label. Always consider a **panel of markers** for each cluster.

> **Ignoring the dot plot scale:** Dot plots use per-gene scaling (`standard_scale="var"`). This means expression values are not directly comparable *between* genes — only *across clusters for the same gene*.

> **Using only t-test:** The t-test assumes normality and may not be optimal for all datasets. Alternatives include Wilcoxon rank-sum and logistic regression.

---

### 📋 Section Summary

- Marker genes translate **cluster numbers** into **biological identities**
- A **t-test** ranks genes by how specifically they are expressed in each cluster
- The **dot plot** encodes both expression level (color) and fraction of expressing spots (size)
- Known marker genes connect clusters to literature-documented cell types
- Marker gene identification is the foundation for annotation (Section 14)

---

### ✏️ Exercises

1. **Conceptual:** Why might a t-test produce different results than a Wilcoxon rank-sum test for this type of data?
2. **Coding:** Increase `n_genes` from 3 to 10 and re-plot. Do additional markers strengthen or weaken your confidence in the cluster identities?
3. **Conceptual:** If a cluster has no clearly specific markers (all genes are shared with other clusters), what might that indicate?
4. **Coding:** Extract the top 5 marker genes for cluster "0" using `sc.get.rank_genes_groups_df(adata_bc, group="0").head(5)`. Look up these genes — what cell type do they suggest?
5. **Conceptual:** Why do we perform marker gene analysis on log-normalized data rather than raw counts?

---

### 📚 Further Reading

- [Scanpy marker gene tutorial](https://scanpy.readthedocs.io/en/stable/api/generated/scanpy.tl.rank_genes_groups.html)
- Soneson, C. & Robinson, M. D. *Bias, robustness and scalability in single-cell differential expression analysis.* Nat. Methods **15**, 255–261 (2018). [DOI](https://doi.org/10.1038/nmeth.4612)
- [GeneCards — human gene database](https://www.genecards.org/)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 11: SPATIAL MARKERS
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 11. Spatial Expression of Key Marker Genes

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Overlay individual gene expression on the tissue image
- Validate marker gene assignments by comparing expression patterns with tissue morphology
- Distinguish tumor-enriched from immune-enriched spatial regions visually

---

### 🧬 Biological Background

After identifying marker genes computationally (Section 10), we validate them **spatially**. If CCND1 (a tumor marker) is truly enriched in tumor clusters, its expression should overlap with tumor-dense regions visible in the H&E image. Similarly, IGKC (an immunoglobulin component) should localize to immune-infiltrated areas.

This visual validation connects **computational results** to **tissue biology** — one of the unique strengths of spatial transcriptomics over standard scRNA-seq.

---

### 💻 Computational Background

We re-use `sq.pl.spatial_scatter()` but now color spots by individual gene expression values (from `adata.X` or `adata.raw`) instead of QC metrics. This creates a **spatial gene expression map** — essentially a molecular stain that can be compared directly to the morphological H&E stain."""))

cells.append(md(r"""### 📊 Expected Output

Two side-by-side spatial plots: one for the tumor marker **CCND1** and one for the immune marker **IGKC**. CCND1 should be enriched in the tumor core; IGKC in immune-infiltrated peripheral regions."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Spatial validation of key marker genes
# ──────────────────────────────────────────────────────────────────────
marker_genes = ["CCND1", "IGKC"]
available_markers = [g for g in marker_genes if g in adata_bc.var_names]

if available_markers:
    sq.pl.spatial_scatter(
        adata_bc,
        color=available_markers,
        title=[f"{'Tumor' if g == 'CCND1' else 'Immune'} Marker ({g})" for g in available_markers],
        cmap="magma",
        size=0.8,
        shape="circle",
        alpha=0.85,
        img_alpha=1.0,
        figsize=(6 * len(available_markers), 6),
    )
    plt.show()
else:
    print(f"None of the requested marker genes {marker_genes} were found in the dataset.")"""))

cells.append(md(r"""### 🔍 Result Interpretation

- **CCND1 (Tumor Marker):** Should show high expression (bright) in the dense tumor regions of the tissue. CCND1 encodes Cyclin D1, a key cell-cycle regulator frequently amplified in breast cancer.
- **IGKC (Immune Marker):** Should show high expression in regions with immune cell infiltration, often at the tumor periphery or in lymphoid aggregates. IGKC encodes the immunoglobulin kappa constant region, produced by B cells and plasma cells.

If the spatial expression patterns match the cluster locations from Section 9, this provides **independent validation** that the clustering captures real biological structure.

---

### ⚠️ Common Mistakes

> **Plotting genes that were excluded during HVG selection:** If a gene is not among the 2,000 HVGs, it won't be in `adata_bc.var_names`. Use `adata_bc.raw` to access the full gene set.

> **Over-interpreting diffuse expression:** Some genes are expressed broadly at low levels. A strong marker should show high expression in a specific region and low/absent expression elsewhere.

---

### 📋 Section Summary

- Spatial gene expression maps **validate** marker genes identified by differential expression
- CCND1 (tumor) and IGKC (immune) show complementary spatial patterns
- This cross-validation between **computational results** and **tissue morphology** is unique to spatial transcriptomics
- Genes not in the HVG subset can be accessed via `adata_bc.raw`

---

### ✏️ Exercises

1. **Coding:** Choose a stromal marker (e.g., COL1A1 or DCN) and plot its spatial expression. Does it localize to a distinct tissue region?
2. **Conceptual:** Why is spatial validation more informative than simply checking if a gene is differentially expressed?
3. **Coding:** Plot the same markers on the UMAP embedding (after Section 13) and compare with the spatial plots. Are the patterns consistent?

---

### 📚 Further Reading

- [Squidpy spatial scatter documentation](https://squidpy.readthedocs.io/en/stable/api/generated/squidpy.pl.spatial_scatter.html)
- Musella, M. et al. *CCND1 in breast cancer.* Oncogene **36**, 1–12 (2017)."""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 12: NEIGHBORHOOD ENRICHMENT
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 12. Spatial Neighborhood Enrichment

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain the concept of spatial neighbor graphs and how they differ from kNN expression graphs
- Interpret a neighborhood enrichment heatmap
- Identify which cluster pairs co-localize or avoid each other
- Understand permutation-based significance testing for spatial statistics

---

### 🧬 Biological Background

Beyond knowing *where* cell types are, we need to know **who neighbors whom**. Tissue architecture is defined by spatial relationships:

- **Tumor–immune co-localization** suggests active immune infiltration or immune surveillance
- **Tumor–stroma adjacency** is expected at tumor boundaries (invasive front)
- **Immune–immune clustering** may indicate tertiary lymphoid structures

Neighborhood enrichment quantifies whether two cluster types are found next to each other **more or less often than expected by chance** (random shuffling of labels).

---

### 💻 Computational Background

**Step 1: Spatial neighbor graph**
`sq.gr.spatial_neighbors()` connects each spot to its **physically adjacent** spots based on spatial coordinates (not expression similarity). This is fundamentally different from the kNN graph in Section 9.

**Step 2: Neighborhood enrichment test**
`sq.gr.nhood_enrichment()` uses a permutation test:
1. Count how often each cluster pair is adjacent in the real data
2. Randomly shuffle cluster labels many times
3. Compare real co-occurrences to the random expectation
4. The resulting Z-score indicates enrichment (+) or depletion (-)"""))

cells.append(md(r"""### 📊 Expected Output

A heatmap where each cell shows the neighborhood enrichment Z-score between two clusters. Bright cells indicate cluster pairs that **co-localize** more than expected; dark cells indicate **spatial avoidance**."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Build a spatial neighbor graph and test neighborhood enrichment
# ──────────────────────────────────────────────────────────────────────

# Spatial graph (based on physical adjacency, reused in Section 20)
sq.gr.spatial_neighbors(adata_bc)
sq.gr.nhood_enrichment(adata_bc, cluster_key="clusters")

sq.pl.nhood_enrichment(
    adata_bc,
    cluster_key="clusters",
    figsize=(8, 8),
    title="Cell–Cell Neighborhood Enrichment",
    cmap="inferno",
)
plt.show()"""))

cells.append(md(r"""### 🔍 Result Interpretation

In the heatmap:

- **Diagonal entries** (self-enrichment) are typically positive — spots of the same cluster tend to be adjacent, confirming spatial coherence
- **Off-diagonal bright entries** indicate clusters that frequently neighbor each other (co-localization)
- **Off-diagonal dark entries** indicate clusters that rarely neighbor each other (spatial segregation)

For breast cancer tissue, you might observe:
- Tumor clusters enriched with themselves (solid tumor core)
- Immune clusters enriched near specific tumor subtypes (tumor–immune interface)
- Stroma enriched at tissue boundaries

> **📌 Key Insight:** This analysis goes beyond "which cell types are present" to **how they are spatially organized** — a question that only spatial transcriptomics can answer.

---

### ⚠️ Common Mistakes

> **Confusing spatial and expression neighbor graphs:** The spatial graph (physical adjacency) and the expression kNN graph (Section 9) are different. This section uses *physical* neighbors.

> **Over-interpreting weak enrichment:** Small Z-scores (±1) may not be biologically meaningful. Focus on strong enrichment/depletion patterns.

---

### 📋 Section Summary

- **Spatial neighbor graphs** connect physically adjacent spots (distinct from expression-based kNN)
- **Neighborhood enrichment** tests whether cluster pairs co-localize more than expected by chance
- Results are presented as a **Z-score heatmap** (positive = co-localization, negative = avoidance)
- This reveals **tissue architecture** — how cell types are organized relative to each other
- The spatial graph built here is **reused** in Section 20

---

### ✏️ Exercises

1. **Conceptual:** Why is it important to use a permutation test rather than simply counting neighbor frequencies?
2. **Coding:** Which cluster pair has the highest co-enrichment? Does this make sense biologically?
3. **Conceptual:** Would you expect the same neighborhood enrichment patterns in a healthy tissue sample? Why might tumor tissue differ?
4. **Conceptual:** How would increasing the number of clusters (higher Leiden resolution) affect the enrichment patterns?

---

### 📚 Further Reading

- Palla, G. et al. *Squidpy: a scalable framework for spatial omics analysis.* Nat. Methods **19**, 171–178 (2022). [DOI](https://doi.org/10.1038/s41592-021-01358-2)
- [Squidpy neighborhood enrichment tutorial](https://squidpy.readthedocs.io/en/stable/auto_tutorials/tutorial_nhood_enrichment.html)
- Schapiro, D. et al. *histoCAT: analysis of cell phenotypes and interactions in multiplex image cytometry data.* Nat. Methods **14**, 873–876 (2017). [DOI](https://doi.org/10.1038/nmeth.4391)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 13: UMAP
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 13. UMAP Embedding

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain how UMAP creates a 2D representation of high-dimensional data
- Distinguish between spatial plots (tissue coordinates) and UMAP plots (expression coordinates)
- Interpret UMAP embeddings colored by cluster and gene expression
- Understand the limitations of UMAP visualization

---

### 🧬 Biological Background

The spatial plot shows clusters on the tissue; UMAP shows clusters in **expression space**. Both views are complementary:

- **Spatial plot:** "Where are the clusters on the tissue?"
- **UMAP plot:** "How different are the clusters in gene expression?"

Clusters that overlap in UMAP space are transcriptomically similar (even if spatially distant), while well-separated UMAP clusters are highly distinct in their expression profiles.

---

### 💻 Computational Background

**UMAP** (Uniform Manifold Approximation and Projection) is a non-linear dimensionality reduction technique that:

1. Constructs a high-dimensional graph of similarities (from the kNN graph)
2. Optimizes a low-dimensional (2D) layout that preserves local neighborhood structure
3. Produces a visualization where similar spots are close together

> **⚠️ Important UMAP caveats:**
> - **Distances between well-separated clusters** are not meaningful
> - **Cluster sizes** in UMAP do not reflect real population sizes
> - UMAP is for **visualization only** — never cluster or test on UMAP coordinates"""))

cells.append(md(r"""### 📊 Expected Output

A multi-panel UMAP plot showing spots colored by cluster assignment, CCND1 expression, and IGKC expression. Clusters should form **visually separated groups**, with tumor markers and immune markers concentrated in different UMAP regions."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# UMAP: non-spatial view of transcriptional similarity
# ──────────────────────────────────────────────────────────────────────
sc.tl.umap(adata_bc, random_state=RANDOM_STATE)

sc.pl.umap(
    adata_bc,
    color=["clusters"] + available_markers,
    cmap="magma",
    size=15,
    title=["Leiden Clusters"] + [f"Marker: {g}" for g in available_markers],
    wspace=0.4,
)"""))

cells.append(md(r"""### 🔍 Result Interpretation

The UMAP should show:

- **Separated cluster clouds:** Well-defined clusters in UMAP space confirm that the Leiden clustering captured real transcriptional differences
- **CCND1 enrichment** concentrated in tumor cluster regions of UMAP
- **IGKC enrichment** concentrated in immune cluster regions of UMAP

If clusters that are spatially adjacent on the tissue also overlap in UMAP space, they may represent transitional zones or closely related cell states.

---

### ⚠️ Common Mistakes

> **Interpreting UMAP distances as quantitative:** The distance between two clusters in UMAP does *not* reflect how different they are biologically. UMAP preserves **local**, not global, structure.

> **Running downstream analyses on UMAP coordinates:** UMAP is a lossy transformation. Always cluster and compute distances in PCA space, not UMAP.

---

### 📋 Section Summary

- UMAP provides a **non-spatial, expression-based** visualization complementary to the tissue plot
- Clusters that separate in UMAP are transcriptomically distinct
- Overlaying marker gene expression on UMAP validates both clustering and marker selection
- UMAP is for **visualization only** — all quantitative analyses use PCA space
- **Distances and cluster sizes in UMAP are not interpretable**

---

### ✏️ Exercises

1. **Conceptual:** If two clusters are adjacent on the tissue but far apart in UMAP, what does that tell you about their relationship?
2. **Coding:** Re-run UMAP with a different `random_state`. Does the overall layout change? Do the clusters still separate?
3. **Conceptual:** Why can't we use UMAP coordinates for differential expression testing?
4. **Coding:** Color the UMAP by `total_counts`. Does sequencing depth correlate with any cluster?

---

### 📚 Further Reading

- McInnes, L., Healy, J. & Melville, J. *UMAP: Uniform Manifold Approximation and Projection for dimension reduction.* arXiv:1802.03426 (2018). [DOI](https://doi.org/10.48550/arXiv.1802.03426)
- [Understanding UMAP](https://pair-code.github.io/understanding-umap/)
- Becht, E. et al. *Dimensionality reduction for visualizing single-cell data using UMAP.* Nat. Biotechnol. **37**, 38–44 (2019). [DOI](https://doi.org/10.1038/nbt.4314)"""))

# ═══════════════════════════════════════════════════════════════════════
# PART IV
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

# Part IV — Cell-Type Annotation & Communication

> *Assigning biological identities to clusters and inferring cell–cell signaling*"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 14: MANUAL ANNOTATION
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 14. Manual Cell-Type Annotation

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Manually assign cell-type labels to clusters based on marker gene evidence
- Explain why manual annotation remains important despite automated tools
- Handle unmapped clusters gracefully with fallback labels
- Visualize annotated cell types on the UMAP embedding

---

### 🧬 Biological Background

Manual cell-type annotation translates cluster numbers into biologically meaningful labels based on the marker genes identified in Section 10. For this breast cancer dataset:

| Clusters | Assigned Label | Evidence |
|----------|---------------|----------|
| 0, 8 | Tumor Cells | CCND1, cell-cycle genes, epithelial markers |
| 2, 7 | Immune/B-Cells | IGKC, immunoglobulin genes |
| 1, 9 | Stromal/Fibroblasts | Collagen genes, extracellular matrix components |
| Others | Other_N | Insufficient evidence for confident assignment |

This mapping is intentionally **conservative** — clusters without strong, unambiguous markers are labeled "Other" rather than force-fit into a category.

---

### 💻 Computational Background

The mapping is implemented as a Python dictionary lookup applied to the cluster labels. A `lambda` function handles unmapped clusters by assigning a fallback label (`Other_<cluster_id>`), ensuring no spots are silently dropped.

> **💡 Tip:** Manual annotation is subjective and depends on the annotator's domain expertise. This is why Section 19 cross-validates these labels with an automated method (CellTypist)."""))

cells.append(md(r"""### 📊 Expected Output

A UMAP plot colored by cell-type labels (e.g., "Tumor Cells", "Immune/B-Cells", "Stromal/Fibroblasts") instead of numeric cluster IDs."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Map cluster numbers to cell-type labels based on marker genes
# ──────────────────────────────────────────────────────────────────────

# Mapping derived from marker gene inspection (Section 10)
cell_type_mapping = {
    "0": "Tumor Cells",
    "8": "Tumor Cells",
    "2": "Immune/B-Cells",
    "7": "Immune/B-Cells",
    "1": "Stromal/Fibroblasts",
    "9": "Stromal/Fibroblasts",
}

# Unmapped clusters get a fallback label (not silently dropped)
adata_bc.obs["cell_type"] = adata_bc.obs["clusters"].map(
    lambda cluster_id: cell_type_mapping.get(cluster_id, f"Other_{cluster_id}")
)

sc.pl.umap(adata_bc, color="cell_type", title="Annotated Cell Types", palette="Set1")"""))

cells.append(md(r"""### 🔍 Result Interpretation

The UMAP should now show biologically meaningful groups:

- **Tumor Cells** should form a large, cohesive cluster (reflecting the dominant cell population in a tumor section)
- **Immune/B-Cells** should separate clearly from tumor cells
- **Stromal/Fibroblasts** should occupy a distinct UMAP region
- **"Other" clusters** may represent transitional states, rare populations, or mixed tissue

> **📌 Key Insight:** This annotation will be used as the basis for downstream analyses: cell–cell communication (Section 15), ML classification (Section 23), and deconvolution (Section 24).

---

### ⚠️ Common Mistakes

> **Force-annotating ambiguous clusters:** If marker genes are unclear, label as "Other" or "Unknown" rather than guessing. Incorrect labels propagate errors to all downstream analyses.

> **Not using multiple markers:** Never assign a cell type based on a single gene. Always confirm with a panel of 3–5 markers.

---

### 📋 Section Summary

- Manual annotation maps **cluster numbers** to **biological identities** using marker gene evidence
- The mapping is **conservative** — ambiguous clusters get fallback labels
- Three major types identified: **Tumor Cells, Immune/B-Cells, Stromal/Fibroblasts**
- These labels are used in all subsequent biological analyses
- Automated validation (CellTypist) in Section 19 provides an independent cross-check

---

### ✏️ Exercises

1. **Conceptual:** What are the advantages and disadvantages of manual vs. automated annotation?
2. **Coding:** Plot the annotated cell types spatially using `sq.pl.spatial_scatter(adata_bc, color="cell_type")`. Do the labels match the tissue morphology?
3. **Conceptual:** If you had access to a pathologist's annotations of this H&E image, how would you use them to validate your cell-type assignments?
4. **Coding:** How many spots are assigned to each cell type? Print `adata_bc.obs["cell_type"].value_counts()`.

---

### 📚 Further Reading

- Abdelaal, T. et al. *A comparison of automatic cell identification methods for single-cell RNA sequencing data.* Genome Biol. **20**, 194 (2019). [DOI](https://doi.org/10.1186/s13059-019-1795-z)
- Clarke, Z. A. et al. *Tutorial: guidelines for annotating single-cell transcriptomic maps.* Nat. Protoc. **16**, 2749–2764 (2021). [DOI](https://doi.org/10.1038/s41596-021-00534-0)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 15: LIANA
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 15. Ligand–Receptor Communication (LIANA)

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain the concept of ligand–receptor cell–cell communication
- Describe how LIANA aggregates multiple interaction scoring methods
- Interpret a LIANA dot plot showing top-ranked interactions
- Generate hypotheses about tumor–immune crosstalk from communication analysis

---

### 🧬 Biological Background

Cells in a tissue do not act in isolation — they communicate through **ligand–receptor (L–R) interactions**. A cell secretes a **ligand** (a signaling molecule) that binds to a **receptor** on a neighboring cell, triggering a downstream response.

In cancer biology, these interactions are particularly important:
- **Tumor → Immune:** Tumor cells may secrete immunosuppressive ligands (e.g., PD-L1) to evade immune detection
- **Immune → Tumor:** Immune cells may release cytokines that either attack or, paradoxically, promote tumor growth
- **Tumor → Stroma:** Tumor cells recruit fibroblasts that remodel the extracellular matrix

---

### 💻 Computational Background

**LIANA** (LIgand-receptor ANAlysis) is a framework that:

1. Uses curated databases of known ligand–receptor pairs
2. Scores each interaction for specificity and magnitude using multiple methods
3. Ranks interactions between specified source and target cell types

The dot plot displays:
- **Y-axis:** Ligand–receptor pairs (e.g., "MIF → CD74")
- **Color:** Magnitude rank (how strongly the interaction is expressed)
- **Size:** Specificity rank (how specific the interaction is to the cell-type pair)

> **📌 Note:** LIANA is installed inline because it is not a core dependency of the pipeline."""))

cells.append(md(r"""### 📊 Expected Output

A dot plot showing the top 20 ligand–receptor interactions from Tumor Cells (source) to Immune/B-Cells (target), ranked by magnitude."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Ligand–receptor communication analysis with LIANA
# ──────────────────────────────────────────────────────────────────────
!pip install -q liana

import liana as li

liana_plot = li.pl.dotplot(
    adata_bc,
    source_labels=["Tumor Cells"],
    target_labels=["Immune/B-Cells"],
    colour="magnitude_rank",
    size="specificity_rank",
    top_n=20,
    orderby="magnitude_rank",
    orderby_ascending=True,
    figure_size=(12, 8),
)
liana_plot"""))

cells.append(md(r"""### 🔍 Result Interpretation

Look for:

- **Known cancer-immune interactions:** Pairs like MIF–CD74, APP–CD74, or HLA-related interactions suggest active immune engagement with the tumor
- **Highly ranked interactions** (top of the plot) are both strongly expressed and specific to this cell-type pair
- **Novel or unexpected pairs** may represent interesting biology worth following up with experimental validation

> **📌 Key Insight:** Communication analysis generates **hypotheses**, not proof. Each predicted interaction needs independent experimental validation (e.g., immunohistochemistry, functional assays).

---

### ⚠️ Common Mistakes

> **Treating predictions as confirmed interactions:** LIANA predicts *potential* interactions based on co-expression of ligand and receptor genes. It does not confirm that the signaling pathway is active.

> **Ignoring interaction directionality:** "Tumor → Immune" and "Immune → Tumor" are different biological processes. Always consider which cell type is the source and which is the target.

---

### 📋 Section Summary

- **Ligand–receptor analysis** predicts cell–cell communication based on co-expression of signaling genes
- **LIANA** aggregates multiple scoring methods for robust ranking
- Top interactions between tumor and immune cells may reveal immune evasion or recruitment mechanisms
- Results are **hypotheses** that require experimental validation
- Directionality (source vs. target) matters biologically

---

### ✏️ Exercises

1. **Conceptual:** What is the difference between "magnitude rank" and "specificity rank"? When would you prioritize one over the other?
2. **Coding:** Change `source_labels` to `["Immune/B-Cells"]` and `target_labels` to `["Tumor Cells"]`. Do the top interactions differ when the direction is reversed?
3. **Conceptual:** Why might spatial transcriptomics be more appropriate for L–R analysis than dissociated scRNA-seq?
4. **Coding:** Run LIANA with all cell types as both source and target. Which cell-type pair has the most predicted interactions?

---

### 📚 Further Reading

- Dimitrov, D. et al. *Comparison of methods and resources for cell-cell communication inference from single-cell RNA-Seq data.* Nat. Commun. **13**, 3224 (2022). [DOI](https://doi.org/10.1038/s41467-022-30755-0)
- [LIANA documentation](https://liana-py.readthedocs.io/)
- Armingol, E. et al. *Deciphering cell–cell interactions and communication from gene expression.* Nat. Rev. Genet. **22**, 71–88 (2021). [DOI](https://doi.org/10.1038/s41576-020-00292-x)"""))

# ═══════════════════════════════════════════════════════════════════════
# PART V
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

# Part V — Multi-Modal & Advanced Analysis

> *Integrating histology images, pathways, automated annotation, spatial statistics, and trajectories*"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 16: HISTOLOGY FEATURES
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 16. Histology-Based Image Feature Extraction

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain why combining image and transcriptomic data is valuable
- Describe summary and texture features extracted from H&E images
- Understand how image features are stored in the AnnData object
- Interpret the extracted feature matrix

---

### 🧬 Biological Background

The H&E histology image contains rich morphological information that gene expression alone cannot capture:

- **Nuclear shape and size** vary between tumor and normal cells
- **Tissue texture** differs between dense tumor, loose stroma, and immune aggregates
- **Color intensity** reflects staining density, which correlates with cellularity

By extracting quantitative image features at each spot location, we create a **second modality** that can be compared, combined, or correlated with the transcriptomic data.

---

### 💻 Computational Background

Squidpy's `sq.im.calculate_image_features()` extracts two types of features from image patches centered on each spot:

| Feature Type | What It Measures | Example Features |
|-------------|-----------------|------------------|
| **Summary** | Basic pixel statistics | Mean, standard deviation per color channel |
| **Texture** | Spatial patterns (GLCM-based) | Homogeneity, contrast, correlation, energy |

These features are stored in `adata.obsm["image_features"]` as a DataFrame with one row per spot and one column per feature."""))

cells.append(md(r"""### 📊 Expected Output

A printed count of extracted features and a preview table (`.head()`) showing the first few spots and their image-derived features."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Extract image features from the H&E image at each spot location
# ──────────────────────────────────────────────────────────────────────
spatial_meta = adata_bc.uns["spatial"][SAMPLE_ID]

img = sq.im.ImageContainer(
    spatial_meta["images"]["hires"],
    scale=spatial_meta["scalefactors"]["tissue_hires_scalef"],
)

sq.im.calculate_image_features(
    adata_bc,
    img,
    features=["summary", "texture"],
    key_added="image_features",
    show_progress_bar=True,
)

features_df = adata_bc.obsm["image_features"]
print(f"Extracted {features_df.shape[1]} image-derived features per spot.")
features_df.head()"""))

cells.append(md(r"""### 🔍 Result Interpretation

The feature matrix should contain ~30–50 features per spot, including:

- **Summary features:** Mean intensity per channel — reflects tissue density and staining
- **Texture features (GLCM):** Homogeneity (smoothness), contrast (local variation), energy (uniformity)

These features can now be compared with transcriptomic clusters (Section 17) to determine whether transcriptionally distinct regions also look morphologically different.

---

### ⚠️ Common Mistakes

> **Ignoring image resolution:** Features are extracted from the `hires` image. Using `lowres` would provide less spatial detail but faster computation.

> **Not scaling features:** Image features have different scales (e.g., mean pixel value 0–255 vs. GLCM features 0–1). Normalize before combining with expression data.

---

### 📋 Section Summary

- H&E images contain **morphological information** complementary to gene expression
- Squidpy extracts **summary** (pixel statistics) and **texture** (GLCM) features per spot
- Features are stored in `adata.obsm["image_features"]`
- These features enable **multi-modal analysis** combining image and transcriptomic data
- ~30–50 features are extracted per spot

---

### ✏️ Exercises

1. **Conceptual:** What biological information might tissue texture capture that gene expression cannot?
2. **Coding:** Print the column names of `features_df`. Can you identify which columns correspond to summary vs. texture features?
3. **Conceptual:** How would deep learning-based features (e.g., from a pretrained ResNet) differ from these handcrafted GLCM features?
4. **Coding:** Compute the correlation between `total_counts` and one of the summary features. Are they related?

---

### 📚 Further Reading

- [Squidpy image features tutorial](https://squidpy.readthedocs.io/en/stable/auto_tutorials/tutorial_image_container.html)
- Haralick, R. M. et al. *Textural features for image classification.* IEEE Trans. Syst. Man Cybern. **3**, 610–621 (1973). [DOI](https://doi.org/10.1109/TSMC.1973.4309314)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 17: FUSING HISTOLOGY + TRANSCRIPTOMICS
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 17. Fusing Histology and Transcriptomics

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Visually compare transcriptomic clusters with image-derived tissue features
- Assess cross-modal consistency (does gene expression agree with tissue morphology?)
- Interpret tissue homogeneity as a proxy for structural organization

---

### 🧬 Biological Background

If transcriptomic clustering captures real tissue biology, then transcriptionally distinct regions should also look structurally different under the microscope. This section performs a **cross-modal validation**:

- **Transcriptomic view:** Leiden clusters (biology inferred from gene expression)
- **Histology view:** Tissue homogeneity (structure inferred from H&E image)

Concordance between these independent modalities strengthens confidence in both the clustering and the image feature extraction.

---

### 💻 Computational Background

Tissue **homogeneity** is a GLCM (Grey-Level Co-occurrence Matrix) texture feature that measures how uniform the pixel intensities are in a local neighborhood:

- **High homogeneity** → smooth, uniform tissue (e.g., dense tumor core)
- **Low homogeneity** → heterogeneous, textured tissue (e.g., mixed stroma with varied cell types)"""))

cells.append(md(r"""### 📊 Expected Output

Two side-by-side spatial plots: Leiden clusters (left) and tissue homogeneity (right). Regions that stand out in the cluster map should also show distinct texture patterns."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Cross-modal comparison: clusters vs. tissue texture
# ──────────────────────────────────────────────────────────────────────
homogeneity_col = "texture_ch-2_homogeneity_dist-1_angle-0.00"

if homogeneity_col in adata_bc.obsm["image_features"].columns:
    adata_bc.obs["tissue_homogeneity"] = adata_bc.obsm["image_features"][homogeneity_col]

    sq.pl.spatial_scatter(
        adata_bc,
        color=["clusters", "tissue_homogeneity"],
        cmap="magma",
        figsize=(12, 5),
        title=["Biology: Leiden Clusters", "AI Vision: Tissue Homogeneity"],
    )
    plt.show()
else:
    print(f"Expected texture feature '{homogeneity_col}' not found in extracted image features.")"""))

cells.append(md(r"""### 🔍 Result Interpretation

Compare the two panels:

- If cluster boundaries **align** with homogeneity transitions → strong cross-modal validation
- The **tumor core** (dense, uniform tissue) typically shows high homogeneity
- **Stromal regions** (mixed cell types, loose connective tissue) show lower homogeneity
- **Immune aggregates** may appear as local texture anomalies

---

### ⚠️ Common Mistakes

> **Expecting perfect correspondence:** Transcriptomics and morphology capture different aspects of biology. Partial disagreement is normal and can be biologically informative.

---

### 📋 Section Summary

- **Cross-modal validation** compares transcriptomic clusters with image-derived features
- **Tissue homogeneity** reflects structural uniformity visible in H&E
- Concordance strengthens confidence in both the clustering and feature extraction
- Disagreement may reveal areas where morphology and expression tell different stories

---

### ✏️ Exercises

1. **Coding:** Plot other texture features (contrast, energy) alongside clusters. Which feature shows the best correspondence?
2. **Conceptual:** Give an example where transcriptomic clusters and tissue morphology might *disagree*. What would that mean biologically?
3. **Coding:** Compute the correlation between homogeneity and expression of a tumor marker (e.g., CCND1). Is there a relationship?

---

### 📚 Further Reading

- He, B. et al. *Integrating spatial gene expression and breast tumour morphology via deep learning.* Nat. Biomed. Eng. **4**, 827–834 (2020). [DOI](https://doi.org/10.1038/s41551-020-0578-x)
- [Squidpy image analysis documentation](https://squidpy.readthedocs.io/en/stable/api/image.html)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 18: GSEA
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 18. Pathway Enrichment Analysis (GSEA)

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain the concept of gene set enrichment and over-representation analysis
- Interpret pathway enrichment results in the context of immune biology
- Use the gseapy library to query KEGG and GO databases
- Translate gene-level results into pathway-level biological insights

---

### 🧬 Biological Background

Individual genes are difficult to interpret in isolation. **Pathway enrichment analysis** asks: "Are the marker genes for a cluster enriched for specific biological pathways?"

For the immune cluster, we expect enrichment in:
- **Antigen processing and presentation** (KEGG pathway)
- **B cell receptor signaling** (KEGG pathway)
- **Immune response** (GO Biological Process)
- **Immunoglobulin production** (GO Biological Process)

This translates a list of genes into **functional insights** — telling us *what* the immune cells are doing, not just which genes they express.

---

### 💻 Computational Background

**Over-Representation Analysis (ORA)** tests whether the marker genes for a cluster overlap with curated gene sets (pathways) more than expected by chance. The test uses the hypergeometric distribution (Fisher's exact test).

We query two databases:
- **KEGG 2021 Human** — metabolic and signaling pathways
- **GO Biological Process 2021** — biological functions and processes

> **📌 Note:** gseapy connects to the Enrichr web API. An internet connection is required."""))

cells.append(md(r"""### 📊 Expected Output

A horizontal bar chart showing the top 15 enriched pathways, ranked by P-value. Immune-related pathways should dominate for the immune cluster."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Pathway enrichment for the immune cluster
# ──────────────────────────────────────────────────────────────────────
!pip install -q gseapy
import gseapy as gp

immune_cluster = "2"
if immune_cluster in adata_bc.uns["rank_genes_groups"]["names"].dtype.names:
    immune_genes = adata_bc.uns["rank_genes_groups"]["names"][immune_cluster][:150].tolist()

    enrichment_results = gp.enrichr(
        gene_list=immune_genes,
        gene_sets=["KEGG_2021_Human", "GO_Biological_Process_2021"],
        organism="human",
        outdir=None,
    )

    gp.plot.barplot(
        enrichment_results.results,
        column="P-value",
        title="Pathways Activated in Immune Cells",
        top_term=15,
        figsize=(10, 8),
        color="darkred",
    )
    plt.show()
else:
    print(f"Cluster '{immune_cluster}' not found among ranked gene groups.")"""))

cells.append(md(r"""### 🔍 Result Interpretation

The bar chart should show immune-related pathways at the top:

- **B cell receptor signaling** confirms the IGKC+ identity of this cluster
- **Antigen processing** suggests active immune surveillance
- **Cytokine-cytokine interaction** indicates immune cell communication
- **Primary immunodeficiency** may appear because many immune genes are enriched

> **📌 Key Insight:** Pathway analysis converts a **gene list** into a **biological narrative**. Instead of "these 150 genes are upregulated," we can say "this cluster is actively engaged in antigen presentation and B-cell signaling."

---

### ⚠️ Common Mistakes

> **Using too few genes:** Over-representation analysis needs a sufficiently large gene list (~50–200) to detect enrichment. Too few genes reduce statistical power.

> **Ignoring multiple testing:** With hundreds of pathways tested, some will appear significant by chance. Look for pathways with strong P-values *and* biological plausibility.

---

### 📋 Section Summary

- Pathway enrichment translates **gene lists** into **biological functions**
- ORA tests whether marker genes overlap with known pathways more than expected by chance
- **KEGG** and **GO** are complementary databases (metabolic/signaling vs. biological processes)
- Results should be interpreted with domain knowledge — statistical significance ≠ biological significance
- The immune cluster should show enrichment for immune-related pathways

---

### ✏️ Exercises

1. **Coding:** Run enrichment analysis for the tumor cluster instead of the immune cluster. What pathways are enriched?
2. **Conceptual:** What is the difference between ORA and GSEA (Gene Set Enrichment Analysis)? When would you use each?
3. **Coding:** Try using only the top 50 instead of 150 genes. How do the results change?
4. **Conceptual:** Why might "Primary immunodeficiency" appear as enriched in an immune cluster? Is this a biological finding or a statistical artifact?

---

### 📚 Further Reading

- Subramanian, A. et al. *Gene set enrichment analysis: A knowledge-based approach.* PNAS **102**, 15545–15550 (2005). [DOI](https://doi.org/10.1073/pnas.0506580102)
- [gseapy documentation](https://gseapy.readthedocs.io/)
- [Enrichr web tool](https://maayanlab.cloud/Enrichr/)
- Kanehisa, M. & Goto, S. *KEGG: Kyoto Encyclopedia of Genes and Genomes.* Nucleic Acids Res. **28**, 27–30 (2000). [DOI](https://doi.org/10.1093/nar/28.1.27)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 19: CELLTYPIST
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 19. Automated Cell-Type Annotation (CellTypist)

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain how reference-based automated annotation works
- Describe the CellTypist majority voting approach
- Compare automated and manual annotations for cross-validation
- Assess when to trust automated vs. manual labels

---

### 🧬 Biological Background

Manual annotation (Section 14) depends on the annotator's expertise and may be subjective. **Automated annotation** provides an independent, reproducible, reference-based second opinion:

- CellTypist uses a **pretrained logistic regression model** built from large immune cell atlases
- The model has "seen" hundreds of immune cell subtypes during training
- It classifies each spot based on its expression profile alone — no spatial information used

**Majority voting** smooths noisy per-spot predictions: after initial classification, each spot's label is refined based on what its neighbors (in expression space) were classified as.

---

### 💻 Computational Background

CellTypist workflow:
1. **Download** a pretrained model (here: `Immune_All_Low.pkl` — trained on immune cell subtypes)
2. **Classify** each spot independently using logistic regression
3. **Refine** with majority voting over expression neighbors
4. Store predictions in `adata.obs["auto_cell_type"]`

> **📌 Note:** CellTypist's immune model works best for immune cells. Non-immune spots (tumor, stroma) may receive imprecise or "best-guess" immune labels."""))

cells.append(md(r"""### 📊 Expected Output

A spatial plot colored by CellTypist-predicted cell types. Immune regions should receive specific immune subtype labels (e.g., "B cells", "Plasma cells"), while non-immune regions may receive less specific labels."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Automated cell-type annotation with CellTypist
# ──────────────────────────────────────────────────────────────────────
!pip install -q celltypist
import celltypist
from celltypist import models

models.download_models(force_update=False, model=["Immune_All_Low.pkl"])

predictions = celltypist.annotate(adata_bc, model="Immune_All_Low.pkl", majority_voting=True)
adata_bc.obs["auto_cell_type"] = predictions.predicted_labels["majority_voting"]

sc.pl.spatial(adata_bc, color="auto_cell_type", title="Automated Annotation (CellTypist)")"""))

cells.append(md(r"""### 🔍 Result Interpretation

Compare CellTypist results with your manual annotations:

- **Agreement** in immune regions (both methods call them immune/B-cells) → high confidence in the immune annotation
- **Disagreement** in non-immune regions is expected — CellTypist's immune model will try to assign immune labels to tumor/stromal spots
- **Subtype resolution:** CellTypist may identify specific subtypes (e.g., "Plasma cells" vs. "Memory B cells") that manual annotation missed

> **📌 Key Insight:** The best practice is to use **both** manual and automated annotation and investigate any discrepancies. Agreement increases confidence; disagreement highlights areas needing closer investigation.

---

### ⚠️ Common Mistakes

> **Using the wrong reference model:** CellTypist has many models. Using an immune model on a purely epithelial dataset will produce poor results. Always choose a model appropriate for your tissue.

> **Trusting automated labels blindly:** Automated methods are only as good as their training data. Always cross-validate with independent evidence (marker genes, spatial patterns).

---

### 📋 Section Summary

- **CellTypist** provides automated, reference-based cell-type annotation
- The `Immune_All_Low` model is trained on large immune cell atlases
- **Majority voting** smooths noisy per-spot predictions using expression neighbors
- Automated annotation serves as a **cross-validation** of manual labels
- Expect good performance on immune cells, poorer performance on non-immune cells

---

### ✏️ Exercises

1. **Coding:** Print `adata_bc.obs["auto_cell_type"].value_counts()` to see the distribution of predicted cell types. How many unique types did CellTypist assign?
2. **Conceptual:** Why might CellTypist assign immune labels to spots that are clearly in the tumor core?
3. **Coding:** Compare manual and automated labels for immune cluster spots: `adata_bc.obs.loc[adata_bc.obs["cell_type"] == "Immune/B-Cells", "auto_cell_type"].value_counts()`. What subtypes does CellTypist identify?
4. **Coding:** Try using a different CellTypist model (e.g., `Immune_All_High.pkl`). How do the predictions change?

---

### 📚 Further Reading

- Domínguez Conde, C. et al. *Cross-tissue immune cell analysis reveals tissue-specific features in humans.* Science **376**, eabl5197 (2022). [DOI](https://doi.org/10.1126/science.abl5197)
- [CellTypist documentation](https://www.celltypist.org/)
- [CellTypist model gallery](https://www.celltypist.org/models)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 20: CO-OCCURRENCE & AUTOCORRELATION
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 20. Spatial Co-occurrence & Autocorrelation

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain the difference between co-occurrence analysis and neighborhood enrichment
- Interpret a co-occurrence curve showing distance-dependent co-localization
- Describe Moran's I as a measure of spatial autocorrelation
- Apply spatial statistics to validate marker gene spatial patterns

---

### 🧬 Biological Background

This section provides two complementary **spatial statistics**:

**1. Co-occurrence analysis** — measures how the probability of finding a tumor spot changes as you move away from an immune spot (and vice versa). Unlike neighborhood enrichment (Section 12), which only considers immediate neighbors, co-occurrence examines relationships across multiple distance scales.

**2. Moran's I** — measures whether a gene's expression is **spatially clustered** (positive Moran's I), **spatially dispersed** (negative), or **randomly distributed** (~0). A high Moran's I for CCND1 confirms that tumor marker expression forms coherent spatial domains, not random speckles.

---

### 💻 Computational Background

| Statistic | Question Answered | Range |
|-----------|-------------------|-------|
| **Co-occurrence** | How does cluster X neighbor cluster Y at different distances? | Probability ratio |
| **Moran's I** | Is gene X expression spatially autocorrelated? | −1 to +1 |

Both methods use the **spatial neighbor graph** built in Section 12 (not recomputed).

Moran's I uses a **permutation test** (100 permutations) to assess statistical significance — shuffling expression values across spots and comparing real spatial clustering to the random expectation."""))

cells.append(md(r"""### 📊 Expected Output

1. A co-occurrence curve for clusters "0" (tumor) and "2" (immune)
2. A printed table of Moran's I values for CCND1, IGKC, and MIF"""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Spatial co-occurrence and Moran's I autocorrelation
# ──────────────────────────────────────────────────────────────────────

# Reuse the spatial neighbor graph from Section 12
if "spatial_neighbors" not in adata_bc.uns:
    sq.gr.spatial_neighbors(adata_bc)

sq.gr.co_occurrence(adata_bc, cluster_key="clusters")
sq.pl.co_occurrence(
    adata_bc,
    cluster_key="clusters",
    clusters=["0", "2"],
    figsize=(10, 4),
)
plt.show()

# Moran's I: spatial autocorrelation for key marker genes
target_genes = ["CCND1", "IGKC", "MIF"]
valid_genes = [g for g in target_genes if g in adata_bc.var_names]

if valid_genes:
    sq.gr.spatial_autocorr(adata_bc, mode="moran", genes=valid_genes, n_perms=100, n_jobs=-1)
    print("Moran's I results:")
    print(adata_bc.uns["moranI"].head())
else:
    print(f"None of the requested genes {target_genes} were found in the dataset.")"""))

cells.append(md(r"""### 🔍 Result Interpretation

**Co-occurrence curve:**
- A ratio > 1 indicates that the two clusters **co-occur more than expected** at that distance
- A ratio < 1 indicates **spatial avoidance**
- The shape of the curve reveals whether co-localization is a **short-range** (only immediate neighbors) or **long-range** phenomenon

**Moran's I:**
- **CCND1** (tumor marker): expect high positive Moran's I → spatially clustered expression
- **IGKC** (immune marker): expect positive Moran's I → immune cells form spatial clusters
- **MIF** (cytokine): may show moderate Moran's I → expressed in specific tissue regions
- Values near 0 indicate random spatial distribution

---

### ⚠️ Common Mistakes

> **Confusing co-occurrence with correlation:** Co-occurrence measures spatial proximity, not expression correlation. Two clusters can co-occur spatially but have uncorrelated gene expression.

> **Not running enough permutations for Moran's I:** 100 permutations is acceptable for exploration; use 1000+ for publication-quality P-values.

---

### 📋 Section Summary

- **Co-occurrence** quantifies distance-dependent spatial relationships between clusters
- **Moran's I** measures whether gene expression is spatially clustered or random
- Both methods use the **spatial neighbor graph** (not the expression kNN graph)
- High Moran's I confirms that marker genes form **coherent spatial domains**
- These spatial statistics are unique advantages of spatial over dissociated scRNA-seq

---

### ✏️ Exercises

1. **Conceptual:** What would a Moran's I near 0 mean for a gene like CCND1? Would that change your interpretation of the tumor cluster?
2. **Coding:** Compute Moran's I for 5 additional genes of your choice. Which has the strongest spatial pattern?
3. **Conceptual:** If co-occurrence between tumor and immune clusters peaks at short distances and drops at longer distances, what tissue architecture does that suggest?
4. **Coding:** Plot co-occurrence for different cluster pairs (e.g., stroma-immune). Does the pattern differ from tumor-immune?

---

### 📚 Further Reading

- Moran, P. A. P. *Notes on continuous stochastic phenomena.* Biometrika **37**, 17–23 (1950). [DOI](https://doi.org/10.2307/2332142)
- [Squidpy spatial statistics tutorial](https://squidpy.readthedocs.io/en/stable/auto_tutorials/tutorial_spatial_statistics.html)
- Anselin, L. *Local indicators of spatial association — LISA.* Geogr. Anal. **27**, 93–115 (1995). [DOI](https://doi.org/10.1111/j.1538-4632.1995.tb00338.x)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 21: PAGA
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 21. Cell Trajectory Analysis (PAGA)

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain the concept of cell trajectories and pseudotime
- Describe how PAGA constructs a connectivity graph between clusters
- Interpret PAGA graphs and force-directed layouts
- Understand when trajectory analysis is appropriate for spatial data

---

### 🧬 Biological Background

**Cell trajectories** describe continuous transitions between cell states. In a tumor, these transitions might represent:

- **Epithelial-to-mesenchymal transition (EMT):** tumor cells acquiring stromal-like properties
- **Immune activation gradients:** resting → activated immune cells
- **Stromal remodeling:** normal fibroblasts → cancer-associated fibroblasts

**PAGA** (Partition-based Graph Abstraction) infers a coarse-grained connectivity graph where:
- Nodes = clusters
- Edge weight = strength of connection (how many cells transition between clusters)
- Thick edges = strong transitions; Thin/absent edges = distinct populations

---

### 💻 Computational Background

PAGA works by:
1. Using the kNN graph built in Section 9
2. Testing whether connections between clusters are stronger than expected by random
3. Producing a connectivity graph that can seed a **force-directed layout** — a continuous embedding initialized by the PAGA topology

> **📌 Note:** PAGA was originally designed for scRNA-seq developmental trajectories. In spatial data, "trajectories" may represent spatial gradients rather than temporal development."""))

cells.append(md(r"""### 📊 Expected Output

Two plots:
1. A **PAGA graph** showing cluster connectivity (thicker edges = stronger connections)
2. A **force-directed graph** colored by cluster, initialized from the PAGA topology"""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# PAGA trajectory analysis
# ──────────────────────────────────────────────────────────────────────
sc.tl.paga(adata_bc, groups="clusters")
sc.pl.paga(adata_bc, color="clusters", title="Trajectory Analysis (PAGA)")

sc.tl.draw_graph(adata_bc, init_pos="paga", random_state=RANDOM_STATE)
sc.pl.draw_graph(adata_bc, color="clusters", legend_loc="on data", title="Continuous Cell Trajectory")"""))

cells.append(md(r"""### 🔍 Result Interpretation

**PAGA graph:**
- Clusters connected by **thick edges** share many transitional cells — they may represent related cell states
- **Isolated clusters** (thin or no edges) are transcriptomically distinct populations
- Tumor-stroma connections may indicate an **invasive front** with transitional gene expression

**Force-directed layout:**
- Preserves the PAGA topology while placing spots in a continuous 2D embedding
- Clusters that were connected in PAGA should flow into each other in the layout
- This view emphasizes **gradients** rather than discrete boundaries

---

### ⚠️ Common Mistakes

> **Interpreting trajectories as temporal order:** In spatial data, connected clusters may be spatially adjacent rather than developmentally related. Context is critical.

> **Over-interpreting edge weights:** PAGA edge weights depend on clustering resolution. Different resolutions produce different connectivity graphs.

---

### 📋 Section Summary

- **PAGA** infers coarse-grained connectivity between clusters
- Thick edges indicate **strong transitions** or shared transcriptional programs
- The force-directed layout provides a **continuous** view complementary to UMAP
- In spatial data, "trajectories" often represent **spatial gradients**, not developmental time
- PAGA initializes the embedding, producing a more biologically meaningful layout

---

### ✏️ Exercises

1. **Conceptual:** How would you distinguish a true developmental trajectory from a spatial gradient using PAGA?
2. **Coding:** Color the force-directed graph by `cell_type` instead of `clusters`. Are the trajectory relationships consistent with the biological annotations?
3. **Conceptual:** If two clusters are spatially adjacent but not connected in PAGA, what does that suggest about their relationship?
4. **Coding:** Try `sc.tl.dpt(adata_bc)` to compute pseudotime along the trajectory. Which cluster is at the "root" and which is at the "tip"?

---

### 📚 Further Reading

- Wolf, F. A. et al. *PAGA: graph abstraction reconciles clustering with trajectory inference through a topology preserving map of single cells.* Genome Biol. **20**, 59 (2019). [DOI](https://doi.org/10.1186/s13059-019-1663-x)
- [Scanpy trajectory tutorial](https://scanpy-tutorials.readthedocs.io/en/latest/paga-paul15.html)"""))

# ═══════════════════════════════════════════════════════════════════════
# PART VI
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

# Part VI — Export & Machine Learning

> *Saving results, training classifiers, and deconvolving multi-cellular spots*"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 22: EXPORT
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 22. Exporting Processed Outputs

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Save processed AnnData objects in the standard h5ad format
- Export spot metadata and marker gene tables as CSV files
- Organize outputs into a structured directory hierarchy
- Understand why checkpointing intermediate results is important

---

### 🧬 Biological Background

Computational reproducibility requires that processed results can be **reloaded without rerunning the entire pipeline**. This is essential for:

- **Sharing results** with collaborators who may not have all dependencies installed
- **Downstream analyses** in separate scripts or notebooks (dashboards, reports)
- **Version control** — tracking how results change as parameters are refined

---

### 💻 Computational Background

Three outputs are saved:

| File | Format | Contents |
|------|--------|----------|
| `processed_spatial.h5ad` | HDF5-backed AnnData | Complete processed dataset (expression, metadata, embeddings) |
| `metadata.csv` | CSV | Per-spot annotations (clusters, cell types, QC metrics) |
| `marker_genes.csv` | CSV | Ranked marker genes for each cluster |"""))

cells.append(md(r"""### 📊 Expected Output

A confirmation message listing the output directory. Three files should be created under `SpatialAIFlow_Outputs/data/`."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Save processed data and analysis results
# ──────────────────────────────────────────────────────────────────────
for subdir in ("data", "reports", "figures"):
    os.makedirs(os.path.join(OUTPUT_DIR, subdir), exist_ok=True)

adata_bc.write_h5ad(os.path.join(OUTPUT_DIR, "data", "processed_spatial.h5ad"))
adata_bc.obs.to_csv(os.path.join(OUTPUT_DIR, "data", "metadata.csv"))

markers_df = sc.get.rank_genes_groups_df(adata_bc, group=None)
markers_df.to_csv(os.path.join(OUTPUT_DIR, "data", "marker_genes.csv"), index=False)

print(f"All outputs saved under '{OUTPUT_DIR}/'.")"""))

cells.append(md(r"""### 🔍 Result Interpretation

Verify the outputs by checking:
- File sizes (h5ad should be several MB; CSVs should be non-empty)
- That the h5ad can be reloaded: `adata_reload = sc.read_h5ad("SpatialAIFlow_Outputs/data/processed_spatial.h5ad")`

---

### ⚠️ Common Mistakes

> **Not creating directories first:** `write_h5ad` will fail if the directory does not exist. Always use `os.makedirs(..., exist_ok=True)`.

> **Saving raw instead of processed data:** Make sure you save the *processed* AnnData object with all annotations, not the raw pre-filtered version.

---

### 📋 Section Summary

- Three output files: **h5ad** (complete dataset), **metadata CSV**, **marker genes CSV**
- Organized into `data/`, `reports/`, and `figures/` subdirectories
- **Checkpointing** enables reproducibility and downstream reuse
- The h5ad format preserves all AnnData components (expression, metadata, embeddings, spatial)

---

### ✏️ Exercises

1. **Coding:** Reload the saved h5ad file and verify that the cluster labels and UMAP coordinates are preserved.
2. **Coding:** Open `marker_genes.csv` and identify the top marker for each cluster.
3. **Conceptual:** Why save both an h5ad and CSV files? When would you use each?

---

### 📚 Further Reading

- [AnnData file format documentation](https://anndata.readthedocs.io/en/stable/fileformat-prose.html)
- [HDF5 format overview](https://www.hdfgroup.org/solutions/hdf5/)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 23: ML CLASSIFIER
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 23. Machine Learning Cell-Type Classifier

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Train a Random Forest classifier on spatial transcriptomics data
- Evaluate classification performance using accuracy and per-class metrics
- Explain why ML classification is useful for labeling new samples
- Interpret a classification report (precision, recall, F1-score)

---

### 🧬 Biological Background

Once cell types are annotated (Section 19), we can train a **machine learning model** to predict cell types from gene expression alone. This has practical applications:

- **Labeling new samples** quickly without rerunning the full annotation pipeline
- **Quantifying separability** — if a classifier achieves high accuracy, the cell types are well-defined in expression space
- **Identifying informative features** — Random Forest feature importances reveal which genes are most discriminative

---

### 💻 Computational Background

**Random Forest** is an ensemble of decision trees that:
1. Each tree is trained on a random subset of data and features (bagging)
2. Predictions are made by majority vote across all trees
3. Robust to overfitting, handles high-dimensional data well

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `n_estimators=100` | 100 trees | Good balance of accuracy and speed |
| `test_size=0.2` | 80/20 split | 20% held out for unbiased evaluation |
| `random_state=42` | Fixed seed | Reproducible train/test split |

The classification report includes:
- **Precision:** Of spots predicted as type X, what fraction are actually X?
- **Recall:** Of all actual type X spots, what fraction were correctly predicted?
- **F1-score:** Harmonic mean of precision and recall"""))

cells.append(md(r"""### 📊 Expected Output

A printed accuracy score and a per-class classification report showing precision, recall, and F1-score for each cell type. A saved model file (`spatial_cell_classifier.pkl`)."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Train a Random Forest classifier on cell-type labels
# ──────────────────────────────────────────────────────────────────────
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

X = adata_bc.to_df()
y = adata_bc.obs["auto_cell_type"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)

print("Training Random Forest classifier...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Test accuracy: {accuracy * 100:.2f}%\n")
print("Classification report:")
import seaborn as sns
import matplotlib.pyplot as plt

# Extract and plot feature importances
importances = rf_model.feature_importances_
top_indices = np.argsort(importances)[::-1][:20]
top_genes = X.columns[top_indices]
top_importances = importances[top_indices]

plt.figure(figsize=(10, 6))
sns.barplot(x=top_importances, y=top_genes, palette="viridis")
plt.title("Top 20 Random Forest Feature Importances")
plt.xlabel("Importance")
plt.show()

model_path = os.path.join(OUTPUT_DIR, "data", "spatial_cell_classifier.pkl")
joblib.dump(rf_model, model_path)
print(f"Model saved to: {model_path}")"""))

cells.append(md(r"""### 🔍 Result Interpretation

- **High accuracy (>85%)** → cell types are well-separated in expression space, and the classifier can reliably distinguish them
- **Per-class metrics:**
  - Low recall for a cell type → those spots are being confused with another type (check which one)
  - Low precision → the model is over-predicting that cell type
- **Rare cell types** may have lower metrics due to insufficient training examples

> **📌 Key Insight:** The classifier's accuracy is also a **validation metric** for the cell-type annotations themselves. If the classifier can easily learn the labels, the labels capture real transcriptional differences.

---

### ⚠️ Common Mistakes

> **Not using a held-out test set:** Evaluating on training data gives inflated accuracy. Always use a train/test split.

> **Class imbalance:** If one cell type dominates (e.g., 70% tumor), accuracy alone is misleading. Check per-class precision and recall.

> **Feature leakage:** Ensure the test set was not used during any normalization or feature selection step. In this pipeline, HVG selection and normalization are done on the full dataset (acceptable for exploratory analysis, not for production ML).

---

### 📋 Section Summary

- A **Random Forest classifier** is trained to predict cell types from gene expression
- **80/20 train/test split** provides unbiased evaluation
- The classification report reveals per-class strengths and weaknesses
- High accuracy validates that cell-type annotations capture **real transcriptional differences**
- The saved model can be applied to **new samples** without rerunning the annotation pipeline

---

### ✏️ Exercises

1. **Coding:** Extract feature importances with `rf_model.feature_importances_` and identify the top 10 most important genes. Do they match the marker genes from Section 10?
2. **Coding:** Create a confusion matrix with `sklearn.metrics.confusion_matrix`. Which cell types are most commonly confused?
3. **Conceptual:** Why might a Random Forest outperform logistic regression for this task? What about a neural network?
4. **Coding:** Try training with `n_estimators=500`. Does accuracy improve? Is the improvement worth the extra computation?
5. **Conceptual:** What precautions would you take before applying this classifier to a sample from a different patient?

---

### 📚 Further Reading

- Breiman, L. *Random Forests.* Mach. Learn. **45**, 5–32 (2001). [DOI](https://doi.org/10.1023/A:1010933404324)
- [scikit-learn Random Forest documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- Alquicira-Hernandez, J. et al. *scPred: accurate supervised method for cell-type classification from single-cell RNA-seq data.* Genome Biol. **20**, 264 (2019). [DOI](https://doi.org/10.1186/s13059-019-1862-5)"""))

# ═══════════════════════════════════════════════════════════════════════
# SECTION 24: TANGRAM
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 24. Multi-omics Spatial Deconvolution (Tangram)

### 🎯 Learning Objectives

After completing this section, you will be able to:

- Explain the cell-type deconvolution problem for multi-cellular spots
- Describe how Tangram maps single-cell data to spatial coordinates
- Interpret deconvolution results as per-spot cell-type proportions
- Understand the limitations of using the same dataset as reference and query

---

### 🧬 Biological Background

Each Visium spot covers ~55 μm and captures RNA from **multiple cells** (typically 5–30). The analyses so far have assigned a **single label** to each spot, but in reality, many spots contain a **mixture** of cell types — especially at tissue boundaries.

**Spatial deconvolution** estimates the proportion of each cell type within each spot. This transforms the "one label per spot" view into a **continuous composition map**:

- A spot labeled "Tumor" might actually be 70% tumor + 20% stroma + 10% immune
- Boundary spots might be 50/50 between adjacent compartments

---

### 💻 Computational Background

**Tangram** works by:
1. Taking a **single-cell reference** dataset (with known cell-type labels at single-cell resolution)
2. Learning a mapping from reference cells to spatial spots using an optimization procedure
3. Projecting cell-type annotations from the reference onto the spatial data

The mapping minimizes the difference between predicted and observed spatial gene expression, producing a per-spot **cell-type probability vector**.

> **⚠️ Important caveat:** In this notebook, the *same processed dataset* is used as both reference and query to demonstrate the method end-to-end. In a real study, you would use an **independently generated scRNA-seq** reference from the same tissue type.

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `mode="cells"` | Cell-level mapping | Maps individual reference cells to spatial spots |
| `density_prior="uniform"` | No prior on cell density | Assumes equal cell density across tissue |
| `num_epochs=500` | Training iterations | Balance between accuracy and runtime |
| `device="cpu"` | CPU computation | Change to `"cuda"` for GPU acceleration |"""))

cells.append(md(r"""### 📊 Expected Output

First cell: a confirmation that Tangram mapping is complete. Second cell: side-by-side spatial plots comparing the original single-label annotation with the Tangram-predicted density of a selected cell type."""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Tangram: map single-cell reference to spatial spots
# ──────────────────────────────────────────────────────────────────────
!pip install -q tangram-sc
import tangram as tg

print("Preparing data for Tangram mapping...")
adata_sc = adata_bc.copy()

# Align genes shared between the "reference" and spatial datasets
tg.pp_adatas(adata_sc, adata_bc, genes=None)

print("Training Tangram mapping model...")
ad_map = tg.map_cells_to_space(
    adata_sc,
    adata_bc,
    mode="cells",
    density_prior="uniform",
    num_epochs=500,
    device="cpu",
)

tg.project_cell_annotations(ad_map, adata_bc, annotation="auto_cell_type")
print("Tangram mapping complete.")"""))

cells.append(code(r"""# ──────────────────────────────────────────────────────────────────────
# Visualize deconvolution results
# ──────────────────────────────────────────────────────────────────────

# Expand per-cell-type predictions into individual obs columns
tangram_preds = adata_bc.obsm["tangram_ct_pred"]
for cell_type in tangram_preds.columns:
    adata_bc.obs[f"tangram_pred_{cell_type}"] = tangram_preds[cell_type]

# Prefer an epithelial/tumor-associated column if available
candidate_cols = [c for c in adata_bc.obs.columns if c.startswith("tangram_pred_")]
tumor_col = next(
    (c for c in candidate_cols if "epithelial" in c.lower() or "tumor" in c.lower()),
    None,
)

if tumor_col:
    sc.pl.spatial(
        adata_bc,
        color=["auto_cell_type", tumor_col],
        title=["Original Annotation (Single Modality)", f"Tangram-Predicted Density: {tumor_col.replace('tangram_pred_', '')}"],
        cmap="viridis",
        figsize=(12, 5),
    )
    plt.show()
    print("Multi-omics deconvolution complete.")
else:
    print(f"No tumor/epithelial column found. Available Tangram predictions: {candidate_cols}")"""))

cells.append(md(r"""### 🔍 Result Interpretation

Compare the two panels:

- **Left (Original annotation):** Each spot has a single categorical label
- **Right (Tangram prediction):** Each spot shows a continuous density value for the selected cell type

Key observations:
- High-density regions in the Tangram map should correspond to clusters labeled as that cell type
- **Boundary spots** should show intermediate densities — these are the multi-cellular spots that the single-label annotation couldn't fully capture
- The **gradient** from high to low density traces the transition zone between tissue compartments

> **📌 Key Insight:** Deconvolution transforms discrete labels into **continuous compositions**, revealing the heterogeneity *within* each spot that Visium's ~55 μm resolution hides.

---

### ⚠️ Common Mistakes

> **Using the same dataset as reference:** This is a methodological demonstration only. For real biological conclusions, always use an independently generated scRNA-seq reference.

> **Over-interpreting exact proportions:** Deconvolution provides estimates, not exact measurements. Small differences in predicted proportions may not be biologically meaningful.

> **Ignoring the reference quality:** Deconvolution is only as good as the reference. If the reference lacks a cell type present in the spatial data, it cannot be detected.

---

### 📋 Section Summary

- Each Visium spot contains **multiple cells** — deconvolution estimates per-spot cell-type proportions
- **Tangram** optimizes a mapping from single-cell reference to spatial spots
- The result is a **continuous composition map** replacing single labels with probability vectors
- In this notebook, the same dataset serves as its own reference (demonstration only)
- Real studies require an **independent scRNA-seq reference** for valid deconvolution

---

### ✏️ Exercises

1. **Conceptual:** Why is an independently generated scRNA-seq reference critical for real deconvolution studies?
2. **Coding:** Examine `adata_bc.obsm["tangram_ct_pred"]`. How many cell types does Tangram predict proportions for?
3. **Coding:** For a spot at the tumor-immune boundary, print its Tangram prediction vector. Does it show mixed proportions?
4. **Conceptual:** How would higher spatial resolution (e.g., 10 μm spots from Visium HD) affect the need for deconvolution?
5. **Coding:** Plot Tangram predictions for the immune cell type alongside the tumor predictions. Are they complementary (high immune where tumor is low)?

---

### 📚 Further Reading

- Biancalani, T. et al. *Deep learning and alignment of spatially resolved single-cell transcriptomes with Tangram.* Nat. Methods **18**, 1352–1362 (2021). [DOI](https://doi.org/10.1038/s41592-021-01264-7)
- [Tangram documentation](https://tangram-sc.readthedocs.io/)
- Cable, D. M. et al. *Robust decomposition of cell type mixtures in spatial transcriptomics.* Nat. Biotechnol. **40**, 517–526 (2022). [DOI](https://doi.org/10.1038/s41587-021-00830-w)
- Kleshchevnikov, V. et al. *Cell2location maps fine-grained cell types in spatial transcriptomics.* Nat. Biotechnol. **40**, 661–671 (2022). [DOI](https://doi.org/10.1038/s41587-021-01139-4)"""))

# ═══════════════════════════════════════════════════════════════════════
# CONCLUSION
# ═══════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

# 🎓 Conclusion

Congratulations! You have completed a full end-to-end spatial transcriptomics analysis pipeline.

## What You've Accomplished

| Section | Skill Acquired |
|---------|---------------|
| §1–3 | Environment setup, data loading, and raw data inspection |
| §4–7 | Quality control, normalization, and feature selection |
| §8–9 | Dimensionality reduction and unsupervised clustering |
| §10–13 | Marker gene identification, spatial validation, neighborhood analysis, and UMAP |
| §14–15 | Cell-type annotation and ligand–receptor communication |
| §16–17 | Multi-modal integration of histology and transcriptomics |
| §18 | Pathway enrichment analysis |
| §19 | Automated annotation with CellTypist |
| §20 | Spatial statistics (co-occurrence, Moran's I) |
| §21 | Trajectory analysis with PAGA |
| §22–24 | Data export, ML classification, and spatial deconvolution |

## Key Takeaways

1. **Spatial transcriptomics** adds location information to gene expression, enabling questions about tissue architecture
2. **Quality control** is the foundation — all downstream results depend on it
3. **Multiple validation approaches** (manual annotation, automated annotation, spatial statistics) increase confidence
4. **Multi-modal integration** (expression + histology) provides complementary biological insights
5. **Deconvolution** reveals within-spot heterogeneity hidden by the Visium resolution limit
6. **Reproducibility** (random seeds, checkpointing, clear documentation) is essential for trustworthy science

## Next Steps

- Apply this pipeline to **your own dataset**
- Experiment with **different parameters** (clustering resolution, QC thresholds, number of HVGs)
- Explore **newer spatial technologies** (Visium HD, MERFISH, Slide-seq) that offer higher resolution
- Read the **original papers** cited in each section's Further Reading

> **💡 Tip:** The best way to learn is to run this notebook on a different tissue type and compare the results.

---

*SpatialAIFlow — Making spatial transcriptomics analysis accessible, reproducible, and educational.*"""))

# ═══════════════════════════════════════════════════════════════════════
# BUILD THE NOTEBOOK
# ═══════════════════════════════════════════════════════════════════════
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notebooks", "SpatialAIFlow.ipynb")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("Notebook generated successfully!")
print(f"   Path: {output_path}")
print(f"   Total cells: {len(cells)}")
md_cells = sum(1 for c in cells if c["cell_type"] == "markdown")
code_cells = sum(1 for c in cells if c["cell_type"] == "code")
print(f"   Markdown cells: {md_cells}")
print(f"   Code cells: {code_cells}")
