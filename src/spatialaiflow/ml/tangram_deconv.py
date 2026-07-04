"""
Tangram deconvolution mapping.
"""
from typing import Tuple, Any
import scanpy as sc
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata, require_columns
from spatialaiflow.utils.exceptions import ModelExecutionError


def prepare_tangram_data(
    adata_sc: anndata.AnnData,
    adata_sp: anndata.AnnData,
    copy: bool = False
) -> Tuple[anndata.AnnData, anndata.AnnData]:
    """
    Prepare single-cell and spatial data for Tangram mapping.

    This function normalizes the single-cell data, finds common genes,
    and constructs the appropriately matched `.uns` dictionaries required by Tangram.

    Parameters
    ----------
    adata_sc : anndata.AnnData
        The single-cell reference data matrix.
    adata_sp : anndata.AnnData
        The spatial transcriptomics data matrix.
    copy : bool, optional
        If True, return a copy of both AnnData objects. If False, modify in place.
        Default is False.

    Returns
    -------
    Tuple[anndata.AnnData, anndata.AnnData]
        The prepared (sc_adata, sp_adata) tuple.

    Raises
    ------
    DataValidationError
        If inputs are not valid AnnData objects.
    ModelExecutionError
        If Tangram is not installed.
    """
    validate_anndata(adata_sc)
    validate_anndata(adata_sp)
    
    logger.info("Preparing data for Tangram mapping...")
    
    try:
        import tangram as tg
    except ImportError as e:
        logger.error("tangram-sc is required for spatial deconvolution.")
        raise ModelExecutionError("tangram-sc not installed.") from e

    out_sc = adata_sc.copy() if copy else adata_sc
    out_sp = adata_sp.copy() if copy else adata_sp
    
    sc.pp.normalize_total(out_sc)
    sc.pp.log1p(out_sc)
    
    tg.pp_adatas(out_sc, out_sp, genes=None)
    
    return out_sc, out_sp


def run_tangram_mapping(
    adata_sc: anndata.AnnData,
    adata_sp: anndata.AnnData,
    **kwargs
) -> Any:
    """
    Run Tangram to map single-cell profiles to spatial spots.

    Parameters
    ----------
    adata_sc : anndata.AnnData
        The preprocessed single-cell reference data matrix.
    adata_sp : anndata.AnnData
        The preprocessed spatial data matrix.
    **kwargs : dict
        Additional arguments passed to `tangram.map_cells_to_space`.

    Returns
    -------
    anndata.AnnData
        The Tangram mapping output AnnData object.

    Raises
    ------
    ModelExecutionError
        If Tangram mapping fails or is not installed.
    """
    logger.info("Running Tangram mapping to project cells to space...")
    
    try:
        import tangram as tg
    except ImportError as e:
        logger.error("tangram-sc is required for spatial deconvolution.")
        raise ModelExecutionError("tangram-sc not installed.") from e
        
    try:
        # Default kwargs
        params = {"mode": "cells", "density_prior": "uniform", "num_epochs": 100, "device": "cpu"}
        params.update(kwargs)
        
        ad_map = tg.map_cells_to_space(
            adata_sc,
            adata_sp,
            **params
        )
        logger.info("Tangram mapping completed successfully.")
        return ad_map
    except Exception as e:
        logger.error(f"Tangram mapping failed: {e}")
        raise ModelExecutionError(f"Tangram failed: {e}") from e


def extract_tangram_results(
    adata_sc: anndata.AnnData,
    ad_map: anndata.AnnData,
    adata_sp: anndata.AnnData,
    annotation_col: str = "cell_type",
    copy: bool = False
) -> Optional[anndata.AnnData]:
    """
    Extract the mapped cell type probabilities into the spatial AnnData object.

    Parameters
    ----------
    adata_sc : anndata.AnnData
        The single-cell reference data matrix.
    ad_map : anndata.AnnData
        The Tangram mapping output AnnData.
    adata_sp : anndata.AnnData
        The spatial transcriptomics data matrix.
    annotation_col : str, optional
        The column in `adata_sc.obs` containing cell annotations, by default "cell_type".
    copy : bool, optional
        If True, return a copy of the spatial AnnData object. If False, modify in place.
        Default is False.

    Returns
    -------
    anndata.AnnData or None
        A copy of the spatial AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `annotation_col` is missing from the single-cell reference.
    ModelExecutionError
        If extraction fails.
    """
    require_columns(adata_sc, cols=[annotation_col], axis="obs")
    logger.info(f"Projecting annotations from '{annotation_col}' to spatial coordinates...")
    
    try:
        import tangram as tg
    except ImportError as e:
        logger.error("tangram-sc is required for spatial deconvolution.")
        raise ModelExecutionError("tangram-sc not installed.") from e
        
    out_sp = adata_sp.copy() if copy else adata_sp
    
    tg.project_cell_annotations(ad_map, out_sp, annotation=annotation_col)
    
    return out_sp if copy else None
