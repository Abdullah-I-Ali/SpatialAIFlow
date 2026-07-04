# SpatialAIFlow Compatibility Report

This document records the external package compatibility issues encountered during the development and testing of SpatialAIFlow. The spatial transcriptomics ecosystem (`scverse`) evolves rapidly, often introducing breaking changes between core dependencies like `AnnData`, `Scanpy`, `Squidpy`, and downstream domain-specific tools.

## 1. Tangram Deconvolution
- **Package Name:** `tangram-sc`
- **Installed Version:** `1.0.4`
- **Compatible Version:** Older versions compatible with PyTorch <2.0 and AnnData <0.9 (e.g., `tangram-sc==1.0.3` with `anndata==0.8.0`)
- **Root Cause:** Tangram heavily relies on deep integration with PyTorch and older AnnData sparse matrix structures. The shift to NumPy 2.x and AnnData 0.11+ broke `X` matrix mappings, causing `RuntimeError` and `IndexError` during `tg.map_cells_to_space()`. Additionally, some internals depend on deprecated `scipy.sparse` behaviors.
- **Recommended Long-Term Solution:** Wait for a major Tangram update that explicitly supports AnnData >0.10 and NumPy 2.0. Alternatively, isolate the Tangram step into a separate, legacy Conda environment running Python 3.9, AnnData 0.8, and PyTorch 1.13.

## 2. CellTypist Annotation
- **Package Name:** `celltypist`
- **Installed Version:** `1.6.3`
- **Compatible Version:** Latest (`1.6.3`) requires specific workarounds.
- **Root Cause:** CellTypist attempts to cast expression data using legacy NumPy/Pandas methods that conflict with AnnData 0.11's stricter CSR sparse matrix handling. It also throws warnings due to deprecated `anndata.X` view operations.
- **Recommended Long-Term Solution:** We currently mitigate this by densifying (`adata.X.toarray()`) the subset of data passed to CellTypist or explicitly aligning features before annotation. The long-term fix will come when CellTypist natively supports NumPy 2.x sparse array standards.

## 3. LIANA Cell-Cell Communication
- **Package Name:** `liana`
- **Installed Version:** `1.4.0`
- **Compatible Version:** Latest (`1.4.0`) is functional with workarounds.
- **Root Cause:** LIANA expects `adata.obs` to strictly contain categorical data for grouping (e.g., cell types). Stricter Pandas 2.x categorical handling occasionally causes LIANA to fail if cluster labels are dynamically assigned as strings rather than properly cast categoricals.
- **Recommended Long-Term Solution:** Ensure strict data typing `adata.obs['cluster'] = adata.obs['cluster'].astype('category')` prior to running LIANA. 

## 4. AnnData & NumPy 2.x Collision
- **Package Name:** `anndata`, `numpy`
- **Installed Version:** `anndata>=0.11.0`, `numpy>=2.0`
- **Compatible Version:** For stability across all legacy spatial packages, `numpy < 2.0` is strongly advised.
- **Root Cause:** NumPy 2.0 introduced significant changes to the C-API and array broadcasting, breaking many compiled extensions in bioinformatics tools that were built against NumPy 1.x.
- **Recommended Long-Term Solution:** SpatialAIFlow's `environment.yml` now correctly pins `numpy<2.0` where possible, or utilizes the latest `scverse` stack that has been patched for NumPy 2.x. Users installing via `pip` must be cautious of transitive dependencies upgrading NumPy to 2.x.
