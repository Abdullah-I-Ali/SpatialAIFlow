# SpatialAIFlow Demo Report

## 1. Dataset Used
- **Dataset:** 10x Genomics Visium Breast Cancer Block A, Section 1
- **Platform:** Visium Spatial Gene Expression
- **Characteristics:** Contains a heterogeneous mix of breast cancer tumor regions, stromal tissue, and immune infiltrates. The dataset perfectly demonstrates the power of spatial transcriptomics in resolving complex tissue microenvironments.

## 2. Successfully Completed Analyses
The pipeline successfully executed the following major analytical milestones:
- **Quality Control:** Filtered out damaged and empty spots using robust, data-driven thresholds (mitochondrial fraction <10%, minimum 1000 detected genes).
- **Preprocessing:** Performed library size normalization (10k counts per cell) and log1p transformation.
- **Feature Selection:** Identified and subset to highly variable genes (HVGs).
- **Dimensionality Reduction:** Computed PCA (50 components) and built spatial/transcriptomic neighborhood graphs.
- **Clustering:** Segregated the dataset into distinct tissue domains using Leiden clustering.
- **Marker Gene Identification:** Performed differential expression analysis to identify cluster-specific spatial signatures.
- **Cell Communication:** Mapped localized ligand-receptor interactions using `LIANA`, identifying key spatial communication pathways (e.g., COL1A1-CD44, MIF-CD74).
- **Machine Learning Integration:** Extracted computer vision features (color/texture) from the H&E image using `Squidpy` and fused them with transcriptomic data. Trained a Random Forest classifier to predict spatial niches, identifying transcriptomic principal components as top predictors.
- **Pathway Enrichment:** Successfully ran Gene Set Enrichment Analysis (GSEA) using `gseapy`, identifying enriched pathways (e.g., Hallmarks of Cancer) per cluster.
- **Automated Annotation:** Used `CellTypist` to automatically annotate immune populations in the dataset.

## 3. Generated Figures
All successfully generated figures are stored in `assets/figures/` in both PNG and SVG formats:
- `raw_data_visualization`: Spatial map of raw UMI counts overlaying H&E.
- `qc_violin`: Quality control distributions (genes, counts, mt%).
- `spatial_gene_expression`: Spatial expression of ERBB2, CD3E, etc.
- `umap_clusters`: Transcriptomic UMAP showing defined tissue clusters.
- `marker_genes_heatmap`: Top 5 marker genes per Leiden cluster.
- `neighborhood_enrichment`: Cell-type spatial co-occurrence map.
- `celltype_annotation`: Final tissue domain annotations (Tumor, Stroma, Immune).
- `cell_communication_network`: Ligand-Receptor interaction network.
- `histology_features`: Summary of extracted H&E image features.
- `pathway_dotplot`: Top enriched GSEA pathways per cluster.
- `trajectory_paga`: Spatial differentiation trajectories.
- `random_forest_feature_importance`: Predictors for spatial niche classification.

## 4. Skipped Sections
- **Multi-Omics Spatial Deconvolution (Tangram):** The Tangram workflow was skipped due to deep dependency conflicts between PyTorch, AnnData 0.11+, and NumPy 2.x. While the conceptual educational content remains, the code execution for Tangram deconvolution is bypassed to ensure the rest of the pipeline executes smoothly for learners.

## 5. Summary
The framework ran highly successfully, generating a rich, publication-ready spatial dataset. The educational notebook is robust and visually striking, achieving its goal of serving as an interactive textbook for Spatial Transcriptomics.
