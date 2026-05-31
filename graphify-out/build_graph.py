import sys
import json
from pathlib import Path
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json

# Paths
input_path = "/home/chihwei/playground/ohmyxxx-study"
out_dir = Path("/home/chihwei/playground/ohmyxxx-study/graphify-out")

def main():
    extraction_path = out_dir / ".graphify_extract.json"
    detect_path = out_dir / ".graphify_detect.json"
    
    if not extraction_path.exists():
        print(f"Error: {extraction_path} not found.")
        sys.exit(1)
        
    if not detect_path.exists():
        print(f"Error: {detect_path} not found.")
        sys.exit(1)
        
    extraction = json.loads(extraction_path.read_text(encoding='utf-8'))
    detection = json.loads(detect_path.read_text(encoding='utf-8'))
    
    print(f"Loaded extraction: {len(extraction['nodes'])} nodes, {len(extraction['edges'])} edges")
    
    # Build Graph
    G = build_from_json(extraction)
    
    if G.number_of_nodes() == 0:
        print("ERROR: Graph is empty - extraction produced no nodes.")
        sys.exit(1)
        
    # Cluster Communities
    communities = cluster(G)
    cohesion = score_all(G, communities)
    
    tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    labels = {cid: 'Community ' + str(cid) for cid in communities}
    
    # Suggest questions
    questions = suggest_questions(G, communities, labels)
    
    # Generate report
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, tokens, input_path, suggested_questions=questions)
    
    report_path = out_dir / "GRAPH_REPORT.md"
    report_path.write_text(report, encoding='utf-8')
    
    # Save graph.json
    graph_json_path = out_dir / "graph.json"
    to_json(G, communities, str(graph_json_path))
    
    # Save analysis.json
    analysis = {
        'communities': {str(k): v for k, v in communities.items()},
        'cohesion': {str(k): v for k, v in cohesion.items()},
        'gods': gods,
        'surprises': surprises,
        'questions': questions,
    }
    analysis_path = out_dir / ".graphify_analysis.json"
    analysis_path.write_text(json.dumps(analysis, indent=2), encoding='utf-8')
    
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(communities)} communities")
    print(f"Report saved to {report_path}")
    print(f"Graph JSON saved to {graph_json_path}")

if __name__ == '__main__':
    main()
