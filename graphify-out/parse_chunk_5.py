import os
import re
import yaml
import json

base_dir = "/home/chihwei/playground/ohmyxxx-study"
files = [
    "oh-my-claudecode/src/features/verification/README.md",
    "oh-my-claudecode/src/features/delegation-categories/README.md",
    "oh-my-claudecode/src/agents/AGENTS.md",
    "oh-my-claudecode/src/agents/templates/exploration-template.md",
    "oh-my-claudecode/src/agents/templates/implementation-template.md",
    "oh-my-claudecode/agents/architect.md",
    "oh-my-claudecode/agents/document-specialist.md",
    "oh-my-claudecode/agents/scientist.md",
    "oh-my-claudecode/agents/designer.md",
    "oh-my-claudecode/agents/qa-tester.md",
    "oh-my-claudecode/agents/verifier.md",
    "oh-my-claudecode/agents/security-reviewer.md",
    "oh-my-claudecode/agents/code-reviewer.md",
    "oh-my-claudecode/agents/debugger.md",
    "oh-my-claudecode/agents/analyst.md",
    "oh-my-claudecode/agents/explore.md",
    "oh-my-claudecode/agents/tracer.md",
    "oh-my-claudecode/agents/writer.md",
    "oh-my-claudecode/agents/executor.md",
    "oh-my-claudecode/agents/critic.md",
    "oh-my-claudecode/agents/test-engineer.md",
    "oh-my-claudecode/agents/planner.md",
    "oh-my-claudecode/agents/git-master.md",
    "oh-my-claudecode/agents/code-simplifier.md",
    "oh-my-claudecode/examples/vendor-mcp-server/README.md",
    "oh-my-codex/README.md",
    "oh-my-codex/prompts/architect.md",
    "oh-my-codex/prompts/quality-reviewer.md",
    "oh-my-codex/prompts/researcher.md",
    "oh-my-codex/prompts/designer.md",
    "oh-my-codex/prompts/api-reviewer.md",
    "oh-my-codex/prompts/scholastic.md",
    "oh-my-codex/prompts/qa-tester.md",
    "oh-my-codex/prompts/prometheus-strict-oracle.md",
    "oh-my-codex/prompts/prometheus-strict-metis.md",
    "oh-my-codex/prompts/prometheus-strict-momus.md",
    "oh-my-codex/prompts/team-orchestrator.md"
]

nodes = []
edges = []

# Helper to identify and register nodes and details
for rel_path in files:
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"Missing: {rel_path}")
        continue
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Parse YAML frontmatter if any
    frontmatter = {}
    main_body = content
    if content.startswith("---"):
        match = re.match(r"^---([\s\S]*?)---\s*([\s\S]*)$", content)
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1)) or {}
                main_body = match.group(2)
            except Exception as e:
                pass
    
    # Determine label and entity name
    stem = os.path.splitext(os.path.basename(rel_path))[0]
    folder = os.path.basename(os.path.dirname(rel_path))
    
    # Unique ID format: {project}_{folder}_{stem}_{entityname}
    project = "omc" if "claudecode" in rel_path else "omx"
    entity_name = frontmatter.get("name", stem)
    node_id = f"{project}_{folder}_{stem}_{entity_name}".replace("-", "_")
    
    # Friendly label
    label = f"{project.upper()} {folder.capitalize()} {stem.capitalize()}"
    if entity_name != stem:
        label += f" ({entity_name})"
    
    # If it is a readme or AGENTS file
    if stem == "README":
        if folder == "verification":
            label = "OMC Verification Module"
        elif folder == "delegation-categories":
            label = "OMC Delegation Categories"
        elif folder == "vendor-mcp-server":
            label = "OMC Vendor MCP Server"
        elif folder == "oh-my-codex":
            label = "OMX Core Readme"
    elif stem == "AGENTS":
        label = "OMC Agents Registry"
    
    nodes.append({
        "id": node_id,
        "label": label,
        "file_type": "document",
        "source_file": rel_path,
        "source_location": None,
        "source_url": None,
        "captured_at": None,
        "author": None,
        "contributor": None
    })

print(f"Generated {len(nodes)} nodes.")
for n in nodes[:5]:
    print(n)
