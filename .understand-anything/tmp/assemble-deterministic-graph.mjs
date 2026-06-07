#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { basename, dirname } from "node:path";
import { readFileSync, writeFileSync } from "node:fs";

const projectRoot = process.cwd();
const scan = JSON.parse(readFileSync(".understand-anything/intermediate/scan-result.json", "utf8"));
const imports = JSON.parse(readFileSync(".understand-anything/intermediate/import-map.json", "utf8"));
const structure = JSON.parse(readFileSync(".understand-anything/intermediate/structure-result.json", "utf8"));

function gitHead() {
  try {
    return execFileSync("git", ["rev-parse", "HEAD"], { cwd: projectRoot, encoding: "utf8" }).trim();
  } catch {
    return "unknown";
  }
}

function complexity(lines) {
  if (lines <= 80) return "simple";
  if (lines <= 300) return "moderate";
  return "complex";
}

function nodeTypeForFile(file) {
  if (file.fileCategory === "config") return "config";
  if (file.fileCategory === "documentation") return "document";
  if (file.language === "sql") return "table";
  if (["terraform", "dockerfile"].includes(file.language)) return "resource";
  if (["yaml", "yml"].includes(file.language) && file.path.includes("workflow")) return "pipeline";
  return "file";
}

function prefixForType(type) {
  return {
    file: "file",
    function: "func",
    class: "class",
    config: "config",
    document: "document",
    service: "service",
    table: "table",
    endpoint: "endpoint",
    pipeline: "pipeline",
    schema: "schema",
    resource: "resource",
  }[type] || "file";
}

function addNode(map, node) {
  if (!map.has(node.id)) map.set(node.id, node);
}

function edgeKey(e) {
  return `${e.source}\u0000${e.target}\u0000${e.type}`;
}

function addEdge(map, edge) {
  if (edge.source === edge.target) return;
  map.set(edgeKey(edge), edge);
}

function pathLayer(path) {
  if (path.startsWith("oh-my-codex/")) return "oh-my-codex";
  if (path.startsWith("oh-my-claudecode/")) return "oh-my-claudecode";
  if (path.startsWith("oh-my-openagent/")) return "oh-my-openagent";
  if (path.startsWith("oh-my-antigravity/")) return "oh-my-antigravity";
  if (path.startsWith("docs/")) return "study-docs";
  if (path.startsWith("scripts/")) return "study-scripts";
  return "root";
}

const nodes = new Map();
const edges = new Map();
const fileNodeId = new Map();

for (const file of scan.files) {
  const type = nodeTypeForFile(file);
  const id = `${prefixForType(type)}:${file.path}`;
  fileNodeId.set(file.path, id);
  addNode(nodes, {
    id,
    type,
    name: basename(file.path),
    filePath: file.path,
    summary: `靜態掃描節點：${file.path}，語言 ${file.language}，分類 ${file.fileCategory}，約 ${file.sizeLines} 行。`,
    tags: [file.language, file.fileCategory, pathLayer(file.path)].filter(Boolean),
    complexity: complexity(file.sizeLines),
    languageNotes: `由 understand-anything deterministic scanner 產生；未使用 LLM 語意推論。`,
  });
}

for (const [sourcePath, targets] of Object.entries(imports.importMap || {})) {
  const source = fileNodeId.get(sourcePath);
  if (!source) continue;
  for (const targetPath of targets) {
    const target = fileNodeId.get(targetPath);
    if (!target) continue;
    addEdge(edges, {
      source,
      target,
      type: "imports",
      direction: "forward",
      description: `${sourcePath} imports ${targetPath}`,
      weight: 0.85,
    });
  }
}

