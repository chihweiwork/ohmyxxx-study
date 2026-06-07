import os
import json
from pathlib import Path

# Paths
base_dir = "/home/chihwei/playground/ohmyxxx-study"
out_dir = Path("/home/chihwei/playground/ohmyxxx-study/graphify-out")

def merge_chunks():
    all_nodes = []
    all_edges = []
    all_hyperedges = []
    
    seen_nodes = set()
    seen_edges = set()
    
    chunk_files = sorted(
        out_dir.glob(".graphify_chunk_*.json"),
        key=lambda path: int(path.stem.rsplit("_", 1)[-1]),
    )
    if not chunk_files:
        print("Warning: no chunk JSON files found on disk.")

    for chunk_file in chunk_files:
            
        try:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {chunk_file.name}: {e}")
            continue
            
        # Merge nodes
        for node in data.get('nodes', []):
            nid = node.get('id')
            if nid and nid not in seen_nodes:
                seen_nodes.add(nid)
                all_nodes.append(node)
                
        # Merge edges
        for edge in data.get('edges', []):
            source = edge.get('source')
            target = edge.get('target')
            relation = edge.get('relation')
            edge_key = (source, target, relation)
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                all_edges.append(edge)
                
        # Merge hyperedges
        for he in data.get('hyperedges', []):
            all_hyperedges.append(he)
            
    merged = {
        "nodes": all_nodes,
        "edges": all_edges,
        "hyperedges": all_hyperedges,
        "input_tokens": 0,
        "output_tokens": 0
    }
    
    extract_path = out_dir / ".graphify_extract.json"
    with open(extract_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2)
        
    print(f"Merged successfully: {len(all_nodes)} nodes, {len(all_edges)} edges saved to {extract_path}")

if __name__ == '__main__':
    merge_chunks()
