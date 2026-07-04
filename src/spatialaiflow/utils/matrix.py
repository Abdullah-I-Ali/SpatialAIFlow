"""
Matrix operations and sparse data handling.
"""
from typing import Union
import numpy as np
import scipy.sparse as sp

def to_dense_array(matrix: Union[np.ndarray, sp.spmatrix]) -> np.ndarray:
    """
    Safely convert a matrix to a dense numpy array.

    Parameters
    ----------
    matrix : Union[np.ndarray, sp.spmatrix]
        The input matrix, which can be dense or sparse.

    Returns
    -------
    np.ndarray
        A dense numpy array representation of the matrix.
    """
    if sp.issparse(matrix):
        return matrix.toarray()
    if hasattr(matrix, "toarray"):
        return matrix.toarray()
    return np.asarray(matrix)
