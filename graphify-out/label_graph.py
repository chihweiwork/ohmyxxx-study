import json
import sys
from collections import Counter
from pathlib import Path

from graphify.analyze import suggest_questions
from graphify.build import build_from_json
from graphify.report import generate

input_path = "/home/chihwei/playground/ohmyxxx-study"
out_dir = Path("/home/chihwei/playground/ohmyxxx-study/graphify-out")


def normalize_part(part):
    return part.replace("-", " ").replace("_", " ").title()


def community_label(members, node_sources):
    paths = [node_sources.get(node_id, "") for node_id in members]
    paths = [path for path in paths if path]
    if not paths:
        return "Mixed Study Surface"

    repo_counts = Counter(path.split("/", 1)[0] for path in paths)
    area_counts = Counter()
    for path in paths:
        parts = path.split("/")
        repo = parts[0]
        area = parts[1] if len(parts) > 1 else "root"
        if area == "packages" and len(parts) > 2:
            area = f"packages/{parts[2]}"
        area_counts[f"{repo}/{area}"] += 1

    top_repos = [normalize_part(repo) for repo, _ in repo_counts.most_common(2)]
    top_areas = [area.replace("-", " ") for area, _ in area_counts.most_common(2)]
    return f"{' + '.join(top_repos)}: {' / '.join(top_areas)}"


def main():
    extraction_path = out_dir / ".graphify_extract.json"
    detect_path = out_dir / ".graphify_detect.json"
    analysis_path = out_dir / ".graphify_analysis.json"

    if not all([p.exists() for p in [extraction_path, detect_path, analysis_path]]):
        print("Error: Required graphify-out files (.graphify_extract.json, .graphify_detect.json, .graphify_analysis.json) are missing.")
        sys.exit(1)

    extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
    detection = json.loads(detect_path.read_text(encoding="utf-8"))
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))

    G = build_from_json(extraction)
    communities = {int(k): v for k, v in analysis["communities"].items()}
    cohesion = {int(k): v for k, v in analysis["cohesion"].items()}
    tokens = {"input": extraction.get("input_tokens", 0), "output": extraction.get("output_tokens", 0)}
    node_sources = {node["id"]: node.get("source_file", "") for node in extraction.get("nodes", [])}

    labels = {
        cid: community_label(members, node_sources)
        for cid, members in communities.items()
    }
    questions = suggest_questions(G, communities, labels)

    report = generate(
        G,
        communities,
        cohesion,
        labels,
        analysis["gods"],
        analysis["surprises"],
        detection,
        tokens,
        input_path,
        suggested_questions=questions,
    )

    (out_dir / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    (out_dir / ".graphify_labels.json").write_text(
        json.dumps({str(k): v for k, v in labels.items()}, indent=2),
        encoding="utf-8",
    )

    print("Report successfully updated with dynamic community labels.")


if __name__ == "__main__":
    main()
