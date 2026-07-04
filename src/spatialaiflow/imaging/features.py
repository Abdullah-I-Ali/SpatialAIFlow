"""
Image feature extraction utilities.
"""
from typing import Optional, List
import squidpy as sq
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata
from spatialaiflow.utils.exceptions import ModelExecutionError


def extract_image_features(
    img: sq.im.ImageContainer,
    adata: anndata.AnnData,
    features: Optional[List[str]] = None,
    key_added: str = "image_features",
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Extract summary, texture, and histogram features from the H&E image.

    Parameters
    ----------
    img : squidpy.im.ImageContainer
        The high-resolution H&E image.
    adata : anndata.AnnData
        The spatial transcriptomics data.
    features : List[str], optional
        List of feature sets to extract. If None, uses ["summary", "texture", "histogram"],
        by default None.
    key_added : str, optional
        Key in `adata.obsm` to store the features, by default "image_features".
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `sq.im.calculate_image_features`.

    Returns
    -------
    anndata.AnnData or None
        A copy of the AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `adata` is not a valid AnnData object.
    ModelExecutionError
        If feature extraction fails.
    """
    validate_anndata(adata)
    
    if features is None:
        features = ["summary", "texture", "histogram"]
        
    logger.info(f"Extracting image features: {features}...")
    
    adata_out = adata.copy() if copy else adata
    
    try:
        # Default kwargs
        params = {"n_jobs": 1, "scale": 1.0}
        params.update(kwargs)
        
        sq.im.calculate_image_features(
            adata_out,
            img,
            features=features,
            key_added=key_added,
            **params
        )
    except Exception as e:
        logger.error(f"Image feature extraction failed: {e}")
        raise ModelExecutionError(f"Feature extraction failed: {e}") from e
    
    return adata_out if copy else None
