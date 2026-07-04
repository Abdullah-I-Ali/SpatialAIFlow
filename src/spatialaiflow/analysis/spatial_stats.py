"""
Spatial statistics and graph operations.
"""
from typing import Optional, List, Union
import squidpy as sq
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata, require_columns


def build_spatial_graph(
    adata: anndata.AnnData,
    radius: float = 400.0,
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Build a spatial graph representing physical neighborhoods.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix with spatial coordinates.
    radius : float, optional
        Radius to consider for spatial neighborhoods, by default 400.0.
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `sq.gr.spatial_neighbors`.

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
    logger.info(f"Building spatial graph with radius={radius}...")
    
    adata_out = adata.copy() if copy else adata
    sq.gr.spatial_neighbors(adata_out, coord_type="generic", radius=radius, **kwargs)
    
    return adata_out if copy else None


def compute_morans_i(
    adata: anndata.AnnData,
    genes: Union[List[str], str, None] = None,
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Compute Moran's I spatial autocorrelation for genes.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix (must have spatial graph computed).
    genes : Union[List[str], str, None], optional
        Genes to compute Moran's I for. If None, computes for all highly variable genes, by default None.
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `sq.gr.spatial_autocorr`.

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
    logger.info("Computing Moran's I spatial autocorrelation...")
    
    adata_out = adata.copy() if copy else adata
    sq.gr.spatial_autocorr(adata_out, mode="moran", genes=genes, **kwargs)
    
    return adata_out if copy else None


def compute_neighborhood_enrichment(
    adata: anndata.AnnData,
    cluster_key: str = "clusters",
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Compute neighborhood enrichment to find co-locating cell types.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    cluster_key : str, optional
        The key in `adata.obs` containing cell cluster labels, by default "clusters".
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `sq.gr.nhood_enrichment`.

    Returns
    -------
    anndata.AnnData or None
        A copy of the AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `cluster_key` is not found in `adata.obs`.
    """
    require_columns(adata, cols=[cluster_key], axis="obs")
    logger.info(f"Computing neighborhood enrichment for '{cluster_key}'...")
    
    adata_out = adata.copy() if copy else adata
    sq.gr.nhood_enrichment(adata_out, cluster_key=cluster_key, **kwargs)
    
    return adata_out if copy else None


def compute_co_occurrence(
    adata: anndata.AnnData,
    cluster_key: str = "auto_cell_type",
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Compute spatial co-occurrence across distances.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    cluster_key : str, optional
        The key in `adata.obs` containing cell type labels, by default "auto_cell_type".
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `sq.gr.co_occurrence`.

    Returns
    -------
    anndata.AnnData or None
        A copy of the AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `cluster_key` is not found in `adata.obs`.
    """
    require_columns(adata, cols=[cluster_key], axis="obs")
    logger.info(f"Computing spatial co-occurrence for '{cluster_key}'...")
    
    adata_out = adata.copy() if copy else adata
    sq.gr.co_occurrence(adata_out, cluster_key=cluster_key, **kwargs)
    
    return adata_out if copy else None
