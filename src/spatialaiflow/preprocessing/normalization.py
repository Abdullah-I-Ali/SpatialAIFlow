"""
Data normalization utilities.
"""
from typing import Optional
import scanpy as sc
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata


def normalize_and_log(
    adata: anndata.AnnData,
    target_sum: float = 1e4,
    copy: bool = False
) -> Optional[anndata.AnnData]:
    """
    Normalize total counts per spot and log-transform the data.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    target_sum : float, optional
        Target sum for normalization, by default 1e4.
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
    logger.info(f"Normalizing total counts to {target_sum} and log-transforming...")
    
    adata_out = adata.copy() if copy else adata
    
    sc.pp.normalize_total(adata_out, target_sum=target_sum, inplace=True)
    sc.pp.log1p(adata_out)
    
    return adata_out if copy else None


def select_highly_variable_genes(
    adata: anndata.AnnData,
    n_top_genes: int = 2000,
    flavor: str = "seurat",
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Select highly variable genes for downstream analysis.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix (log-normalized).
    n_top_genes : int, optional
        Number of top variable genes to select, by default 2000.
    flavor : str, optional
        Flavor of variable gene selection, by default "seurat".
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `sc.pp.highly_variable_genes`.

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
    logger.info(f"Selecting {n_top_genes} highly variable genes (flavor='{flavor}')...")
    
    adata_out = adata.copy() if copy else adata
    
    sc.pp.highly_variable_genes(
        adata_out,
        flavor=flavor,
        n_top_genes=n_top_genes,
        **kwargs
    )
    
    return adata_out if copy else None
