# Mermaid Rendering Helper

This folder documents the local Mermaid rendering helper for Mermaid source
drafts.

The installed tool binaries and downloaded runtime libraries live under
`.tools/`, which is intentionally ignored. Do not commit `.tools/`; it contains
machine-specific Node, `node_modules`, and Chromium runtime libraries.

Current local tool layout expected by `scripts/render-mermaid-figures.sh`:

- `.tools/node-v22.16.0-linux-x64/bin/node`
- `.tools/mermaid-cli/node_modules/.bin/mmdc`
- `.tools/chrome-libs/usr/lib/x86_64-linux-gnu`
- `.tools/mermaid-puppeteer-config.json`

Render all Mermaid drafts in the current directory to `/tmp/mermaid-render-check`:

```bash
scripts/render-mermaid-figures.sh
```

Render one file:

```bash
scripts/render-mermaid-figures.sh \
  --file path/to/example.mmd
```

The helper renders SVGs for local review only. Source `.mmd` files remain the
reviewable artifacts, and generated PNG, JPG, or SVG files are not committed by
default.
