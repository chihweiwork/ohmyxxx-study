# ohmyxxx-study

This repository contains study notes, graphify outputs, and generated HTML pages for comparing four agentic coding enhancer projects:

- `oh-my-openagent`
- `oh-my-claudecode`
- `oh-my-codex`
- `oh-my-antigravity`

The four source projects are tracked as Git submodules. The study material is in `docs/`, the generated browser-readable pages are in `docs-html/`, and graphify analysis output is in `graphify-out/`.

## Clone

Clone this repo with submodules:

```bash
git clone --recurse-submodules git@github.com:chihweiwork/ohmyxxx-study.git
cd ohmyxxx-study
```

If you already cloned without submodules, initialize them:

```bash
git submodule update --init --recursive
```

## Read The Docs In Browser

The easiest way to read the generated HTML is to serve `docs-html/` with Python:

```bash
cd docs-html
python3 -m http.server 8001 --bind 0.0.0.0
```

Then open:

```text
http://localhost:8001/
```

If you are opening it from another machine, replace `localhost` with the server IP:

```text
http://<server-ip>:8001/
```

The source Markdown translation index is here:

```text
http://<server-ip>:8001/sources/index.html
```

## Important Pages

- `docs-html/index.html`: generated HTML home page
- `docs-html/sources/index.html`: source Markdown index with English/Chinese side-by-side translations
- `docs/README.md`: Markdown study guide entry point
- `graphify-out/index.html`: graphify visual output

## Regenerate Source Translation HTML

The source translation pages are generated from cached translations:

```bash
node scripts/translate_sources_with_codex.mjs
```

This reuses `docs-html/.translation-cache/` when available. It should not call the model again unless cache entries are missing.

## Notes

- The generated source pages use a side-by-side layout on wide screens and automatically switch back to stacked layout on narrow screens.
- The graphify relationships are study aids and should be treated as analysis signals, not as upstream project design claims.