for (const result of structure.results || []) {
  const parent = fileNodeId.get(result.path);
  if (!parent) continue;

  for (const fn of result.functions || []) {
    const id = `func:${result.path}:${fn.name}`;
    addNode(nodes, {
      id,
      type: "function",
      name: fn.name,
      filePath: result.path,
      lineRange: [fn.startLine, fn.endLine],
      summary: `函式 ${fn.name}，位於 ${result.path}:${fn.startLine}-${fn.endLine}。`,
      tags: [result.language, "function", pathLayer(result.path)],
      complexity: complexity((fn.endLine || fn.startLine) - (fn.startLine || 0) + 1),
    });
    addEdge(edges, { source: parent, target: id, type: "contains", direction: "forward", weight: 0.7 });
  }

  for (const cls of result.classes || []) {
    const id = `class:${result.path}:${cls.name}`;
    addNode(nodes, {
      id,
      type: "class",
      name: cls.name,
      filePath: result.path,
      lineRange: [cls.startLine, cls.endLine],
      summary: `類別/型別 ${cls.name}，位於 ${result.path}:${cls.startLine}-${cls.endLine}。`,
      tags: [result.language, "class", pathLayer(result.path)],
      complexity: complexity((cls.endLine || cls.startLine) - (cls.startLine || 0) + 1),
    });
    addEdge(edges, { source: parent, target: id, type: "contains", direction: "forward", weight: 0.7 });
  }

  for (const exp of result.exports || []) {
    const target = nodes.has(`func:${result.path}:${exp.name}`)
      ? `func:${result.path}:${exp.name}`
      : nodes.has(`class:${result.path}:${exp.name}`)
        ? `class:${result.path}:${exp.name}`
        : parent;
    addEdge(edges, { source: parent, target, type: "exports", direction: "forward", weight: 0.5 });
  }

  const structuralGroups = [
    ["sections", "document", "documents"],
    ["definitions", "schema", "defines_schema"],
    ["services", "service", "configures"],
    ["endpoints", "endpoint", "routes"],
    ["steps", "pipeline", "triggers"],
    ["resources", "resource", "provisions"],
  ];

  for (const [key, type, edgeType] of structuralGroups) {
    for (const item of result[key] || []) {
      const rawName = item.heading || item.name || item.path || item.kind || key;
      const id = `${prefixForType(type)}:${result.path}:${rawName}`;
      addNode(nodes, {
        id,
        type,
        name: rawName,
        filePath: result.path,
        lineRange: item.line ? [item.line, item.line] : item.startLine ? [item.startLine, item.endLine] : undefined,
        summary: `結構項目 ${rawName}，由 ${result.path} 解析而來。`,
        tags: [result.language, key, pathLayer(result.path)],
        complexity: "simple",
      });
      addEdge(edges, { source: parent, target: id, type: edgeType, direction: "forward", weight: 0.55 });
    }
  }

  for (const cg of result.callGraph || []) {
    const source = `func:${result.path}:${cg.caller}`;
    const target = `func:${result.path}:${cg.callee}`;
    if (nodes.has(source) && nodes.has(target)) {
      addEdge(edges, { source, target, type: "calls", direction: "forward", weight: 0.6 });
    }
  }
}

const layerNodes = new Map();
for (const node of nodes.values()) {
  const layer = pathLayer(node.filePath || "");
  if (!layerNodes.has(layer)) layerNodes.set(layer, []);
  layerNodes.get(layer).push(node.id);
}

const layerNames = {
  root: "Study root",
  "study-docs": "Study documentation",
  "study-scripts": "Study scripts",
  "oh-my-codex": "oh-my-codex submodule",
  "oh-my-claudecode": "oh-my-claudecode submodule",
  "oh-my-openagent": "oh-my-openagent submodule",
  "oh-my-antigravity": "oh-my-antigravity submodule",
};

const layers = [...layerNodes.entries()].sort().map(([id, nodeIds]) => ({
  id,
  name: layerNames[id] || id,
  description: `包含 ${id} 範圍內由靜態掃描建立的節點。`,
  nodeIds,
}));

const topLayerIds = [...layerNodes.keys()].sort().map((id) => layerNodes.get(id)[0]).filter(Boolean);

const graph = {
  version: "1.0.0",
  kind: "codebase",
  project: {
    name: scan.name || "ohmyxxx-study",
    languages: scan.languages,
    frameworks: scan.frameworks || [],
    description: scan.rawDescription,
    analyzedAt: new Date().toISOString(),
    gitCommitHash: gitHead(),
  },
  nodes: [...nodes.values()],
  edges: [...edges.values()].filter((e) => nodes.has(e.source) && nodes.has(e.target)),
  layers,
  tour: [
    {
      order: 1,
      title: "專案總覽",
      description: "從 root 與各 submodule layer 開始，檢視 study repo 與三個主要工具專案的關係。",
      nodeIds: topLayerIds.slice(0, 8),
      languageLesson: "此圖由靜態掃描與 import/structure extraction 產生，適合先看檔案關係與結構熱點。",
    },
    {
      order: 2,
      title: "依 imports 追蹤",
      description: "沿著 imports edges 查看各套工具內部模組依賴。",
      nodeIds: [...nodes.keys()].filter((id) => id.startsWith("file:")).slice(0, 8),
    },
  ],
};

writeFileSync(".understand-anything/intermediate/assembled-graph.json", JSON.stringify(graph, null, 2), "utf8");
writeFileSync(".understand-anything/knowledge-graph.json", JSON.stringify(graph, null, 2), "utf8");
process.stderr.write(`assemble: nodes=${graph.nodes.length} edges=${graph.edges.length} layers=${graph.layers.length}\n`);
