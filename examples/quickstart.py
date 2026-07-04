"""
SpatialAIFlow — Quick Start Example.

Demonstrates the minimal steps to run the spatial transcriptomics pipeline.

Usage
-----
    python examples/quickstart.py

Notes
-----
This is a placeholder script. Once the notebook has been refactored into the
``spatialaiflow`` package, this example will show how to import and run the
pipeline programmatically::

    import spatialaiflow as saf

    adata = saf.io.load_visium("V1_Breast_Cancer_Block_A_Section_1")
    adata = saf.preprocessing.run_qc(adata)
    adata = saf.analysis.cluster(adata)
    saf.plotting.spatial_clusters(adata)
"""


def main():
    """Run the quickstart example."""
    print("SpatialAIFlow quickstart — placeholder.")
    print("See notebooks/SpatialAIFlow.ipynb for the full pipeline.")


if __name__ == "__main__":
    main()
