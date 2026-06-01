import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const manifestPath = path.join(root, "docs-html", "sources-manifest.json");
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
const outDir = path.join(root, "docs-html", "sources");
const cacheDir = path.join(root, "docs-html", ".translation-cache");
fs.mkdirSync(cacheDir, { recursive: true });

const model = process.env.CODEX_TRANSLATE_MODEL || "gpt-5.4-mini";
const only = process.env.TRANSLATE_ONLY || "";
const limit = Number(process.env.TRANSLATE_LIMIT || "0");
const cacheOnly = process.env.TRANSLATE_CACHE_ONLY === "1";

function sourceName(p) {
  return p.replace(/[^a-zA-Z0-9]+/g, "_").replace(/^_+|_+$/g, "") + ".html";
}

function preservesOriginalTranslation(file) {
  return /^oh-my-openagent\/packages\/prompts-core\/prompts\/(atlas|prometheus)\/(gemini|gpt)\.md$/.test(file);
}

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function splitBlocks(text) {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const blocks = [];
  let buf = [];
  let inFence = false;
  for (const line of lines) {
    if (line.startsWith("```")) {
      buf.push(line);
      inFence = !inFence;
      continue;
    }
    if (!inFence && /^\s*$/.test(line)) {
      if (buf.length) {
        blocks.push(buf.join("\n"));
        buf = [];
      }
      continue;
    }
    buf.push(line);
  }
  if (buf.length) blocks.push(buf.join("\n"));
  return blocks;
}

function chunkBlocks(blocks, maxChars = 6500) {
  const chunks = [];
  let current = [];
  let size = 0;
  for (const block of blocks) {
    const blockSize = block.length + 2;
    if (current.length && size + blockSize > maxChars) {
      chunks.push(current);
      current = [];
      size = 0;
    }
    current.push(block);
    size += blockSize;
  }
  if (current.length) chunks.push(current);
  return chunks;
}

function stripCodexOutput(raw) {
  const trimmed = raw.trim();
  const firstArray = trimmed.indexOf("[");
  const lastArray = trimmed.lastIndexOf("]");
  if (firstArray === -1 || lastArray === -1 || lastArray <= firstArray) {
    throw new Error("No JSON array found in Codex output");
  }
  return trimmed.slice(firstArray, lastArray + 1);
}

function translateChunk(file, chunk, chunkIndex) {
  const cachePath = path.join(cacheDir, `${sourceName(file)}.${chunkIndex}.json`);
  if (fs.existsSync(cachePath)) {
    return normalizePairs(JSON.parse(fs.readFileSync(cachePath, "utf8")), chunk);
  }
  if (cacheOnly && preservesOriginalTranslation(file)) {
    console.warn(`  using original text for untranslated prompt variant chunk ${chunkIndex + 1}`);
    return chunk.map((original) => ({ original, zh_tw: original }));
  }
  if (cacheOnly) {
    throw new Error(`Missing cached translation: ${path.relative(root, cachePath)}`);
  }

  const prompt = buildPrompt(file, chunk);

  const tmpOut = path.join("/tmp", `codex-translation-${process.pid}-${chunkIndex}.json`);
  const result = spawnSync(
    "rtk",
    [
      "codex",
      "exec",
      "-m",
      model,
      "-s",
      "workspace-write",
      "--skip-git-repo-check",
      "--cd",
      root,
      "--output-last-message",
      tmpOut,
      "-",
    ],
    {
      input: prompt,
      encoding: "utf8",
      stdio: ["pipe", "inherit", "inherit"],
    },
  );
  if (result.status !== 0) {
    throw new Error(`codex exec failed for ${file} chunk ${chunkIndex}`);
  }
  const raw = fs.readFileSync(tmpOut, "utf8");
  let parsed;
  try {
    parsed = normalizePairs(JSON.parse(stripCodexOutput(raw)), chunk);
  } catch (error) {
    console.warn(`  retrying chunk ${chunkIndex + 1} block-by-block: ${error.message}`);
    parsed = [];
    for (let i = 0; i < chunk.length; i++) {
      parsed.push(...translateSingleBlock(file, chunk[i], chunkIndex, i));
    }
  }
  fs.writeFileSync(cachePath, JSON.stringify(parsed, null, 2));
  return parsed;
}

