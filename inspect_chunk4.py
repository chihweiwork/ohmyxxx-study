import os
import re
import json

workspace = "/home/chihwei/playground/ohmyxxx-study"
files = [
    "oh-my-claudecode/skills/cancel/SKILL.md",
    "oh-my-claudecode/skills/setup/SKILL.md",
    "oh-my-claudecode/skills/ask/SKILL.md",
    "oh-my-claudecode/skills/remember/SKILL.md",
    "oh-my-claudecode/skills/omc-reference/SKILL.md",
    "oh-my-claudecode/skills/writer-memory/SKILL.md",
    "oh-my-claudecode/skills/writer-memory/templates/synopsis-template.md",
    "oh-my-claudecode/skills/project-session-manager/SKILL.md",
    "oh-my-claudecode/skills/project-session-manager/templates/pr-review.md",
    "oh-my-claudecode/skills/project-session-manager/templates/feature.md",
    "oh-my-claudecode/skills/project-session-manager/templates/issue-fix.md",
    "oh-my-claudecode/skills/external-context/SKILL.md",
    "oh-my-claudecode/skills/release/SKILL.md",
    "oh-my-claudecode/skills/verify/SKILL.md",
    "oh-my-claudecode/skills/ultragoal/SKILL.md",
    "oh-my-claudecode/skills/omc-doctor/SKILL.md",
    "oh-my-claudecode/skills/debug/SKILL.md",
    "oh-my-claudecode/skills/deep-dive/SKILL.md",
    "oh-my-claudecode/benchmark/README.md",
    "oh-my-claudecode/benchmark/results/README.md",
    "oh-my-claudecode/templates/rules/README.md",
    "oh-my-claudecode/docs/CLAUDE.md",
    "oh-my-claudecode/docs/ARCHITECTURE.md",
    "oh-my-claudecode/docs/AGENTS.md",
    "oh-my-claudecode/docs/design/CLAUDE_CODE_GOAL_ADAPTER.md",
    "oh-my-claudecode/docs/design/TIERED_AGENTS_V2.md",
    "oh-my-claudecode/docs/agents/model-compatibility.md",
    "oh-my-claudecode/docs/agent-templates/README.md",
    "oh-my-claudecode/seminar/demos/README.md",
    "oh-my-claudecode/seminar/screenshots/README.md",
    "oh-my-claudecode/src/AGENTS.md",
    "oh-my-claudecode/src/tools/AGENTS.md",
    "oh-my-claudecode/src/tools/lsp/AGENTS.md",
    "oh-my-claudecode/src/tools/diagnostics/AGENTS.md",
    "oh-my-claudecode/src/hooks/AGENTS.md",
    "oh-my-claudecode/src/hooks/setup/README.md",
    "oh-my-claudecode/src/features/AGENTS.md"
]

results = {}
for f in files:
    path = os.path.join(workspace, f)
    if not os.path.exists(path):
        results[f] = {"error": "File not found"}
        continue
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Extract title (# Title)
    title_m = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else None
    
    # Extract name/description frontmatter or other tags
    name_m = re.search(r"^name:\s*(\S+)", content, re.MULTILINE)
    desc_m = re.search(r"^description:\s*(.+)", content, re.MULTILINE)
    
    name = name_m.group(1).strip() if name_m else None
    desc = desc_m.group(1).strip() if desc_m else None
    
    # Extract all markdown links
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
    
    results[f] = {
        "title": title,
        "name": name,
        "description": desc,
        "links": links,
        "content_preview": content[:600]
    }

print(json.dumps(results, indent=2))
