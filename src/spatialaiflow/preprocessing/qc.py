"""
Quality control module for spatial transcriptomics data.
"""
from typing import Optional
import scanpy as sc
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata, require_columns
from spatialaiflow.utils.exceptions import DataValidationError


def calculate_qc_metrics(adata: anndata.AnnData, copy: bool = False) -> Optional[anndata.AnnData]:
    """
    Calculate quality control metrics (e.g., n_genes_by_counts, pct_counts_mt).

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.

    Returns
    -------
    anndata.AnnData or None
        A copy of the AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `adata` is not a valid AnnData object.
    """
    validate_anndata(adata)
    logger.info("Calculating QC metrics...")
    
    adata_out = adata.copy() if copy else adata
    
    # Tag mitochondrial genes
    adata_out.var["mt"] = adata_out.var_names.str.startswith("MT-")
    sc.pp.calculate_qc_metrics(adata_out, qc_vars=["mt"], inplace=True)
    
    logger.debug(f"QC metrics calculated for {adata_out.n_obs} cells.")
    return adata_out if copy else None


def filter_data(
    adata: anndata.AnnData,
    min_counts: int = 500,
    min_genes: int = 250,
    max_pct_mt: float = 20.0,
    copy: bool = False
) -> Optional[anndata.AnnData]:
    """
    Filter spots and genes based on QC metrics.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    min_counts : int, optional
        Minimum number of counts required for a cell to pass filtering, by default 500.
    min_genes : int, optional
        Minimum number of genes expressed required for a cell to pass filtering, by default 250.
    max_pct_mt : float, optional
        Maximum allowed percentage of mitochondrial counts, by default 20.0.
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.

    Returns
    -------
    anndata.AnnData or None
        A copy of the AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `pct_counts_mt` is not found in `adata.obs`.
    """
    require_columns(adata, cols=["pct_counts_mt"], axis="obs")
    logger.info(f"Filtering data (min_counts={min_counts}, min_genes={min_genes}, max_pct_mt={max_pct_mt})...")
    
    adata_out = adata.copy() if copy else adata
    
    sc.pp.filter_cells(adata_out, min_counts=min_counts)
    sc.pp.filter_cells(adata_out, min_genes=min_genes)
    sc.pp.filter_genes(adata_out, min_cells=10)
    
    # In-place subsetting is not directly supported by scanpy for view restrictions,
    # so we must create a copy and update the original object's internals if copy=False
    mask = adata_out.obs["pct_counts_mt"] < max_pct_mt
    filtered = adata_out[mask].copy()
    
    if not copy:
        # Update the original object in place safely
        adata_out._init_as_actual(filtered)
        logger.info(f"Retained {adata_out.n_obs} cells after filtering.")
        return None
    
    logger.info(f"Retained {filtered.n_obs} cells after filtering.")
    return filtered
