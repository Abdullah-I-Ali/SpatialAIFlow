"""
Ligand-receptor cell communication inference.
"""
from typing import Optional
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import require_columns
from spatialaiflow.utils.exceptions import ModelExecutionError


def run_liana_communication(
    adata: anndata.AnnData,
    groupby: str = "cell_type",
    resource: str = "Consensus",
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Run LIANA to infer ligand-receptor interactions between cell types.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    groupby : str, optional
        The key in `adata.obs` defining the cell types or clusters, by default "cell_type".
    resource : str, optional
        The database resource to use for interactions, by default "Consensus".
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `liana.mt.liana_pipe`.

    Returns
    -------
    anndata.AnnData or None
        A copy of the AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `groupby` is missing from `adata.obs`.
    ModelExecutionError
        If LIANA fails to execute or is not installed.
    """
    require_columns(adata, cols=[groupby], axis="obs")
    logger.info(f"Running LIANA communication inference (groupby='{groupby}', resource='{resource}')...")
    
    try:
        import liana as li
    except ImportError as e:
        logger.error("liana is required for communication inference.")
        raise ModelExecutionError("liana not installed.") from e

    adata_out = adata.copy() if copy else adata
    
    try:
        # Default kwargs
        params = {"expr_prop": 0.1, "n_perms": 100}
        params.update(kwargs)
        
        li.mt.liana_pipe(
            adata_out,
            groupby=groupby,
            resource=resource,
            **params
        )
    except Exception as e:
        logger.error(f"LIANA execution failed: {e}")
        raise ModelExecutionError(f"LIANA failed: {e}") from e
    
    return adata_out if copy else None
