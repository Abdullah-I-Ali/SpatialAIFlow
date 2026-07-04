"""
Dimensionality reduction tools.
"""
from typing import Optional
import scanpy as sc
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata


def run_pca(
    adata: anndata.AnnData,
    n_comps: int = 50,
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Run Principal Component Analysis (PCA).

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    n_comps : int, optional
        Number of principal components to compute, by default 50.
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional keyword arguments passed to `sc.pp.pca`.

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
    logger.info(f"Running PCA with {n_comps} components...")
    
    adata_out = adata.copy() if copy else adata
    sc.pp.pca(adata_out, n_comps=n_comps, **kwargs)
    
    return adata_out if copy else None


def compute_neighbors_and_umap(
    adata: anndata.AnnData,
    n_neighbors: int = 15,
    n_pcs: int = 30,
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Compute the neighborhood graph and run UMAP embedding.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix (must have PCA computed).
    n_neighbors : int, optional
        Size of local neighborhood (in terms of number of neighboring data points), by default 15.
    n_pcs : int, optional
        Number of principal components to use for graph construction, by default 30.
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional keyword arguments passed to `sc.tl.umap`.

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
    logger.info(f"Computing neighborhood graph (n_neighbors={n_neighbors}, n_pcs={n_pcs})...")
    
    adata_out = adata.copy() if copy else adata
    
    sc.pp.neighbors(adata_out, n_neighbors=n_neighbors, n_pcs=n_pcs)
    logger.info("Running UMAP embedding...")
    sc.tl.umap(adata_out, **kwargs)
    
    return adata_out if copy else None
