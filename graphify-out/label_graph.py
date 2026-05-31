import sys
import json
from pathlib import Path
from graphify.build import build_from_json
from graphify.cluster import score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate

# Paths
input_path = "/home/chihwei/playground/ohmyxxx-study"
out_dir = Path("/home/chihwei/playground/ohmyxxx-study/graphify-out")

# Define community labels dictionary
LABELS_DICT = {
    0: "Antigravity CLI Framework",
    1: "OpenCode OpenAgent Orchestration",
    2: "OpenAgent Specialized Personas",
    3: "Claude Code Specialized Agents",
    4: "Codex Specialized Prompts",
    5: "Claude Code Compatibility Commands",
    6: "OpenCode Hooks and Tools",
    7: "Codex Local Advisor Skills",
    8: "Claude Code Core Skills & Design",
    9: "Claude Code Self-Improvement Workflow",
    10: "Agent Autoresearch Showcase & Missions",
    11: "OpenCode Atlas Multi-Model Prompts",
    12: "Claude Code Agent Templates & Matrix",
    13: "OpenCode Prometheus Prompts",
    14: "Claude Code Benchmarks",
    15: "Claude Code Seminar Showcases",
    16: "Codex Wiki System",
    17: "Claude-Codex-Gemini Interoperability",
    18: "Codex Wiki Skill",
    19: "Evidence-Driven Tracing",
    20: "Claude Code Notifications",
    21: "Claude Code Memory",
    22: "Claude Code Diagnostics",
    23: "Claude Code Rules Engine",
    24: "Claude Code Vendor MCP Contract",
    25: "Codex Explore Prompt",
    26: "Codex SparkShell Prompt"
}

def main():
    extraction_path = out_dir / ".graphify_extract.json"
    detect_path = out_dir / ".graphify_detect.json"
    analysis_path = out_dir / ".graphify_analysis.json"
    
    if not all([p.exists() for p in [extraction_path, detect_path, analysis_path]]):
        print("Error: Required graphify-out files (.graphify_extract.json, .graphify_detect.json, .graphify_analysis.json) are missing.")
        sys.exit(1)
        
    extraction = json.loads(extraction_path.read_text(encoding='utf-8'))
    detection = json.loads(detect_path.read_text(encoding='utf-8'))
    analysis = json.loads(analysis_path.read_text(encoding='utf-8'))
    
    G = build_from_json(extraction)
    communities = {int(k): v for k, v in analysis['communities'].items()}
    cohesion = {int(k): v for k, v in analysis['cohesion'].items()}
    tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}
    
    # Fill missing labels just in case
    for cid in communities:
        if cid not in LABELS_DICT:
            LABELS_DICT[cid] = f"Community {cid}"
            
    # Regenerate questions with real community labels
    questions = suggest_questions(G, communities, LABELS_DICT)
    
    # Generate report
    report = generate(G, communities, cohesion, LABELS_DICT, analysis['gods'], analysis['surprises'], detection, tokens, input_path, suggested_questions=questions)
    
    report_path = out_dir / "GRAPH_REPORT.md"
    report_path.write_text(report, encoding='utf-8')
    
    labels_path = out_dir / ".graphify_labels.json"
    labels_path.write_text(json.dumps({str(k): v for k, v in LABELS_DICT.items()}, indent=2), encoding='utf-8')
    
    print("Report successfully updated with community labels.")

if __name__ == '__main__':
    main()
