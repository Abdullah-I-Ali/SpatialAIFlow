"""
Marker gene identification utilities.
"""
from typing import Optional
import scanpy as sc
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata, require_columns


def find_marker_genes(
    adata: anndata.AnnData,
    groupby: str = "clusters",
    method: str = "t-test",
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Identify marker genes for each cluster.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    groupby : str, optional
        The key of the observation grouping to consider, by default "clusters".
    method : str, optional
        The statistical method for differential expression, by default "t-test".
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `sc.tl.rank_genes_groups`.

    Returns
    -------
    anndata.AnnData or None
        A copy of the AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `groupby` is not present in `adata.obs`.
    """
    require_columns(adata, cols=[groupby], axis="obs")
    logger.info(f"Finding marker genes (groupby='{groupby}', method='{method}')...")
    
    adata_out = adata.copy() if copy else adata
    
    sc.tl.rank_genes_groups(adata_out, groupby=groupby, method=method, **kwargs)
    
    return adata_out if copy else None
