---
name: magic-kb-compiler
description: Use when the user wants to compile voice notes, Get notes, clippings, AI chat records, loose thoughts, AI practice notes, workflows, or tutorial material into reusable Magic AI knowledge assets for Obsidian / Magic AI 知识库 or ima.
---

# Magic KB Compiler

## Overview

Compile raw inputs into reusable Magic AI knowledge assets. The goal is not neutral summarization; it is to turn scattered material into reusable knowledge assets, output directions, recommended questions, methods, and future AI context.

The primary quick-reading unit is the atomic card in `cards/`, not a whole article, whole Get note, or whole wiki page. `brief-cards/` is optional theme-level overview material; it is not the default speed-reading layer.

## High-Value IP Principle

This knowledge base serves high-value IP, professional creators, small-company operators, consultants, and AI practitioners. Do not optimize compiled outputs for emotional traffic.

When generating cards, topic pools, recommended questions, context packs, prompts, or platform-specific output directions:

- Prefer judgment over emotion.
- Prefer professional trust over clickbait.
- Prefer frameworks, tradeoffs, cases, methods, and evidence over empty resonance.
- Do not manufacture anxiety, sensational titles, or爽文-style conclusions.
- Do not lower the professional density just to gain generic engagement.
- If a source contains emotion, extract the underlying judgment, scene, problem, method, or boundary instead of amplifying the emotion itself.

The target is high-quality trust and useful judgment, not low-value follower growth.

## Target Platforms

This skill compiles raw material into reusable knowledge assets. Do not treat one storage platform as the whole skill.

Supported target modes:

- **Obsidian / Magic AI 知识库 mode**: current most complete local-first mode. Use this when the user wants raw files, schema-driven cards, wiki pages, views, and compile logs.
- **ima mode**: supported as an export/import target. Use this when the user wants material prepared for ima. Generate Markdown documents, topic entries, source summaries, and import packages instead of assuming Obsidian's folder structure exists.

If the user specifies `target_platform`, accept only `obsidian` or `ima`. If the user does not specify a target, default to Obsidian when a usable `magic-ai-kb` exists; otherwise generate an ima-ready Markdown import package and state that no platform was written.

For detailed target behavior, read `references/target-platforms.md` when choosing or implementing a target adapter.

### Obsidian / Magic AI 知识库 Mode

Default vault root for the user's local Obsidian setup:

`/Users/magicsang666/Library/Mobile Documents/iCloud~md~obsidian/Documents/MacbookAir`

Default knowledge base:

`/Users/magicsang666/Library/Mobile Documents/iCloud~md~obsidian/Documents/MacbookAir/magic-ai-kb`

If the user provides another vault or `magic-ai-kb` path, use that path for the current task.

### ima Mode

When the target is ima:

1. Do not require the Obsidian `schema/`, `cards/`, `wiki/`, `views/`, or `logs/` folders to exist.
2. Ask or infer the platform import shape:
   - Markdown document
   - Folder of Markdown files
   - PDF/docx export
   - Web link/import package
   - API-backed upload
3. Preserve provenance in the exported content:
   - source title or note id
   - original source type
   - capture/compile date
   - short summary
   - key topics/tags
4. Prefer a staged output package first. Do not claim the platform has been updated unless an actual upload/import action was performed and verified.

## Required Reading

For Obsidian / Magic AI 知识库 mode, before compiling anything, read these files from `magic-ai-kb`:

1. `00-index.md`
2. `schema/mvp-definition.md`
3. `schema/compile-rules.md`
4. `schema/card-types.md`
5. `schema/recompile-rules.md`

If any file is missing, recreate the missing file only after telling the user what is missing.

For ima mode, read `references/target-platforms.md`. Produce a clear export package and document the import assumptions unless an actual ima upload/import path is available and verified.

## Workflow

### One-Line Get Note Mode

When the user gives a Get笔记 share URL such as `https://d.biji.com/...` and asks to compile it, do not ask the user to export anything manually.

1. Use the external Get笔记 official Skill / OpenAPI ability when available. This repository does not bundle the Get笔记 Skill.
2. Fetch shared notes with the nearest available compatible `getnote/scripts/fetch_shared_note.py` if it exists locally.
   Prefer these locations in order:
   - The current agent's local skill directory.
   - `/Users/magicsang666/.agents/skills/getnote/scripts/fetch_shared_note.py`
   - `/Users/magicsang666/.codex/skills/getnote/scripts/fetch_shared_note.py`
   - `/Users/magicsang666/.claude/skills/getnote/scripts/fetch_shared_note.py`
3. Only use a browser as a last-resort fallback if the official/API/script path cannot fetch the note.
4. Then continue the normal compile workflow below.

1. Identify the input source:
   - User-pasted text
   - Get note export
   - Obsidian clipping
   - AI conversation record
   - Local file path
   - Folder of pending raw notes

2. Preserve the raw input:
   - Obsidian mode: save new raw material under the appropriate `raw/` subfolder.
   - ima mode: include the source text or a source summary in the import package unless the user asks to omit raw material.
   - Do not overwrite or edit raw source files.
   - If the input is already in the vault, reference it instead of duplicating unless the user asks to copy it.

3. Compile into knowledge assets:
   - Create or update atomic cards in `cards/`.
   - Split material into granular viewpoint, method, question, topic, and case cards.
   - Do not compress a whole article, whole Get note, or whole wiki page into one speed card.
   - Keep topic/output cards aligned with the High-Value IP Principle: less emotional traffic, more judgment density.
   - Only create `brief-cards/` when a theme-level overview is genuinely useful.
   - Prefer card types from `schema/card-types.md`.
   - Prioritize topic/output cards, recommended questions, methods, and tutorial material.
   - Treat idea cards as intermediate assets, not the main output.

4. Weave backward:
   - Check existing `wiki/`, `views/`, and `00-index.md`.
   - Update related old pages when new material changes or enriches them.
   - Do not leave strong new inputs as isolated notes.

5. Update views:
   - Add output directions to `views/topic-pool.md`.
   - Add recommended questions to `views/question-pool.md`.
   - Add deferred items to `views/backlog.md`.

6. Log the compile:
   - Add one log file in `logs/` named `YYYY-MM-DD-HHMM-compile.md`.
   - Include source, generated/updated files, key decisions, and next recommended action.

## File Naming

Use readable Chinese titles for user-facing Markdown files when content is Chinese. Keep system folders and skill names in lowercase English.

For generated brief cards, prefer:

`brief-cards/YYYY-MM-DD-短标题.md`

Brief cards are optional and theme-level. The reader's main speed cards are generated from structured files in `cards/`.

For generated cards, prefer:

`cards/YYYY-MM-DD-短标题.md`

For logs, prefer:

`logs/YYYY-MM-DD-HHMM-compile.md`

## Output Style

After compiling, report:

- Raw source handling
- Atomic cards created or updated
- Whether optional theme-level brief cards were created or skipped
- Wiki/views updated
- Recommended next action

Keep the reply concise and include clickable local file links.

## Runtime Portability

This skill should stay portable across Codex, Claude, ima, WorkBuddy, OpenClaw, and Hermes:

- Keep the core workflow in `SKILL.md` and target details in `references/`.
- Do not require a platform-specific API unless the current task explicitly uses it.
- If the runtime cannot write files or run scripts, produce a Markdown package and clear manual import steps.
- Do not claim a target platform was updated unless the write/import action was actually performed and verified.

## Non-Goals

Do not implement full automation, visual apps, provider-specific plugin migrations, or large migrations unless the user explicitly asks. Put these into `views/backlog.md` when they arise.