function buildPrompt(file, chunk) {
  const input = chunk.map((text, id) => ({ id, text }));
  return `你是專業技術文件翻譯員。請把下方 Markdown 逐段翻譯成繁體中文。\n\n規則：\n- 輸入是一個 JSON array，每個元素都有 id 與 text。\n- 請輸出同長度 JSON array，每個元素格式為 {\"id\": 原 id, \"original\": 原 text, \"zh_tw\": 繁體中文翻譯}。\n- 不可以合併、拆分、刪除或重排 block。\n- original 必須完全等於輸入 text，不可改字元、不可改換行。\n- zh_tw 請逐句翻譯，不摘要、不新增解釋。\n- 保留 frontmatter key、程式碼、路徑、函式名、XML tag、Markdown 結構，不要翻譯。\n- 如果整個 block 是程式碼、frontmatter、純路徑或 tag wrapper，只翻譯其中自然語言；無自然語言則 zh_tw 等於 original。\n- 只輸出 JSON，不要 markdown fence。\n\n來源檔案：${file}\n\nJSON input:\n${JSON.stringify(input, null, 2)}\n`;
}

function translateSingleBlock(file, block, chunkIndex, blockIndex) {
  const cachePath = path.join(cacheDir, `${sourceName(file)}.${chunkIndex}.${blockIndex}.json`);
  if (fs.existsSync(cachePath)) {
    return normalizePairs(JSON.parse(fs.readFileSync(cachePath, "utf8")), [block]);
  }
  if (cacheOnly) {
    throw new Error(`Missing cached translation: ${path.relative(root, cachePath)}`);
  }
  const prompt = buildPrompt(file, [block]);
  const tmpOut = path.join("/tmp", `codex-translation-${process.pid}-${chunkIndex}-${blockIndex}.json`);
  const result = spawnSync(
    "rtk",
    [
      "codex",
      "exec",
      "-m",
      model,
      "-s",
      "workspace-write",
      "--skip-git-repo-check",
      "--cd",
      root,
      "--output-last-message",
      tmpOut,
      "-",
    ],
    {
      input: prompt,
      encoding: "utf8",
      stdio: ["pipe", "inherit", "inherit"],
    },
  );
  if (result.status !== 0) {
    throw new Error(`codex exec failed for ${file} chunk ${chunkIndex} block ${blockIndex}`);
  }
  const raw = fs.readFileSync(tmpOut, "utf8");
  const parsed = normalizePairs(JSON.parse(stripCodexOutput(raw)), [block]);
  fs.writeFileSync(cachePath, JSON.stringify(parsed, null, 2));
  return parsed;
}

function normalizePairs(parsed, chunk) {
  if (!Array.isArray(parsed)) {
    throw new Error("Codex output is not an array");
  }
  if (parsed.length !== chunk.length) {
    throw new Error(`Codex output length mismatch: expected ${chunk.length}, got ${parsed.length}`);
  }
  const byId = new Map();
  for (const entry of parsed) {
    if (entry && typeof entry === "object" && Number.isInteger(entry.id)) {
      byId.set(entry.id, entry);
    }
  }
  const ordered = byId.size === chunk.length ? chunk.map((_, id) => byId.get(id)) : parsed;
  return ordered.map((entry, index) => {
    if (typeof entry === "string") {
      return { original: chunk[index], zh_tw: entry };
    }
    if (entry && typeof entry === "object") {
      return {
        original: typeof entry.original === "string" ? entry.original : chunk[index],
        zh_tw: typeof entry.zh_tw === "string" ? entry.zh_tw : String(entry.translation ?? ""),
      };
    }
    return { original: chunk[index], zh_tw: String(entry ?? "") };
  });
}

function splitTableRow(line) {
  let row = line.trim();
  if (row.startsWith("|")) row = row.slice(1);
  if (row.endsWith("|")) row = row.slice(0, -1);

  const cells = [];
  let cell = "";
  let escaped = false;
  for (const char of row) {
    if (escaped) {
      cell += char;
      escaped = false;
    } else if (char === "\\") {
      escaped = true;
    } else if (char === "|") {
      cells.push(cell.trim());
      cell = "";
    } else {
      cell += char;
    }
  }
  cells.push(cell.trim());
  return cells;
}

function parseSeparatorCell(cell) {
  const trimmed = cell.trim();
  if (!/^:?-{3,}:?$/.test(trimmed)) return null;
  if (trimmed.startsWith(":") && trimmed.endsWith(":")) return "center";
  if (trimmed.endsWith(":")) return "right";
  if (trimmed.startsWith(":")) return "left";
  return "";
}

