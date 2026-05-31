const fs = require('fs');
const path = require('path');

const baseDir = "/home/chihwei/playground/ohmyxxx-study";
const outDir = "/home/chihwei/playground/ohmyxxx-study/graphify-out";

function titleCase(str) {
    return str.replace(/\b\w/g, c => c.toUpperCase());
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function processChunk(chunkId) {
    const chunkTxt = path.join(outDir, `.graphify_targeted_chunk_${chunkId}.txt`);
    if (!fs.existsSync(chunkTxt)) {
        console.error(`Chunk file ${chunkTxt} not found.`);
        return;
    }
        
    const files = fs.readFileSync(chunkTxt, 'utf-8')
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0);
        
    const nodes = [];
    const edges = [];
    
    // 1. Create Nodes
    for (const f of files) {
        const filePath = path.join(baseDir, f);
        if (!fs.existsSync(filePath)) {
            continue;
        }
            
        const content = fs.readFileSync(filePath, 'utf-8');
        const stem = path.parse(f).name;
        
        let node_id = "";
        let default_label = "";
        
        // Avoid naming conflicts by using parent directory for SKILL or README
        if (['SKILL', 'README'].includes(stem.toUpperCase())) {
            const parts = f.split('/');
            if (parts.length >= 2) {
                const parent_dir = parts[parts.length - 2];
                const repo = parts[0];
                node_id = `${repo.replace(/-/g, '_')}_${parent_dir}_${stem.toLowerCase()}`;
                default_label = `[${repo}] ${titleCase(parent_dir.replace(/-/g, ' '))} ${stem.toUpperCase()}`;
            } else {
                const parent_dir = path.basename(path.dirname(f));
                node_id = `${parent_dir}_${stem.toLowerCase()}`;
                default_label = `${titleCase(parent_dir.replace(/-/g, ' '))} ${stem.toUpperCase()}`;
            }
        } else {
            const repo = f.split('/')[0];
            node_id = `${repo.replace(/-/g, '_')}_${stem}_${stem}`;
            default_label = `[${repo}] ${titleCase(stem.replace(/-/g, ' '))}`;
        }
            
        // Extract Human Readable Name (header)
        const header_match = content.match(/^#\s+(.+)$/m);
        let label = header_match ? header_match[1].trim() : default_label;
        label = label.replace(/[*`_]/g, '');
        
        nodes.push({
            "id": node_id,
            "label": label,
            "file_type": "document",
            "source_file": f,
            "source_location": null,
            "source_url": null,
            "captured_at": null,
            "author": null,
            "contributor": null
        });
    }
        
    // 2. Extract Edges
    const globalTargetedFilesPath = path.join(outDir, ".graphify_targeted_files.txt");
    let global_files = [];
    if (fs.existsSync(globalTargetedFilesPath)) {
        global_files = fs.readFileSync(globalTargetedFilesPath, 'utf-8')
            .split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);
    }
            
    // Build a lookup of global node IDs and names to relate to
    const global_targets = [];
    for (const gf of global_files) {
        const gf_stem = path.parse(gf).name;
        const gf_parts = gf.split('/');
        const gf_repo = gf_parts[0];
        
        let gf_node_id = "";
        let gf_match_name = "";
        
        if (['SKILL', 'README'].includes(gf_stem.toUpperCase())) {
            if (gf_parts.length >= 2) {
                const gf_parent = gf_parts[gf_parts.length - 2];
                gf_node_id = `${gf_repo.replace(/-/g, '_')}_${gf_parent}_${gf_stem.toLowerCase()}`;
                gf_match_name = gf_parent;
            } else {
                const gf_parent = path.basename(path.dirname(gf));
                gf_node_id = `${gf_parent}_${gf_stem.toLowerCase()}`;
                gf_match_name = gf_parent;
            }
        } else {
            gf_node_id = `${gf_repo.replace(/-/g, '_')}_${gf_stem}_${gf_stem}`;
            gf_match_name = gf_stem;
        }
            
        global_targets.push({
            "file": gf,
            "node_id": gf_node_id,
            "match_name": gf_match_name,
            "stem": gf_stem
        });
    }

    for (const f of files) {
        const filePath = path.join(baseDir, f);
        if (!fs.existsSync(filePath)) {
            continue;
        }
        const content = fs.readFileSync(filePath, 'utf-8');
        const stem = path.parse(f).name;
        const parts = f.split('/');
        const repo = parts[0];
        
        let source_id = "";
        if (['SKILL', 'README'].includes(stem.toUpperCase())) {
            if (parts.length >= 2) {
                const parent_dir = parts[parts.length - 2];
                source_id = `${repo.replace(/-/g, '_')}_${parent_dir}_${stem.toLowerCase()}`;
            } else {
                const parent_dir = path.basename(path.dirname(f));
                source_id = `${parent_dir}_${stem.toLowerCase()}`;
            }
        } else {
            source_id = `${repo.replace(/-/g, '_')}_${stem}_${stem}`;
        }
            
        for (const gt of global_targets) {
            if (gt.file === f) {
                continue;
            }
                
            let mentioned = false;
            // Check if mentioned
            if (['SKILL', 'README'].includes(gt.stem.toUpperCase())) {
                const pattern1 = new RegExp(`\\b${escapeRegExp(gt.match_name)}\\b`, 'i');
                mentioned = pattern1.test(content);
            } else {
                const pattern = new RegExp(`\\b${escapeRegExp(gt.match_name)}\\b`, 'i');
                const patternMd = new RegExp(`\\b${escapeRegExp(gt.match_name)}\\.md\\b`, 'i');
                mentioned = pattern.test(content) || patternMd.test(content);
            }
                
            if (mentioned) {
                let context = "";
                const match = content.match(new RegExp(`(.{0,50}\\b${escapeRegExp(gt.match_name)}\\b.{0,50})`, 'i'));
                if (match) {
                    context = match[1].toLowerCase();
                }
                    
                let relation = "references";
                let confidence = "EXTRACTED";
                let confidence_score = 0.9;
                
                if (context.includes("call") || context.includes("invoke") || context.includes("delegate")) {
                    relation = "calls";
                    confidence_score = 0.95;
                } else if (context.includes("implement") || context.includes("realize")) {
                    relation = "implements";
                    confidence_score = 0.95;
                } else if (context.includes("similar") || context.includes("like")) {
                    relation = "semantically_similar_to";
                    confidence_score = 0.8;
                } else if (context.includes("relate") || context.includes("connect")) {
                    relation = "conceptually_related_to";
                    confidence_score = 0.8;
                }
                    
                if (content.includes(`[${gt.match_name}]`) || content.includes(`(${gt.match_name}`)) {
                    confidence = "EXTRACTED";
                    confidence_score = 1.0;
                }
                    
                edges.push({
                    "source": source_id,
                    "target": gt.node_id,
                    "relation": relation,
                    "confidence": confidence,
                    "confidence_score": confidence_score,
                    "source_file": f,
                    "source_location": null,
                    "weight": 1.0
                });
            }
        }
    }
                
    const graphData = {
        "nodes": nodes,
        "edges": edges,
        "hyperedges": [],
        "input_tokens": 0,
        "output_tokens": 0
    };
    
    const outPath = path.join(outDir, `.graphify_chunk_${chunkId}.json`);
    fs.writeFileSync(outPath, JSON.stringify(graphData, null, 2), 'utf-8');
    console.log(`Chunk ${chunkId}: Extracted ${nodes.length} nodes and ${edges.length} edges. Saved to ${outPath}`);
}

processChunk(7);
processChunk(8);
processChunk(9);
