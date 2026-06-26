# Target Platforms

Use this reference when `magic-kb-compiler` needs to choose or implement a knowledge-base target.

## Selection

Accept only two target platforms for now:

- `obsidian`
- `ima`

If the user specifies a target, use it. If not:

1. Use `obsidian` when a usable `magic-ai-kb` exists.
2. Use `ima` export-package mode when no local `magic-ai-kb` is available.
3. Ask one concise question only when the target choice changes what files will be written and cannot be inferred safely.

## Obsidian Adapter

Use Obsidian mode for the local Magic AI knowledge base.

Expected structure:

```text
magic-ai-kb/
  00-index.md
  schema/
  raw/
  cards/
  wiki/
  views/
  logs/
```

Behavior:

- Preserve raw source files under `raw/`.
- Read schema files before creating or changing cards.
- Create or update atomic cards under `cards/`.
- Update related `wiki/`, `views/`, and `00-index.md`.
- Write a compile log under `logs/`.
- Report clickable local file paths after writing.

Use this mode when the user wants maximum provenance, local-first storage, and long-term cross-linking.

## ima Adapter

Use ima mode for a platform-friendly import package.

Default output shape:

```text
ima-import/YYYY-MM-DD-短标题/
  README.md
  source.md
  topics/
    001-主题.md
    002-主题.md
  summaries/
    source-summary.md
```

Behavior:

- Do not require Obsidian folders or schema files.
- Preserve provenance in every generated file: source title/id, source type, compile date, and tags.
- Prefer Markdown because it is easiest to inspect and import.
- Split into topic entries when the source has multiple durable ideas.
- Keep raw source in `source.md` unless the user asks not to preserve it.
- Include a concise `README.md` with suggested ima import steps.

Do not claim ima has been updated unless an actual ima import/upload action was performed and verified.
