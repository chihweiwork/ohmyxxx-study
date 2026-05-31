import sys
import json
from pathlib import Path
from graphify.build import build_from_json
from graphify.export import to_html

# Paths
out_dir = Path("/home/chihwei/playground/ohmyxxx-study/graphify-out")

def main():
    extraction_path = out_dir / ".graphify_extract.json"
    analysis_path = out_dir / ".graphify_analysis.json"
    labels_raw_path = out_dir / ".graphify_labels.json"
    
    if not all([p.exists() for p in [extraction_path, analysis_path]]):
        print("Error: Required graphify-out files are missing.")
        sys.exit(1)
        
    extraction = json.loads(extraction_path.read_text(encoding='utf-8'))
    analysis = json.loads(analysis_path.read_text(encoding='utf-8'))
    labels_raw = json.loads(labels_raw_path.read_text(encoding='utf-8')) if labels_raw_path.exists() else {}
    
    G = build_from_json(extraction)
    communities = {int(k): v for k, v in analysis['communities'].items()}
    labels = {int(k): v for k, v in labels_raw.items()}
    
    # Save graph.html
    html_path = out_dir / "graph.html"
    index_path = out_dir / "index.html"
    
    # Generate
    to_html(G, communities, str(index_path), community_labels=labels or None)
    to_html(G, communities, str(html_path), community_labels=labels or None)
    
    print(f"HTML Visualization generated successfully:")
    print(f"  - {index_path}")
    print(f"  - {html_path}")

if __name__ == '__main__':
    main()
