"""
Validation utilities for defensive programming.
"""
from typing import List, Optional
import anndata

from spatialaiflow.utils.exceptions import DataValidationError


def validate_anndata(adata: anndata.AnnData) -> None:
    """
    Validate that the input is a valid AnnData object.

    Parameters
    ----------
    adata : anndata.AnnData
        The object to validate.

    Raises
    ------
    DataValidationError
        If the input is not an AnnData object.
    """
    if not isinstance(adata, anndata.AnnData):
        raise DataValidationError(f"Expected AnnData object, got {type(adata)}")


def require_columns(adata: anndata.AnnData, cols: List[str], axis: str = "obs") -> None:
    """
    Ensure specific columns exist in adata.obs or adata.var.

    Parameters
    ----------
    adata : anndata.AnnData
        The AnnData object to validate.
    cols : List[str]
        List of column names that must exist.
    axis : str, optional
        The axis to check ('obs' or 'var'), by default "obs".

    Raises
    ------
    DataValidationError
        If any required column is missing.
    """
    validate_anndata(adata)
    
    if axis == "obs":
        df = adata.obs
    elif axis == "var":
        df = adata.var
    else:
        raise ValueError("axis must be 'obs' or 'var'")

    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise DataValidationError(f"Missing required columns in adata.{axis}: {missing}")
