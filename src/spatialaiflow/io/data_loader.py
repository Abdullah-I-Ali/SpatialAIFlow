"""
Data loading utilities for SpatialAIFlow.
"""
from typing import Tuple, Optional
import squidpy as sq
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.exceptions import ModelExecutionError


def load_visium_data() -> Tuple[sq.im.ImageContainer, anndata.AnnData]:
    """
    Load the Visium H&E image and corresponding AnnData object.

    This function downloads or loads a built-in Visium spatial transcriptomics
    dataset provided by Squidpy.

    Returns
    -------
    img : squidpy.im.ImageContainer
        The high-resolution H&E image.
    adata : anndata.AnnData
        The spatial transcriptomics data.

    Raises
    ------
    ModelExecutionError
        If the datasets fail to load or download.
    """
    logger.info("Loading Visium H&E image and AnnData object...")
    try:
        img = sq.datasets.visium_hne_image()
        adata = sq.datasets.visium_hne_adata()
        logger.info(f"Loaded AnnData with {adata.n_obs} spots and {adata.n_vars} genes.")
        return img, adata
    except Exception as e:
        logger.error(f"Failed to load Visium data: {e}")
        raise ModelExecutionError(f"Data loading failed: {e}") from e
