---
name: magic-recorder
description: Turn Chinese or bilingual spoken notes, rough transcripts, Get笔记 records, voice-dump text, and unfinished personal reflections into structured Markdown thinking records. Use when the user says they want to record something, asks to整理/记录/沉淀/保存一段口述, says "按昨天那种方式整理", provides a raw spoken transcript, gives a Get笔记 share link, asks to read the latest/specified Get笔记, or wants a reusable personal note workflow that preserves their original viewpoint while improving readability.
---

# Magic Recorder

## Overview

Transform rough spoken thinking into a readable personal record without changing the user's intellectual ownership. Keep the user's claims, tone, and reasoning intact; only repair the shape.

## Core Rules

- Preserve the user's original viewpoints, judgments, uncertainty, and speaking style.
- Do not add new factual claims, examples, conclusions, or outside context unless the user explicitly asks.
- Smooth obvious speech artifacts: repeated phrases, broken sentences, filler transitions, and unfinished clauses.
- Keep the result as a personal thinking record, not a media article, marketing post, report, or ghostwritten essay.
- Prefer clear Chinese prose when the source is Chinese. Keep product names, English terms, and acronyms in their common form.
- If a sentence is unfinished but the intent is clear, complete it conservatively. If intent is unclear, leave it natural or mark it gently as an unresolved thought.
- Do not browse the web just to verify claims unless the user asks for verification, current facts, quotes, or links.

## Input Routing

Before asking the user for more material, decide which input mode applies:

- **Pasted long text / transcript**: If the user gives a substantial block of text, treat it as the source material and start the recorder workflow directly. Do not ask whether it came from Get笔记.
- **Get笔记 share link**: If the user gives a link such as `https://d.biji.com/...`, load the `getnote` skill and fetch it with `/Users/magicsang666/.codex/skills/getnote/scripts/fetch_shared_note.py`.
- **Implicit Get笔记 request**: If the user asks to record/整理/沉淀/编译 but provides no text, file, or link, assume the intended source is the newest Get笔记 record. Load the `getnote` skill and run `/Users/magicsang666/.codex/skills/getnote/scripts/fetch_note.py --latest`.
- **Direct Get笔记 request**: If the user says “读取 Get 笔记”, “读最新 Get 笔记”, “最新的 Get 笔记记录”, or similar without a link, load the `getnote` skill and run `/Users/magicsang666/.codex/skills/getnote/scripts/fetch_note.py --latest`.
- **Specified Get笔记 request**: If the user names a note title, note id, date, or keyword, load the `getnote` skill and run `/Users/magicsang666/.codex/skills/getnote/scripts/fetch_note.py --query "..."` or `--id ...`. If multiple notes are plausible and the wrong choice would be risky, ask one concise clarification.
- **File path**: If the user references a local file, read that file and use it as the source.
- **No usable source**: Only ask for the transcript or source when there is no pasted text, no file, no Get笔记 link, and no clear request to fetch Get笔记.

For private Get笔记 API access, load credentials from `/Users/magicsang666/.getnote/.env` when environment variables are absent. Do not print credentials.

For Get笔记 detail records:

- Audio notes: use `audio.original` as the primary transcript when available; use `content` only as a readability aid. Do not let the polished content add claims absent from the original.
- Plain text notes: use `content` as the primary material.
- Link notes: use `web_page.content` when available; otherwise use `content` and `web_page.excerpt`.
- If only the list endpoint has enough content and detail is unavailable, proceed with the list `content` but mention that detail fetch failed.

## Workflow

1. Identify the user's raw material:
   - If the user pasted a transcript, use it directly.
   - If the user references a file, read that file.
   - If the user provides a Get笔记 shared link such as `https://d.biji.com/...`, also load the `getnote` skill and fetch it with `/Users/magicsang666/.codex/skills/getnote/scripts/fetch_shared_note.py`.
   - If the user asks to read Get笔记 without a link, use the Input Routing rules above instead of asking the user to paste or export the note.
   - For fetched Get笔记 audio notes, use `audio.original` or `original.c.content` as the primary transcript and use polished/list content only as a readability aid; do not let the polished version add claims absent from the original.
   - If the user asks to "record this" but provides no content, ask for the transcript or source.

2. Extract the natural structure:
   - Opening context: what prompted this thought.
   - Core question or tension.
   - Main judgments.
   - Supporting analysis.
   - Opportunity, conclusion, or open question.

3. Write a Markdown record:
   - Add YAML frontmatter with `title`, `date`, and `summary`.
   - Use one H1 matching the title.
   - Add short `##` sections that follow the actual logic of the thought.
   - Convert buried enumerations into bullets only when it improves scanning.
   - Keep paragraphs short and readable.

4. Save the file:
   - Default to the workspace `docs/` directory when available.
   - Use the current date in the user's timezone.
   - Name the file with a concise Chinese title plus date, for example `docs/微信开放小程序AI能力思考-2026-06-08.md`.
   - If a likely duplicate filename exists, add a short suffix rather than overwriting.

5. Verify:
   - Read the saved file back after writing.
   - Confirm the file has valid frontmatter, a title, sections, and the user's core points.

6. Reply to the user:
   - Give the saved file path as a clickable local file link.
   - Briefly state what structure was used.
   - Mention any uncertainty or intentionally unresolved sentence.

## House Style

Use this general shape when it fits the material:

```markdown
---
title: 简洁、有判断力的中文标题
date: YYYY-MM-DD
summary: 一句话概括这段思考记录的主题和核心判断。
---

# 简洁、有判断力的中文标题

今天想记录一下……

## 背景

……

## 核心判断

……

## 具体分析

……

## 机会在哪里

……
```

Do not force this exact outline. Choose headings from the user's content.

## Trigger Examples

- "帮我记录一件事情。"
- "把下面这段口述整理成昨天那种风格。"
- "我先随便说，你帮我沉淀成一篇 Markdown。"
- "这是一段语音转文字，帮我整理成个人思考记录。"
- "以后我想复用这个口述整理工作流。"
