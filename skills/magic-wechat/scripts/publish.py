#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
magic-wechat 发布器（神奇桑桑自用）
直接调微信 draft/add，把可自动化的 5 项一次带上：
  封面 / 留言开关 / 只关注可评 / 原文链接 / 指定微信号预览
只发草稿，绝不直接群发。无 API 字段的设置（原创/快捷转载/赞赏/自动精选/合集/创作来源）
留在编辑器里手动。

用法:
  python3 publish.py <article.html> --cover cover.png --title "标题" \
      --author "神奇桑桑" --digest "摘要" \
      --source-url "https://..." --preview-to MagicSang666
"""
import sys, os, json, argparse, subprocess, urllib.request, urllib.parse

API = "https://api.weixin.qq.com/cgi-bin"

def load_env():
    for p in [os.path.join(os.getcwd(), ".baoyu-skills/.env"),
              os.path.expanduser("~/.baoyu-skills/.env")]:
        if os.path.isfile(p):
            env = {}
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
            if env.get("WECHAT_APP_ID"):
                return env
    sys.exit("未找到 WECHAT_APP_ID（查 .baoyu-skills/.env）")

def get_json(url):
    return json.loads(urllib.request.urlopen(url, timeout=30).read().decode())

def post_json(url, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())

def token(env):
    u = f"{API}/token?grant_type=client_credential&appid={env['WECHAT_APP_ID']}&secret={env['WECHAT_APP_SECRET']}"
    r = get_json(u)
    if "access_token" not in r:
        sys.exit(f"取 token 失败: {r}")
    return r["access_token"]

def upload_thumb(tok, cover):
    """永久素材上传作封面 thumb（用 curl 处理 multipart 最稳）"""
    url = f"{API}/material/add_material?access_token={tok}&type=image"
    out = subprocess.run(["curl", "-s", "-F", f"media=@{cover}", url],
                         capture_output=True, text=True).stdout
    r = json.loads(out)
    if "media_id" not in r:
        sys.exit(f"上传封面失败: {r}")
    return r["media_id"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--cover", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--author", default="神奇桑桑")
    ap.add_argument("--digest", default="")
    ap.add_argument("--source-url", default="", help="阅读原文链接 content_source_url")
    ap.add_argument("--preview-to", default="", help="指定微信号预览，如 MagicSang666")
    ap.add_argument("--open-comment", type=int, default=1)      # 留言开关
    ap.add_argument("--only-fans", type=int, default=1)         # 只允许关注的人评论
    a = ap.parse_args()

    env = load_env()
    tok = token(env)
    thumb = upload_thumb(tok, a.cover)
    content = open(a.html, encoding="utf-8").read()

    article = {
        "title": a.title,
        "author": a.author,
        "digest": a.digest,
        "content": content,
        "thumb_media_id": thumb,
        "need_open_comment": a.open_comment,
        "only_fans_can_comment": a.only_fans,
    }
    if a.source_url:
        article["content_source_url"] = a.source_url

    r = post_json(f"{API}/draft/add?access_token={tok}", {"articles": [article]})
    if "media_id" not in r:
        sys.exit(f"发草稿失败: {r}")
    media_id = r["media_id"]
    print(f"✓ 草稿已存 media_id: {media_id}")
    print(f"  封面: thumb {thumb}")
    print(f"  留言: {'开' if a.open_comment else '关'} / {'只关注可评' if a.only_fans else '所有人可评'}")
    print(f"  原文链接: {a.source_url or '(无)'}")

    if a.preview_to:
        wxname = a.preview_to.lstrip("@")
        pr = post_json(f"{API}/message/mass/preview?access_token={tok}",
                       {"towxname": wxname, "mpnews": {"media_id": media_id}, "msgtype": "mpnews"})
        ok = pr.get("errcode") == 0
        print(f"  预览推送 -> {wxname}: {'✓ 已发，去手机看' if ok else '✗ '+str(pr)}")

if __name__ == "__main__":
    main()