function tableAt(lines, index) {
  if (index + 1 >= lines.length || !lines[index].includes("|") || !lines[index + 1].includes("|")) {
    return null;
  }

  const headers = splitTableRow(lines[index]);
  const alignments = splitTableRow(lines[index + 1]).map(parseSeparatorCell);
  if (headers.length < 2 || alignments.length !== headers.length || alignments.some((value) => value === null)) {
    return null;
  }

  const rows = [];
  let cursor = index + 2;
  while (cursor < lines.length && lines[cursor].includes("|") && lines[cursor].trim() !== "") {
    const cells = splitTableRow(lines[cursor]);
    rows.push(headers.map((_, cellIndex) => cells[cellIndex] ?? ""));
    cursor += 1;
  }

  return { headers, alignments, rows, nextIndex: cursor };
}

function renderInlineMarkdown(text) {
  const codeTokens = [];
  let rendered = escapeHtml(text).replace(/`([^`]+)`/g, (_match, code) => {
    const token = `@@CODE${codeTokens.length}@@`;
    codeTokens.push(`<code>${code}</code>`);
    return token;
  });

  rendered = rendered
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_match, label, href) => {
      return `<a href="${escapeHtml(href)}">${label}</a>`;
    })
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/@@CODE(\d+)@@/g, (_match, index) => codeTokens[Number(index)]);

  return rendered;
}

function renderMarkdownTable(table) {
  const alignAttrs = table.alignments.map((alignment) => (alignment ? ` style="text-align:${alignment}"` : ""));
  const headerHtml = table.headers
    .map((cell, index) => `<th${alignAttrs[index]}>${renderInlineMarkdown(cell)}</th>`)
    .join("");
  const bodyHtml = table.rows
    .map((row) => {
      const cells = table.headers
        .map((_, index) => `<td${alignAttrs[index]}>${renderInlineMarkdown(row[index] ?? "")}</td>`)
        .join("");
      return `<tr>${cells}</tr>`;
    })
    .join("");

  return `<div class="table-wrap"><table><thead><tr>${headerHtml}</tr></thead><tbody>${bodyHtml}</tbody></table></div>`;
}

function renderMarkdownBlock(text) {
  const trimmed = text.trim();
  if (!trimmed) return "";

  if (/^---\n[\s\S]*\n---$/.test(trimmed)) {
    return `<pre><code>${escapeHtml(trimmed)}</code></pre>`;
  }

  const lines = trimmed.split("\n");
  const parts = [];
  let index = 0;

  while (index < lines.length) {
    if (!lines[index].trim()) {
      index += 1;
      continue;
    }

    if (lines[index].startsWith("```")) {
      const language = lines[index].slice(3).trim();
      const codeLines = [];
      index += 1;
      while (index < lines.length && !lines[index].startsWith("```")) {
        codeLines.push(lines[index]);
        index += 1;
      }
      if (index < lines.length) index += 1;
      const className = language ? ` class="language-${escapeHtml(language)}"` : "";
      parts.push(`<pre><code${className}>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
      continue;
    }

    const table = tableAt(lines, index);
    if (table) {
      parts.push(renderMarkdownTable(table));
      index = table.nextIndex;
      continue;
    }

    const heading = /^(#{1,6})\s+(.+)$/.exec(lines[index]);
    if (heading) {
      const level = heading[1].length;
      parts.push(`<h${level}>${renderInlineMarkdown(heading[2])}</h${level}>`);
      index += 1;
      continue;
    }

    if (/^\s*[-*+]\s+/.test(lines[index])) {
      const items = [];
      while (index < lines.length && /^\s*[-*+]\s+/.test(lines[index])) {
        items.push(`<li>${renderInlineMarkdown(lines[index].replace(/^\s*[-*+]\s+/, ""))}</li>`);
        index += 1;
      }
      parts.push(`<ul>${items.join("")}</ul>`);
      continue;
    }

    if (/^\s*\d+[.)]\s+/.test(lines[index])) {
      const items = [];
      while (index < lines.length && /^\s*\d+[.)]\s+/.test(lines[index])) {
        items.push(`<li>${renderInlineMarkdown(lines[index].replace(/^\s*\d+[.)]\s+/, ""))}</li>`);
        index += 1;
      }
      parts.push(`<ol>${items.join("")}</ol>`);
      continue;
    }

    const paragraph = [];
    while (
      index < lines.length &&
      lines[index].trim() &&
      !lines[index].startsWith("```") &&
      !tableAt(lines, index) &&
      !/^(#{1,6})\s+/.test(lines[index]) &&
      !/^\s*[-*+]\s+/.test(lines[index]) &&
      !/^\s*\d+[.)]\s+/.test(lines[index])
    ) {
      paragraph.push(lines[index].trim());
      index += 1;
    }
    parts.push(`<p>${renderInlineMarkdown(paragraph.join(" "))}</p>`);
  }

  return parts.join("\n");
}

