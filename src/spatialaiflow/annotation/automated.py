"""
Automated cell-type annotation using CellTypist.
"""
from typing import Optional, Any
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata
from spatialaiflow.utils.exceptions import ModelExecutionError


def run_celltypist_annotation(
    adata: anndata.AnnData,
    model_name: str = "Immune_All_Low.pkl",
    out_key: str = "auto_cell_type",
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Run automated cell type annotation using CellTypist.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    model_name : str, optional
        The CellTypist model to download and use, by default "Immune_All_Low.pkl".
    out_key : str, optional
        The key in `adata.obs` to save predictions to, by default "auto_cell_type".
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `celltypist.annotate`.

    Returns
    -------
    anndata.AnnData or None
        A copy of the AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `adata` is not a valid AnnData object.
    ModelExecutionError
        If CellTypist fails to download the model or execute predictions.
    """
    validate_anndata(adata)
    logger.info(f"Running automated annotation using CellTypist (model='{model_name}')...")
    
    try:
        # Lazy import to avoid loading heavy models unnecessarily
        import celltypist
    except ImportError as e:
        logger.error("celltypist is required for automated annotation.")
        raise ModelExecutionError("celltypist not installed.") from e

    adata_out = adata.copy() if copy else adata
    
    try:
        celltypist.models.download_models(force_update=False, model=model_name)
        model = celltypist.models.Model.load(model_name)
        
        predictions = celltypist.annotate(adata_out, model=model, majority_voting=True, **kwargs)
        adata_out.obs[out_key] = predictions.predicted_labels["majority_voting"]
    except Exception as e:
        logger.error(f"CellTypist annotation failed: {e}")
        raise ModelExecutionError(f"CellTypist annotation failed: {e}") from e
    
    return adata_out if copy else None
