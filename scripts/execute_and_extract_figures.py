import os
import sys
import base64
import nbformat
from nbclient import NotebookClient

NOTEBOOK_PATH = "notebooks/SpatialAIFlow.ipynb"
OUTPUT_PNG_DIR = "assets/figures/png"
OUTPUT_SVG_DIR = "assets/figures/svg"

os.makedirs(OUTPUT_PNG_DIR, exist_ok=True)
os.makedirs(OUTPUT_SVG_DIR, exist_ok=True)

print(f"Loading notebook: {NOTEBOOK_PATH}")
with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Inject cell to ensure matplotlib outputs both PNG and SVG and high quality
config_code = (
    "import matplotlib_inline\n"
    "import matplotlib.pyplot as plt\n"
    "matplotlib_inline.backend_inline.set_matplotlib_formats('png', 'svg')\n"
    "plt.rcParams.update({\n"
    "    'figure.dpi': 300,\n"
    "    'font.size': 14,\n"
    "    'axes.titlesize': 16,\n"
    "    'axes.labelsize': 14,\n"
    "    'legend.fontsize': 12,\n"
    "    'figure.autolayout': True\n"
    "})"
)
config_cell = nbformat.v4.new_code_cell(source=config_code)
nb.cells.insert(0, config_cell)

print("Executing notebook (this may take a while)...")
client = NotebookClient(nb, timeout=3600, kernel_name='spatial_env', allow_errors=True)
try:
    client.execute()
    print("Execution complete. Extracting figures...")
except Exception as e:
    print(f"Execution failed: {e}")

# Save the executed notebook to disk so we have the cache
with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

# Collect compatibility errors
compatibility_issues = []

# Mapping of code signatures to output filenames
signature_map = {
    "sc.pl.violin": "qc_violin",
    "color=\"total_counts\"": "raw_data_visualization",
    "color=[\"clusters\"]": "umap_clusters",
    "sc.pl.rank_genes_groups_dotplot": "marker_genes_heatmap",
    "color=available_markers": "spatial_gene_expression",
    "sq.pl.nhood_enrichment": "neighborhood_enrichment",
    "color=\"cell_type\"": "celltype_annotation",
    "li.pl.dotplot": "cell_communication_network",
    "color=[\"clusters\", \"tissue_homogeneity\"]": "histology_features",
    "gp.plot.barplot": "pathway_dotplot",
    "draw_graph": "trajectory_paga",
    "sns.barplot": "random_forest_feature_importance",
    "color=[\"auto_cell_type\", tumor_col]": "tangram_mapping",
}

found_figures = set()

for cell in nb.cells:
    if cell.cell_type != 'code':
        continue
    
    # Identify which figure this cell produced
    fig_name = None
    for sig, name in signature_map.items():
        if sig in cell.source:
            fig_name = name
            break
            
    if not fig_name:
        continue
        
    for output in cell.get('outputs', []):
        if output.output_type == 'error':
            error_trace = "\\n".join(output.traceback)
            compatibility_issues.append((fig_name or "Unknown Cell", output.ename, output.evalue, error_trace))
            
        if output.output_type in ('display_data', 'execute_result'):
            data = output.get('data', {})
            
            # Extract PNG
            if 'image/png' in data:
                png_path = os.path.join(OUTPUT_PNG_DIR, f"{fig_name}.png")
                with open(png_path, "wb") as f_png:
                    f_png.write(base64.b64decode(data['image/png']))
                print(f"Saved: {png_path}")
                found_figures.add(fig_name)
                
            # Extract SVG
            if 'image/svg+xml' in data:
                svg_path = os.path.join(OUTPUT_SVG_DIR, f"{fig_name}.svg")
                with open(svg_path, "w", encoding='utf-8') as f_svg:
                    f_svg.write(data['image/svg+xml'])
                print(f"Saved: {svg_path}")

print(f"Finished extracting {len(found_figures)} unique figures.")

# Generate COMPATIBILITY_REPORT.md
with open("COMPATIBILITY_REPORT.md", "w", encoding="utf-8") as f:
    f.write("# External Dependency Compatibility Report\\n\\n")
    if not compatibility_issues:
        f.write("No compatibility issues detected during execution.\\n")
    else:
        for section, ename, evalue, _ in compatibility_issues:
            f.write(f"## Issue in {section}\\n")
            f.write(f"- **Error Type**: `{ename}`\\n")
            f.write(f"- **Details**: `{evalue}`\\n")
            f.write("- **Recommendation**: Verify package versions for third-party libraries.\\n\\n")

