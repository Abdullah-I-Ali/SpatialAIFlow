"""
Non-negative matrix factorization (NMF) for spatial modules.
"""
from typing import Optional, Any
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import validate_anndata
from spatialaiflow.utils.matrix import to_dense_array


def run_nmf(
    adata: anndata.AnnData,
    n_components: int = 10,
    random_state: int = 42,
    copy: bool = False,
    **kwargs
) -> Optional[anndata.AnnData]:
    """
    Factorize the expression matrix into spatial modules using NMF.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    n_components : int, optional
        Number of NMF components to extract, by default 10.
    random_state : int, optional
        Random seed for reproducibility, by default 42.
    copy : bool, optional
        If True, return a copy of the AnnData object. If False, modify in place.
        Default is False.
    **kwargs : dict
        Additional arguments passed to `sklearn.decomposition.NMF`.

    Returns
    -------
    anndata.AnnData or None
        A copy of the AnnData object if `copy=True`, otherwise None.

    Raises
    ------
    DataValidationError
        If `adata` is not a valid AnnData object.
    ModelExecutionError
        If the sklearn NMF model fails to fit.
    """
    validate_anndata(adata)
    logger.info(f"Running NMF factorization (n_components={n_components})...")
    
    try:
        from sklearn.decomposition import NMF
    except ImportError as e:
        logger.error("scikit-learn is required for NMF.")
        raise e
        
    adata_out = adata.copy() if copy else adata
    
    # Safely convert matrix to dense if it's sparse, as required by standard NMF
    # (Though NMF does support some sparse formats, ensuring dense array prevents typical errors)
    X = to_dense_array(adata_out.X)
    
    nmf_model = NMF(n_components=n_components, init="random", random_state=random_state, **kwargs)
    W = nmf_model.fit_transform(X)
    
    for i in range(n_components):
        adata_out.obs[f"NMF_{i}"] = W[:, i]
        
    logger.info(f"Stored {n_components} NMF components in adata.obs.")
    
    return adata_out if copy else None
