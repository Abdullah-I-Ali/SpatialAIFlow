"""
Machine learning classifiers for spatial data.
"""
from typing import Tuple, Any
import pandas as pd
import anndata

from spatialaiflow.utils.logger import logger
from spatialaiflow.utils.validation import require_columns
from spatialaiflow.utils.exceptions import ModelExecutionError
from spatialaiflow.utils.matrix import to_dense_array


def prepare_ml_data(
    adata: anndata.AnnData,
    target_col: str = "tumor_niche"
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepare feature matrix X and target vector y for Machine Learning.

    Parameters
    ----------
    adata : anndata.AnnData
        The annotated data matrix.
    target_col : str, optional
        The column in `adata.obs` used as the target variable, by default "tumor_niche".

    Returns
    -------
    Tuple[pd.DataFrame, pd.Series]
        - X: Feature matrix (genes as columns, cells as rows).
        - y: Target vector.

    Raises
    ------
    DataValidationError
        If `target_col` is missing from `adata.obs`.
    """
    require_columns(adata, cols=[target_col], axis="obs")
    logger.info(f"Preparing ML data matrix (target='{target_col}')...")
    
    # Securely convert to dense array if sparse
    X_array = to_dense_array(adata.X)
    X = pd.DataFrame(X_array, index=adata.obs_names, columns=adata.var_names)
    y = adata.obs[target_col].astype(str)
    
    return X, y


def train_random_forest(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.3,
    random_state: int = 42,
    **kwargs
) -> Tuple[Any, pd.DataFrame, pd.Series, pd.Series]:
    """
    Train a Random Forest classifier.

    Parameters
    ----------
    X : pd.DataFrame
        The feature matrix.
    y : pd.Series
        The target vector.
    test_size : float, optional
        Proportion of the dataset to include in the test split, by default 0.3.
    random_state : int, optional
        Random seed for reproducibility, by default 42.
    **kwargs : dict
        Additional arguments passed to `RandomForestClassifier`.

    Returns
    -------
    Tuple[Any, pd.DataFrame, pd.Series, pd.Series]
        - rf_model: The trained scikit-learn RandomForestClassifier instance.
        - X_test: The test feature matrix.
        - y_test: The true test labels.
        - y_pred: The predicted test labels.

    Raises
    ------
    ModelExecutionError
        If scikit-learn is missing or training fails.
    """
    logger.info(f"Training RandomForestClassifier (test_size={test_size})...")
    
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
    except ImportError as e:
        logger.error("scikit-learn is required for ML classifiers.")
        raise ModelExecutionError("scikit-learn not installed.") from e

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        # Default kwargs
        params = {"n_estimators": 100, "n_jobs": -1}
        params.update(kwargs)
        
        rf_model = RandomForestClassifier(random_state=random_state, **params)
        rf_model.fit(X_train, y_train)
        
        y_pred = pd.Series(rf_model.predict(X_test), index=X_test.index)
        
        logger.info("Random forest training complete.")
        return rf_model, X_test, y_test, y_pred
    except Exception as e:
        logger.error(f"Random forest training failed: {e}")
        raise ModelExecutionError(f"Training failed: {e}") from e
