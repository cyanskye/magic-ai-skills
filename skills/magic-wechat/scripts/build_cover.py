#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
magic-wechat 纯文字封面生成器（本地绘制，零 API，可商用字体）
字体：阿里巴巴普惠体（免费商用）。2.35:1 主图，关键文字落在中心 1:1 安全区，
兼容推送页横版 + 朋友圈 1:1 裁切。同时导出 1:1 预览。

用法:
  python3 build_cover.py --label "写给爱折腾的 AI 同好" \
     --line1 "你做的 AI 小工具" --line2 "一半人" --hl "「打不开」" \
     --sub "GitHub → Gitee 自动镜像 · 零维护" --out images/cover.png
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = os.path.expanduser("~/Library/Fonts")
F_HEAVY = FONT_DIR + "/Alibaba-PuHuiTi-Heavy.ttf"
F_BOLD  = FONT_DIR + "/Alibaba-PuHuiTi-Bold.ttf"
F_REG   = FONT_DIR + "/Alibaba-PuHuiTi-Regular.ttf"

W, H, SAFE = 1410, 600, 600
BG = (250, 247, 242); BLACK = (26, 28, 31); GRAY = (140, 140, 146); ORANGE = (255, 104, 39)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="")
    ap.add_argument("--line1", required=True)
    ap.add_argument("--line2", default="", help="第二行普通色部分")
    ap.add_argument("--hl", default="", help="第二行橙色高亮部分")
    ap.add_argument("--sub", default="")
    ap.add_argument("--out", default="images/cover.png")
    a = ap.parse_args()

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cx = W // 2
    def f(p, s): return ImageFont.truetype(p, s)
    def w(s, fnt): b = d.textbbox((0, 0), s, font=fnt); return b[2] - b[0]
    def center(s, fnt, y, c): d.text((cx - w(s, fnt) // 2, y), s, font=fnt, fill=c)
    def center_mixed(parts, fnt, y):
        tot = sum(w(t, fnt) for t, _ in parts); x = cx - tot // 2
        for t, c in parts:
            d.text((x, y), t, font=fnt, fill=c); x += w(t, fnt)

    if a.label:
        center(a.label, f(F_BOLD, 28), 150, ORANGE)
    f_title = f(F_HEAVY, 72)
    center(a.line1, f_title, 215, BLACK)
    if a.line2 or a.hl:
        center_mixed([(a.line2, BLACK), (a.hl, ORANGE)], f_title, 310)
    d.line([(cx - 40, 420), (cx + 40, 420)], fill=ORANGE, width=4)
    if a.sub:
        center(a.sub, f(F_REG, 28), 445, GRAY)

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    img.save(a.out)
    # 1:1 中心裁切预览
    crop = img.crop((cx - H // 2, 0, cx + H // 2, H))
    base, ext = os.path.splitext(a.out)
    crop.save(base + "-1x1" + ext)
    print(f"OK 2.35:1 -> {a.out}  |  1:1 预览 -> {base}-1x1{ext}")

if __name__ == "__main__":
    main()
