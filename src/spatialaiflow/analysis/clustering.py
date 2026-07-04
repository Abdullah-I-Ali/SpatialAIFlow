"""
Clustering algorithms for spatial data.
"""
from typing import Optional
import scanpy as sc
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata


def run_leiden_clustering(
    adata: anndata.AnnData,
    resolution: float = 0.5,
    key_added: str = "clusters",
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Run Leiden clustering on the neighborhood graph.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix (must have neighborhood graph computed).
    resolution : float, optional
        Resolution parameter that controls the coarseness of the clustering, by default 0.5.
    key_added : str, optional
        The key under which to add the cluster labels in `adata.obs`, by default "clusters".
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional keyword arguments passed to `sc.tl.leiden`.

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
    logger.info(f"Running Leiden clustering (resolution={resolution}, key_added='{key_added}')...")
    
    adata_out = adata.copy() if copy else adata
    
    sc.tl.leiden(adata_out, resolution=resolution, key_added=key_added, **kwargs)
    
    return adata_out if copy else None