function htmlPage(title, body) {
  return `<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(title)}</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.7;margin:0;color:#1f2937;background:#f8fafc}main{width:100%;box-sizing:border-box;margin:0;padding:40px 24px 80px;background:#fff;min-height:100vh}nav{margin-bottom:32px;padding-bottom:16px;border-bottom:1px solid #e5e7eb;display:flex;gap:16px;flex-wrap:wrap}a{color:#075985}h1,h2,h3{line-height:1.25;color:#111827}h1{font-size:2rem}.path{word-break:break-all}.source-columns{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:28px;align-items:start;margin-top:24px}.source-column{min-width:0}.column-header{position:sticky;top:0;z-index:2;margin:0 0 14px;padding:10px 0;background:rgba(255,255,255,.96);border-bottom:1px solid #e5e7eb;font-size:.8rem;font-weight:700;color:#4b5563;text-transform:uppercase;letter-spacing:.04em}.sync-block{position:relative;margin:0 0 18px;padding-left:42px}.block-anchor{position:absolute;left:0;top:.45rem;color:#94a3b8;font-size:.72rem;line-height:1;text-decoration:none;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}.block-anchor:hover{color:#075985;text-decoration:underline}.sync-block>*:not(.block-anchor):first-child{margin-top:0}.sync-block>*:last-child{margin-bottom:0}p{margin:0 0 1rem}ul,ol{margin:.4rem 0 1rem;padding-left:1.4rem}pre{background:#0f172a;color:#e5e7eb;padding:16px;border-radius:8px;overflow-x:auto;white-space:pre-wrap}code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;background:#f1f5f9;border-radius:4px;padding:.1em .3em}pre code{background:transparent;border-radius:0;padding:0;color:inherit}.table-wrap{overflow-x:auto;margin:12px 0}table{border-collapse:collapse;width:100%;font-size:.95rem;background:#fff}th,td{border:1px solid #cbd5e1;padding:8px 10px;vertical-align:top}th{background:#f1f5f9;font-weight:700}td code,th code{background:#e2e8f0}@media (max-width:760px){main{padding:28px 16px 64px}.source-columns{display:block}.source-column+.source-column{margin-top:36px}.column-header{top:0}.sync-block{padding-left:38px}}</style>
</head>
<body>
<main>
<nav><a href="../index.html">Docs Home</a><a href="../sources/index.html">Sources</a></nav>
${body}
</main>
</body>
</html>
`;
}

function renderTranslatedSource(item, pairs) {
  const renderColumn = (kind, label, field) => {
    const blocks = pairs
      .map((pair, index) => {
        const blockNumber = String(index + 1).padStart(3, "0");
        const id = `${kind}-b${blockNumber}`;
        return `<section class="sync-block" id="${id}"><a class="block-anchor" href="#${id}" aria-label="${id}">b${blockNumber}</a>${renderMarkdownBlock(pair[field])}</section>`;
      })
      .join("\n");
    return `<article class="source-column"><h2 class="column-header">${label}</h2>${blocks}</article>`;
  };

  const body =
    `<h1 class="path">${escapeHtml(item.file)}</h1>` +
    `<p>被引用於：${item.docs.map((d) => `<code>${escapeHtml(d)}</code>`).join("、")}</p>` +
    `<p><a href="../../${escapeHtml(item.file)}">原始檔案路徑</a></p>` +
    `<section class="source-columns">${renderColumn("orig", "Original", "original")}\n${renderColumn("zh", "中文翻譯", "zh_tw")}</section>`;
  fs.writeFileSync(path.join(outDir, sourceName(item.file)), htmlPage(item.file, body));
}

let selected = manifest;
if (only) selected = selected.filter((item) => item.file === only);
if (limit > 0) selected = selected.slice(0, limit);

for (const item of selected) {
  console.log(`${cacheOnly ? "Rendering" : "Translating"} ${item.file}`);
  const text = fs.readFileSync(path.join(root, item.file), "utf8");
  const blocks = splitBlocks(text);
  const chunks = chunkBlocks(blocks);
  const pairs = [];
  for (let i = 0; i < chunks.length; i++) {
    console.log(`  chunk ${i + 1}/${chunks.length}`);
    pairs.push(...translateChunk(item.file, chunks[i], i));
  }
  renderTranslatedSource(item, pairs);
  console.log(`  wrote ${path.join("docs-html", "sources", sourceName(item.file))}`);
}
