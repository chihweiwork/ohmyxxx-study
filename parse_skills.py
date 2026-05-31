import os
import json
import re

workspace = "/home/chihwei/playground/ohmyxxx-study"
files = [
  "oh-my-claudecode/skills/AGENTS.md",
  "oh-my-claudecode/skills/deep-interview/SKILL.md",
  "oh-my-claudecode/skills/ccg/SKILL.md",
  "oh-my-claudecode/skills/self-improve/si-goal-clarifier.md",
  "oh-my-claudecode/skills/self-improve/data_contracts.md",
  "oh-my-claudecode/skills/self-improve/si-researcher.md",
  "oh-my-claudecode/skills/self-improve/si-benchmark-builder.md",
  "oh-my-claudecode/skills/self-improve/SKILL.md",
  "oh-my-claudecode/skills/self-improve/templates/harness.md",
  "oh-my-claudecode/skills/self-improve/templates/goal.md",
  "oh-my-claudecode/skills/self-improve/templates/idea.md",
  "oh-my-claudecode/skills/deepinit/SKILL.md",
  "oh-my-claudecode/skills/ai-slop-cleaner/SKILL.md",
  "oh-my-claudecode/skills/autoresearch/SKILL.md",
  "oh-my-claudecode/skills/omc-teams/SKILL.md",
  "oh-my-claudecode/skills/hud/SKILL.md",
  "oh-my-claudecode/skills/skillify/SKILL.md",
  "oh-my-claudecode/skills/mcp-setup/SKILL.md",
  "oh-my-claudecode/skills/sciomc/SKILL.md",
  "oh-my-claudecode/skills/visual-verdict/SKILL.md",
  "oh-my-claudecode/skills/ralplan/SKILL.md",
  "oh-my-claudecode/skills/autopilot/SKILL.md",
  "oh-my-claudecode/skills/plan/SKILL.md",
  "oh-my-claudecode/skills/learner/SKILL.md",
  "oh-my-claudecode/skills/omc-setup/SKILL.md",
  "oh-my-claudecode/skills/omc-setup/phases/04-welcome.md",
  "oh-my-claudecode/skills/omc-setup/phases/01-install-claude-md.md",
  "oh-my-claudecode/skills/omc-setup/phases/03-integrations.md",
  "oh-my-claudecode/skills/omc-setup/phases/02-configure.md",
  "oh-my-claudecode/skills/team/SKILL.md",
  "oh-my-claudecode/skills/ralph/SKILL.md",
  "oh-my-claudecode/skills/skill/SKILL.md",
  "oh-my-claudecode/skills/wiki/SKILL.md",
  "oh-my-claudecode/skills/ultrawork/SKILL.md",
  "oh-my-claudecode/skills/ultraqa/SKILL.md",
  "oh-my-claudecode/skills/trace/SKILL.md",
  "oh-my-claudecode/skills/configure-notifications/SKILL.md"
]

results = []
for f in files:
    path = os.path.join(workspace, f)
    if not os.path.exists(path):
        print(f"NOT FOUND: {f}")
        continue
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Simple extraction of title, frontmatter name
    name_match = re.search(r"^name:\s*(\S+)", content, re.MULTILINE)
    h1_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    
    name = name_match.group(1) if name_match else None
    h1 = h1_match.group(1).strip() if h1_match else None
    
    # Get relative stem name
    parts = f.split('/')
    if len(parts) >= 2:
        if parts[-1] == "SKILL.md":
            stem = f"{parts[-2]}_skill"
        else:
            stem = f"{parts[-2]}_{parts[-1].replace('.md', '')}"
    else:
        stem = f.replace('.md', '')
    
    results.append({
        "file": f,
        "stem": stem,
        "name": name,
        "h1": h1,
        "content_length": len(content),
        "sample": content[:200]
    })

print(json.dumps(results, indent=2))
