import json
import os
import re
from pathlib import Path

base_dir = Path("/home/chihwei/playground/ohmyxxx-study")
out_dir = base_dir / "graphify-out"

PROJECT_ROOTS = [
    "oh-my-openagent",
    "oh-my-claudecode",
    "oh-my-codex",
    "oh-my-antigravity",
]

TEXT_EXTENSIONS = {".md", ".txt", ".rst", ".toml"}
SKIP_PARTS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "target",
    "docs-html",
    "graphify-out",
    "__pycache__",
}


def is_target_surface(rel_path):
    path = Path(rel_path)
    parts = path.parts
    name = path.name
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return False
    if any(part in SKIP_PARTS for part in parts):
        return False
    if name in {"AGENTS.md", "GEMINI.md", "CLAUDE.md", "DESIGN.md"}:
        return True
    if name.startswith("README") and path.suffix.lower() == ".md":
        return True
    surface_dirs = {
        "agents",
        "commands",
        "context",
        "docs",
        "hooks",
        "prompts",
        "skills",
        "templates",
    }
    if any(part in surface_dirs for part in parts):
        return True
    if "packages" in parts and ("prompts-core" in parts or "omo-codex" in parts):
        return True
    return False


def collect_targeted_files():
    files = []
    for root_name in PROJECT_ROOTS:
        root = base_dir / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(base_dir).as_posix()
            if is_target_surface(rel):
                files.append(rel)
    return sorted(dict.fromkeys(files))


def write_targeted_chunks(files, chunk_size=42):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / ".graphify_targeted_files.txt").write_text(
        "\n".join(files) + ("\n" if files else ""),
        encoding="utf-8",
    )
    (out_dir / ".graphify_targeted_files_clean.txt").write_text(
        "\n".join(files) + ("\n" if files else ""),
        encoding="utf-8",
    )

    for old_chunk in out_dir.glob(".graphify_targeted_chunk_*.txt"):
        old_chunk.unlink()

    for index in range(0, len(files), chunk_size):
        chunk_id = index // chunk_size
        chunk = files[index:index + chunk_size]
        (out_dir / f".graphify_targeted_chunk_{chunk_id}.txt").write_text(
            "\n".join(chunk) + "\n",
            encoding="utf-8",
        )
    return (len(files) + chunk_size - 1) // chunk_size if files else 0


def node_info(rel_path):
    path = Path(rel_path)
    stem = path.stem
    parts = path.parts
    repo = parts[0] if parts else "root"
    parent_dir = parts[-2] if len(parts) >= 2 else "root"
    path_slug = re.sub(r"[^a-zA-Z0-9]+", "_", rel_path).strip("_").lower()

    if stem.upper() in ["SKILL", "README", "AGENTS", "GEMINI", "CLAUDE", "DESIGN"]:
        node_id = path_slug
        default_label = f"[{repo}] {parent_dir.replace('-', ' ').title()} {stem.upper()}"
        match_name = parent_dir
    else:
        node_id = path_slug
        default_label = f"[{repo}] {stem.replace('-', ' ').title()}"
        match_name = stem
    return node_id, default_label, match_name, stem


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def process_chunk(chunk_id):
    chunk_txt = out_dir / f".graphify_targeted_chunk_{chunk_id}.txt"
    if not chunk_txt.exists():
        print(f"Chunk file {chunk_txt} not found.")
        return

    files = [line.strip() for line in chunk_txt.read_text(encoding="utf-8").splitlines() if line.strip()]
    nodes = []
    edges = []

    for rel in files:
        path = base_dir / rel
        if not path.exists():
            continue

        content = read_text(path)
        node_id, default_label, _, _ = node_info(rel)
        header_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        label = header_match.group(1).strip() if header_match else default_label
        label = re.sub(r"[*`_]", "", label)

        nodes.append({
            "id": node_id,
            "label": label,
            "file_type": "document",
            "source_file": rel,
            "source_location": None,
            "source_url": None,
            "captured_at": None,
            "author": None,
            "contributor": None,
        })

    global_files_path = out_dir / ".graphify_targeted_files.txt"
    global_files = [
        line.strip()
        for line in global_files_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ] if global_files_path.exists() else []

    global_targets = []
    for rel in global_files:
        node_id, _, match_name, stem = node_info(rel)
        global_targets.append({
            "file": rel,
            "node_id": node_id,
            "match_name": match_name,
            "stem": stem,
        })

    for rel in files:
        path = base_dir / rel
        if not path.exists():
            continue
        content = read_text(path)
        source_id, _, _, _ = node_info(rel)

        for target in global_targets:
            if target["file"] == rel:
                continue

            match_name = target["match_name"]
            pattern = rf"\b{re.escape(match_name)}\b"
            mentioned = re.search(pattern, content, re.IGNORECASE) or re.search(
                rf"\b{re.escape(match_name)}\.md\b",
                content,
                re.IGNORECASE,
            )
            if not mentioned:
                continue

            context = ""
            match = re.search(rf"(.{{0,50}}\b{re.escape(match_name)}\b.{{0,50}})", content, re.IGNORECASE)
            if match:
                context = match.group(1).lower()

            relation = "references"
            confidence_score = 0.9
            if any(word in context for word in ["call", "invoke", "delegate", "dispatch"]):
                relation = "calls"
                confidence_score = 0.95
            elif any(word in context for word in ["implement", "realize", "provide"]):
                relation = "implements"
                confidence_score = 0.95
            elif any(word in context for word in ["similar", "like", "parity"]):
                relation = "semantically_similar_to"
                confidence_score = 0.8
            elif any(word in context for word in ["relate", "connect", "coordinate"]):
                relation = "conceptually_related_to"
                confidence_score = 0.8

            edges.append({
                "source": source_id,
                "target": target["node_id"],
                "relation": relation,
                "confidence": "EXTRACTED",
                "confidence_score": confidence_score,
                "source_file": rel,
                "source_location": None,
                "weight": 1.0,
            })

    out_path = out_dir / f".graphify_chunk_{chunk_id}.json"
    out_path.write_text(
        json.dumps({
            "nodes": nodes,
            "edges": edges,
            "hyperedges": [],
            "input_tokens": 0,
            "output_tokens": 0,
        }, indent=2),
        encoding="utf-8",
    )

    print(f"Chunk {chunk_id}: Extracted {len(nodes)} nodes and {len(edges)} edges. Saved to {out_path}")


def main():
    files = collect_targeted_files()
    chunk_count = write_targeted_chunks(files)

    for old_chunk in out_dir.glob(".graphify_chunk_*.json"):
        old_chunk.unlink()

    print(f"Targeted files: {len(files)} across {chunk_count} chunk(s)")
    for chunk_id in range(chunk_count):
        process_chunk(chunk_id)


if __name__ == "__main__":
    main()
