#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join, relative } from "node:path";
import scanner from "/home/chihwei/.understand-anything/repo/understand-anything-plugin/skills/understand/scan-project.mjs";

const [projectRoot, rawScanPath, outputPath] = process.argv.slice(2);

if (!projectRoot || !rawScanPath || !outputPath) {
  process.stderr.write("Usage: node scan-submodules.mjs <projectRoot> <rawScanPath> <outputPath>\n");
  process.exit(1);
}

function git(args, cwd) {
  return execFileSync("git", args, { cwd, encoding: "utf8" }).trim();
}

function parseGitmodules() {
  const p = join(projectRoot, ".gitmodules");
  if (!existsSync(p)) return [];
  const out = git(["config", "--file", ".gitmodules", "--get-regexp", "path"], projectRoot);
  return out
    .split("\n")
    .map((line) => line.trim().split(/\s+/).at(-1))
    .filter(Boolean);
}

function targetSubmodules() {
  return parseGitmodules()
    .filter((path) => path.startsWith("oh-my-"))
    .sort((a, b) => a.localeCompare(b));
}

function lineCount(path) {
  const content = readFileSync(path, "utf8");
  if (content.length === 0) return 0;
  return content.endsWith("\n") ? content.split("\n").length - 1 : content.split("\n").length;
}

function fileEntry(relPath) {
  const abs = join(projectRoot, relPath);
  const st = statSync(abs);
  if (!st.isFile()) return null;
  return {
    path: relPath,
    language: scanner.detectLanguage(relPath),
    sizeLines: lineCount(abs),
    fileCategory: scanner.detectCategory(relPath),
  };
}

const raw = JSON.parse(readFileSync(rawScanPath, "utf8"));
const byPath = new Map();
const submodules = targetSubmodules();

for (const submodule of submodules) {
  const subRoot = join(projectRoot, submodule);
  const files = git(["ls-files", "-z"], subRoot).split("\0").filter(Boolean);
  for (const f of files) {
    const relPath = relative(projectRoot, join(subRoot, f)).split("/").join("/");
    if (
      relPath.startsWith(".understand-anything/") ||
      relPath.startsWith("graphify-out/") ||
      relPath.startsWith("docs-html/")
    ) {
      continue;
    }
    const entry = fileEntry(relPath);
    if (entry) byPath.set(relPath, entry);
  }
}

const files = [...byPath.values()].sort((a, b) => a.path.localeCompare(b.path));
const byCategory = {};
const byLanguage = {};

for (const f of files) {
  byCategory[f.fileCategory] = (byCategory[f.fileCategory] || 0) + 1;
  byLanguage[f.language] = (byLanguage[f.language] || 0) + 1;
}

const output = {
  scriptCompleted: true,
  projectRoot,
  name: "ohmyxxx-study",
  rawDescription: `Study workspace graph focused only on these oh-my submodules: ${submodules.join(", ")}.`,
  readmeHead: existsSync(join(projectRoot, "README.md"))
    ? readFileSync(join(projectRoot, "README.md"), "utf8").split("\n").slice(0, 40).join("\n")
    : "",
  frameworks: [],
  submodules,
  languages: Object.keys(byLanguage).sort(),
  files,
  totalFiles: files.length,
  filteredByIgnore: raw.filteredByIgnore,
  estimatedComplexity: scanner.estimateComplexity(files.length),
  stats: {
    filesScanned: files.length,
    byCategory,
    byLanguage,
  },
};

writeFileSync(outputPath, JSON.stringify(output, null, 2), "utf8");
process.stderr.write(`scan-submodules: filesScanned=${files.length} complexity=${output.estimatedComplexity}\n`);
