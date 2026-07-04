"""
Manual cell-type annotation utilities.
"""
from typing import Dict, Optional
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import require_columns


def apply_manual_annotation(
    adata: anndata.AnnData,
    mapping_dict: Dict[str, str],
    source_key: str = "clusters",
    target_key: str = "cell_type",
    copy: bool = False
) -> Optional[anndata.AnnData]:
    """
    Map cluster labels to cell type annotations using a dictionary.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    mapping_dict : Dict[str, str]
        Dictionary mapping existing cluster labels to biological cell types.
    source_key : str, optional
        The key in `adata.obs` to map from, by default "clusters".
    target_key : str, optional
        The key in `adata.obs` to save the mapped annotations to, by default "cell_type".
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
        If `source_key` is not found in `adata.obs`.
    """
    require_columns(adata, cols=[source_key], axis="obs")
    logger.info(f"Applying manual annotations from '{source_key}' to '{target_key}'...")
    
    adata_out = adata.copy() if copy else adata
    
    adata_out.obs[target_key] = adata_out.obs[source_key].map(mapping_dict).astype("category")
    
    return adata_out if copy else None
