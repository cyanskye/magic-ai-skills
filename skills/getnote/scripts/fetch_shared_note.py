#!/usr/bin/env python3
"""Fetch a public Get笔记 shared note without opening a browser."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


SHARE_RE = re.compile(r"/share_note/([A-Za-z0-9_-]+)")


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 magic-kb-compiler",
            "Accept": "application/json,text/plain,*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read()
    return json.loads(body.decode("utf-8"))


def resolve_url(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 magic-kb-compiler"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.geturl()


def extract_share_id(resolved_url: str) -> str:
    match = SHARE_RE.search(resolved_url)
    if not match:
        raise ValueError(f"Could not find share id in resolved URL: {resolved_url}")
    return match.group(1)


def normalize_payload(source_url: str, resolved_url: str, share_id: str) -> dict[str, Any]:
    base = f"https://get-notes.luojilab.com/voicenotes/web/share/notes/{share_id}"
    polished = fetch_json(f"{base}?acode=")
    original = fetch_json(f"{base}/original")
    return {
        "source_url": source_url,
        "resolved_url": resolved_url,
        "share_id": share_id,
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "polished": polished,
        "original": original,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a public Get笔记 shared note.")
    parser.add_argument("url", help="Get笔记 share URL, for example https://d.biji.com/...")
    parser.add_argument("--output", "-o", help="Write normalized JSON to this path.")
    args = parser.parse_args()

    try:
        resolved_url = resolve_url(args.url)
        share_id = extract_share_id(resolved_url)
        payload = normalize_payload(args.url, resolved_url, share_id)
    except (urllib.error.URLError, json.JSONDecodeError, ValueError) as exc:
        print(f"fetch_failed: {exc}", file=sys.stderr)
        return 1

    if args.output:
        output = Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    polished_note = payload.get("polished", {}).get("c", {}).get("note", {})
    title = polished_note.get("title") or polished_note.get("note_title") or ""
    duration = polished_note.get("duration") or polished_note.get("audio_duration") or ""
    print(json.dumps({
        "ok": True,
        "share_id": payload["share_id"],
        "title": title,
        "duration": duration,
        "output": args.output,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
