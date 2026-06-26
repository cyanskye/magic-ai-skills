---
name: getnote
description: Use when the user wants to read, search, save, or manage Get笔记 notes through the Get笔记 OpenAPI, or when a Get note should be imported into Magic AI 知识库.
metadata:
  requires_env:
    - GETNOTE_API_KEY
    - GETNOTE_CLIENT_ID
  optional_env:
    - GETNOTE_OWNER_ID
  credential_file: /Users/magicsang666/.getnote/.env
  base_url: https://openapi.biji.com
---

# Getnote

## Use This Skill When

- The user asks to save something to Get笔记.
- The user asks to search, list, read, or delete Get笔记 notes.
- The user provides a Get笔记 link and wants it imported or compiled.
- The user wants Get笔记 content to become Magic AI 知识库 material.

## Credentials

Use environment variables first:

- `GETNOTE_API_KEY`
- `GETNOTE_CLIENT_ID`
- `GETNOTE_OWNER_ID` (optional)

If they are not already set, load them from:

`/Users/magicsang666/.getnote/.env`

Do not print credentials, paste credentials into responses, or expose private note content unless it is needed for the user's active request.

## API Basics

Base URL:

`https://openapi.biji.com`

Required headers:

- `Authorization: $GETNOTE_API_KEY`
- `X-Client-ID: $GETNOTE_CLIENT_ID`

For detailed endpoint behavior, read `references/openclaw-api.md` only when needed.

## Common Actions

- Fetch a public shared Get note without opening a browser:
  `python scripts/fetch_shared_note.py "https://d.biji.com/..." --output /tmp/getnote.json`
- Fetch the latest private note through OpenAPI:
  `python scripts/fetch_note.py --latest --output /tmp/getnote-latest.json`
- Fetch a private note by id or keyword:
  `python scripts/fetch_note.py --id NOTE_ID --output /tmp/getnote.json`
  `python scripts/fetch_note.py --query "关键词或标题" --output /tmp/getnote.json`
- List notes: `GET /open/api/v1/resource/note/list?since_id=0`
- Read detail: `GET /open/api/v1/resource/note/detail?id={note_id}`
- Save plain text: `POST /open/api/v1/resource/note/save`
- Delete note: `POST /open/api/v1/resource/note/delete`
- List knowledge bases: `GET /open/api/v1/resource/knowledge/list`

For image upload, prefer the bundled scripts in `scripts/`.

## Magic AI 知识库 Flow

When importing Get笔记 material into Magic AI 知识库:

1. Fetch the note or use the provided shared note content. If the user asks to record/compile a note but gives no text or link, use `scripts/fetch_note.py --latest` by default.
2. Preserve the raw note under `magic-ai-kb/raw/`.
3. Use `magic-kb-compiler` rules to create cards, wiki updates, views, and logs.
4. Keep Get笔记 as an input source, not the long-term knowledge structure.

## Safety

- Treat all Get笔记 data as private by default.
- Summarize note lists before showing full content.
- If an API call fails with `not_member` or error code `10201`, explain that Get笔记 membership/API access is required.
