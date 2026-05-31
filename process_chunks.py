import os
import json
import re

base_dir = "/home/chihwei/playground/ohmyxxx-study"
out_dir = "/home/chihwei/playground/ohmyxxx-study/graphify-out"

def process_chunk(chunk_id):
    chunk_txt = os.path.join(out_dir, f".graphify_targeted_chunk_{chunk_id}.txt")
    if not os.path.exists(chunk_txt):
        print(f"Chunk file {chunk_txt} not found.")
        return
        
    with open(chunk_txt, 'r', encoding='utf-8') as f:
        files = [line.strip() for line in f if line.strip()]
        
    nodes = []
    edges = []
    
    # 1. Create Nodes
    for f in files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        stem = os.path.splitext(os.path.basename(f))[0]
        # Avoid naming conflicts by using parent directory for SKILL or README
        if stem.upper() in ['SKILL', 'README']:
            # Get the directory hierarchy name to make it unique
            parts = f.split('/')
            if len(parts) >= 2:
                # E.g., oh-my-codex/skills/ralplan/SKILL.md -> ralplan_skill
                # E.g., oh-my-antigravity/skills/blueprint/SKILL.md -> blueprint_skill
                parent_dir = parts[-2]
                repo = parts[0]
                node_id = f"{repo.replace('-', '_')}_{parent_dir}_{stem.lower()}"
                default_label = f"[{repo}] {parent_dir.replace('-', ' ').title()} {stem.upper()}"
            else:
                parent_dir = os.path.basename(os.path.dirname(f))
                node_id = f"{parent_dir}_{stem.lower()}"
                default_label = f"{parent_dir.replace('-', ' ').title()} {stem.upper()}"
        else:
            repo = f.split('/')[0]
            node_id = f"{repo.replace('-', '_')}_{stem}_{stem}"
            default_label = f"[{repo}] {stem.replace('-', ' ').title()}"
            
        # Extract Human Readable Name (header)
        header_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        label = header_match.group(1).strip() if header_match else default_label
        label = re.sub(r'[*`_]', '', label)
        
        nodes.append({
            "id": node_id,
            "label": label,
            "file_type": "document",
            "source_file": f,
            "source_location": None,
            "source_url": None,
            "captured_at": None,
            "author": None,
            "contributor": None
        })
        
    # 2. Extract Edges (within files of this chunk or overall files)
    # We can also match other files in the same chunk or overall
    # Let's read all targeted files to have a global list of potential targets
    global_targeted_files_path = os.path.join(out_dir, ".graphify_targeted_files.txt")
    global_files = []
    if os.path.exists(global_targeted_files_path):
        with open(global_targeted_files_path, 'r', encoding='utf-8') as gf:
            global_files = [line.strip() for line in gf if line.strip()]
            
    # Build a lookup of global node IDs and names to relate to
    global_targets = []
    for gf in global_files:
        gf_stem = os.path.splitext(os.path.basename(gf))[0]
        gf_parts = gf.split('/')
        gf_repo = gf_parts[0]
        if gf_stem.upper() in ['SKILL', 'README']:
            if len(gf_parts) >= 2:
                gf_parent = gf_parts[-2]
                gf_node_id = f"{gf_repo.replace('-', '_')}_{gf_parent}_{gf_stem.lower()}"
                gf_match_name = gf_parent
            else:
                gf_parent = os.path.basename(os.path.dirname(gf))
                gf_node_id = f"{gf_parent}_{gf_stem.lower()}"
                gf_match_name = gf_parent
        else:
            gf_node_id = f"{gf_repo.replace('-', '_')}_{gf_stem}_{gf_stem}"
            gf_match_name = gf_stem
            
        global_targets.append({
            "file": gf,
            "node_id": gf_node_id,
            "match_name": gf_match_name,
            "stem": gf_stem
        })

    for f in files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        stem = os.path.splitext(os.path.basename(f))[0]
        parts = f.split('/')
        repo = parts[0]
        if stem.upper() in ['SKILL', 'README']:
            if len(parts) >= 2:
                parent_dir = parts[-2]
                source_id = f"{repo.replace('-', '_')}_{parent_dir}_{stem.lower()}"
            else:
                parent_dir = os.path.basename(os.path.dirname(f))
                source_id = f"{parent_dir}_{stem.lower()}"
        else:
            source_id = f"{repo.replace('-', '_')}_{stem}_{stem}"
            
        for gt in global_targets:
            if gt["file"] == f:
                continue
                
            mentioned = False
            # Check if mentioned
            if gt["stem"].upper() in ['SKILL', 'README']:
                pattern1 = rf"\b{re.escape(gt['match_name'])}\b"
                mentioned = re.search(pattern1, content, re.IGNORECASE)
            else:
                pattern = rf"\b{re.escape(gt['match_name'])}\b"
                mentioned = re.search(pattern, content, re.IGNORECASE) or re.search(rf"\b{re.escape(gt['match_name'])}\.md\b", content, re.IGNORECASE)
                
            if mentioned:
                context = ""
                match = re.search(rf"(.{{0,50}}\b{re.escape(gt['match_name'])}\b.{{0,50}})", content, re.IGNORECASE)
                if match:
                    context = match.group(1).lower()
                    
                relation = "references"
                confidence = "EXTRACTED"
                confidence_score = 0.9
                
                if "call" in context or "invoke" in context or "delegate" in context:
                    relation = "calls"
                    confidence_score = 0.95
                elif "implement" in context or "realize" in context:
                    relation = "implements"
                    confidence_score = 0.95
                elif "similar" in context or "like" in context:
                    relation = "semantically_similar_to"
                    confidence_score = 0.8
                elif "relate" in context or "connect" in context:
                    relation = "conceptually_related_to"
                    confidence_score = 0.8
                    
                if f"[{gt['match_name']}]" in content or f"({gt['match_name']}" in content:
                    confidence = "EXTRACTED"
                    confidence_score = 1.0
                    
                edges.append({
                    "source": source_id,
                    "target": gt["node_id"],
                    "relation": relation,
                    "confidence": confidence,
                    "confidence_score": confidence_score,
                    "source_file": f,
                    "source_location": None,
                    "weight": 1.0
                })
                
    graph_data = {
        "nodes": nodes,
        "edges": edges,
        "hyperedges": [],
        "input_tokens": 0,
        "output_tokens": 0
    }
    
    out_path = os.path.join(out_dir, f".graphify_chunk_{chunk_id}.json")
    with open(out_path, 'w', encoding='utf-8') as out_f:
        json.dump(graph_data, out_f, indent=2)
        
    print(f"Chunk {chunk_id}: Extracted {len(nodes)} nodes and {len(edges)} edges. Saved to {out_path}")

# Run for chunks 7, 8, 9
for c_id in [7, 8, 9]:
    process_chunk(c_id)
