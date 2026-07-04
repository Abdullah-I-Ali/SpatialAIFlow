"""Shared pytest fixtures for the SpatialAIFlow test suite."""

import pytest


@pytest.fixture
def sample_adata():
    """Create a minimal AnnData object for testing.

    Returns a small, synthetic AnnData with:
    - 50 observations (spots)
    - 100 variables (genes)
    - Random count data
    - Spatial coordinates in obsm["spatial"]

    This fixture avoids downloading real data during tests.
    """
    # TODO: Implement once source modules are populated.
    pass
