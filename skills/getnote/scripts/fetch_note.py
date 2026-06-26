#!/usr/bin/env python3
"""Fetch private Get笔记 notes through the OpenAPI.

Supports the common recorder/compiler routes:
- latest note
- note by id
- best title/content keyword match from the first list page
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_URL = "https://openapi.biji.com"
ENV_PATH = Path("/Users/magicsang666/.getnote/.env")
CACHE_DIR = Path("/tmp/getnote-fetch-cache")


def load_env_file(path: Path = ENV_PATH) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def credentials() -> tuple[str, str]:
    load_env_file()
    api_key = os.environ.get("GETNOTE_API_KEY", "")
    client_id = os.environ.get("GETNOTE_CLIENT_ID", "")
    if not api_key or not client_id:
        raise RuntimeError("missing GETNOTE_API_KEY or GETNOTE_CLIENT_ID")
    return api_key, client_id


def request_json(
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    retries: int = 2,
    retry_delay: float = 2.0,
) -> Any:
    api_key, client_id = credentials()
    url = f"{BASE_URL}{path}"
    data = None
    headers = {
        "Authorization": api_key,
        "X-Client-ID": client_id,
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, method=method, headers=headers)
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = max(float(retry_after), retry_delay)
                except ValueError:
                    delay = retry_delay * (attempt + 1)
            else:
                delay = retry_delay * (attempt + 1)
            print(
                f"rate_limited: HTTP 429, retrying in {delay:g}s ({attempt + 1}/{retries})",
                file=sys.stderr,
            )
            time.sleep(delay)
    raise RuntimeError("request retry loop exhausted")


def unwrap_notes(payload: Any) -> list[dict[str, Any]]:
    candidates = [
        payload.get("notes") if isinstance(payload, dict) else None,
        payload.get("data", {}).get("notes") if isinstance(payload, dict) else None,
        payload.get("data", {}).get("note_list") if isinstance(payload, dict) else None,
        payload.get("c", {}).get("notes") if isinstance(payload, dict) else None,
    ]
    for candidate in candidates:
        if isinstance(candidate, list):
            return candidate
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("note"), list):
            return data["note"]
    return []


def unwrap_note(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    for path in (
        ("note",),
        ("data", "note"),
        ("data",),
        ("c", "note"),
    ):
        value: Any = payload
        for key in path:
            value = value.get(key) if isinstance(value, dict) else None
        if isinstance(value, dict) and (value.get("id") or value.get("note_id")):
            return value
    return {}


def list_notes(retries: int = 2, retry_delay: float = 2.0) -> list[dict[str, Any]]:
    payload = request_json(
        "GET",
        "/open/api/v1/resource/note/list?since_id=0",
        retries=retries,
        retry_delay=retry_delay,
    )
    return unwrap_notes(payload)


def parse_time(note: dict[str, Any]) -> str:
    return str(note.get("created_at") or note.get("updated_at") or "")


def newest_note(notes: list[dict[str, Any]]) -> dict[str, Any]:
    if not notes:
        raise RuntimeError("no Get笔记 notes returned")
    return sorted(notes, key=parse_time, reverse=True)[0]


def find_note(notes: list[dict[str, Any]], query: str) -> dict[str, Any]:
    normalized = query.lower().strip()
    scored: list[tuple[int, str, dict[str, Any]]] = []
    for note in notes:
        title = str(note.get("title") or "")
        content = str(note.get("content") or "")
        note_id = str(note.get("note_id") or note.get("id") or "")
        haystack = f"{title}\n{content}\n{note_id}".lower()
        if normalized == note_id:
            score = 100
        elif normalized and normalized in title.lower():
            score = 80
        elif normalized and normalized in haystack:
            score = 50
        else:
            score = 0
        if score:
            scored.append((score, parse_time(note), note))
    if not scored:
        raise RuntimeError(f"no Get笔记 note matched query: {query}")
    return sorted(scored, key=lambda item: (item[0], item[1]), reverse=True)[0][2]


def detail(note_id: str, retries: int = 2, retry_delay: float = 2.0) -> dict[str, Any]:
    encoded = urllib.parse.quote(str(note_id), safe="")
    payload = request_json(
        "GET",
        f"/open/api/v1/resource/note/detail?id={encoded}",
        retries=retries,
        retry_delay=retry_delay,
    )
    note = unwrap_note(payload)
    if not note:
        raise RuntimeError(f"detail returned no note for id: {note_id}")
    return note


def primary_text(note: dict[str, Any]) -> str:
    audio = note.get("audio") if isinstance(note.get("audio"), dict) else {}
    web_page = note.get("web_page") if isinstance(note.get("web_page"), dict) else {}
    for value in (
        audio.get("original"),
        web_page.get("content"),
        note.get("content"),
        web_page.get("excerpt"),
    ):
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def normalize(note: dict[str, Any], mode: str, query: str | None = None) -> dict[str, Any]:
    return {
        "ok": True,
        "mode": mode,
        "query": query,
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "note": note,
        "primary_text": primary_text(note),
    }


def cache_path(key: str) -> Path:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
    return CACHE_DIR / f"{digest}.json"


def load_cache(key: str, ttl: int) -> dict[str, Any] | None:
    if ttl <= 0:
        return None
    path = cache_path(key)
    if not path.exists():
        return None
    age = time.time() - path.stat().st_mtime
    if age > ttl:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def save_cache(key: str, payload: dict[str, Any]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path(key).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a private Get笔记 note.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--latest", action="store_true", help="Fetch newest note from list.")
    group.add_argument("--id", help="Fetch note detail by note id.")
    group.add_argument("--query", help="Find best title/content/id match from the first list page.")
    parser.add_argument("--output", "-o", help="Write normalized JSON to this path.")
    parser.add_argument("--retries", type=int, default=2, help="Retry count for HTTP 429.")
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=2.0,
        help="Base delay in seconds for HTTP 429 retries.",
    )
    parser.add_argument(
        "--cache-ttl",
        type=int,
        default=300,
        help="Reuse a recent fetched note for this many seconds. Set 0 to disable.",
    )
    args = parser.parse_args()

    cache_key = (
        f"id:{args.id}"
        if args.id
        else f"query:{args.query}"
        if args.query
        else "latest"
    )
    cached = load_cache(cache_key, args.cache_ttl)
    if cached:
        cached["cache_hit"] = True
        payload = cached
        note = payload["note"]
        print(
            json.dumps(
                {
                    "ok": True,
                    "cache_hit": True,
                    "mode": payload["mode"],
                    "id": note.get("note_id") or note.get("id"),
                    "title": note.get("title") or "",
                    "note_type": note.get("note_type") or "",
                    "created_at": note.get("created_at") or "",
                    "primary_text_chars": len(payload.get("primary_text") or ""),
                    "output": args.output,
                },
                ensure_ascii=False,
            )
        )
        if args.output:
            output = Path(args.output).expanduser()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    try:
        if args.id:
            note = detail(args.id, retries=args.retries, retry_delay=args.retry_delay)
            payload = normalize(note, "id", args.id)
        else:
            notes = list_notes(retries=args.retries, retry_delay=args.retry_delay)
            selected = newest_note(notes) if args.latest else find_note(notes, args.query or "")
            note_id = str(selected.get("note_id") or selected.get("id") or "")
            note = (
                detail(note_id, retries=args.retries, retry_delay=args.retry_delay)
                if note_id
                else selected
            )
            payload = normalize(note, "latest" if args.latest else "query", args.query)
    except (RuntimeError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"fetch_failed: {exc}", file=sys.stderr)
        return 1

    save_cache(cache_key, payload)

    if args.output:
        output = Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    note = payload["note"]
    print(
        json.dumps(
            {
                "ok": True,
                "mode": payload["mode"],
                "id": note.get("note_id") or note.get("id"),
                "title": note.get("title") or "",
                "note_type": note.get("note_type") or "",
                "created_at": note.get("created_at") or "",
                "primary_text_chars": len(payload.get("primary_text") or ""),
                "output": args.output,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
