import json
from pathlib import Path

out_dir = Path("/home/chihwei/playground/ohmyxxx-study/graphify-out")

def print_comms():
    analysis_path = out_dir / ".graphify_analysis.json"
    analysis = json.loads(analysis_path.read_text(encoding='utf-8'))
    
    extraction_path = out_dir / ".graphify_extract.json"
    extraction = json.loads(extraction_path.read_text(encoding='utf-8'))
    
    # Map node id to label
    node_labels = {n['id']: n['label'] for n in extraction['nodes']}
    
    communities = analysis['communities']
    print(f"Total Communities: {len(communities)}")
    for cid, nodes in communities.items():
        print(f"\nCommunity {cid} (size {len(nodes)}):")
        for nid in nodes[:8]: # Show first 8 nodes
            print(f"  - {node_labels.get(nid, nid)} ({nid})")
        if len(nodes) > 8:
            print(f"  - ... and {len(nodes) - 8} more")

if __name__ == '__main__':
    print_comms()
