#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神奇桑桑公众号 HTML 生成器
从对标文章提取的真实样式，套用页头/页尾 + 橙色标题分割区。
用法: python3 build_wechat_html.py <input.md> <output.html>
"""
import sys, re, html as htmllib

BRAND = "#ff6827"          # 品牌橙（仅用于关键位置点缀：标题左竖条、页尾"点赞"）
TEXT = "#1a1c1f"           # 正文主色（黑）
# ↓↓↓ 神奇桑桑微调区：想松一点把 LINE_HEIGHT 调大（如 2.0/2.1），段距改 PARA_MARGIN ↓↓↓
LINE_HEIGHT = "1.9"        # 行间距（行高），1.75 较紧、1.9 适中、2.1 较松
PARA_MARGIN = "20px"       # 段间距（段落上下外边距）
FONT_SIZE = "17px"         # 正文字号
# ↑↑↑ 微调区结束 ↑↑↑
P_OPEN = ('<p style="box-sizing:border-box;margin:%s 0;padding:0;'
          'font-size:14px;line-height:%s;color:%s;font-weight:normal;text-align:start;">' % (PARA_MARGIN, LINE_HEIGHT, TEXT))
SPAN_OPEN = '<span style="font-size:%s;letter-spacing:1px;font-weight:normal;">' % FONT_SIZE

def inline(text):
    """处理 **加粗**、`代码`、链接，转义其余。色调：黑色为主，不全局变橙。"""
    # 先转义
    text = htmllib.escape(text)
    # 裸 URL -> 链接（黑字+浅下划线，停在 * ` 前避免吞掉加粗标记）
    text = re.sub(r'(https?://[^\s<>*`）)]+)',
                  r'<a href="\1" style="color:%s;border-bottom:1px solid #d0d0d5;text-decoration:none;">\1</a>' % TEXT, text)
    # **加粗** -> 黑色加粗（标题/关键词/关键句），不变橙
    text = re.sub(r'\*\*(.+?)\*\*',
                  r'<strong style="color:%s;font-weight:600;">\1</strong>' % TEXT, text)
    # `代码` -> 浅灰底黑字
    text = re.sub(r'`(.+?)`',
                  r'<code style="background:#f4f4f5;border-radius:3px;padding:1px 5px;font-size:15px;color:%s;">\1</code>' % TEXT, text)
    return text

def h2(text):
    # 标题分割区：橙色左竖条做关键位置点缀，标题文字仍为黑色
    return ('<h2 style="margin:36px 0 16px;padding:2px 0 2px 12px;'
            'border-left:3px solid %s;font-size:19px;font-weight:600;'
            'line-height:1.5;color:%s;"><span style="letter-spacing:1px;">%s</span></h2>'
            % (BRAND, TEXT, inline(text)))

def para(text):
    return '%s%s%s</span></p>' % (P_OPEN, SPAN_OPEN, inline(text))

def figure(caption):
    label = htmllib.escape(caption.replace("配图：", "").replace("配图:", ""))
    return ('<p style="margin:22px 0;text-align:center;">'
            '<span style="display:inline-block;padding:24px 18px;background:#f7f7f8;'
            'border:1px dashed #d2d2d7;border-radius:8px;color:#9a9aa0;font-size:13px;line-height:1.7;">'
            '📷 配图位 ｜ %s</span></p>' % label)

def blockquote(text):
    # 摘要：灰色左竖条（非橙），贴近原文 default 风格
    return ('<blockquote style="margin:16px 0 22px;padding:12px 16px;'
            'border-left:3px solid #d0d0d5;background:#fafafa;border-radius:0 4px 4px 0;">'
            '<span style="font-size:15px;line-height:1.8;color:#6a6a70;letter-spacing:0.5px;">%s</span>'
            '</blockquote>' % inline(text))

# ---------- 页头：公众号名片卡（神奇桑桑固定，逐字保留用户提供版本）----------
PROFILE_CARD = ('<section class="mp_profile_iframe_wrp" nodeleaf="">'
    '<mp-common-profile class="js_uneditable custom_select_card mp_profile_iframe" '
    'data-pluginname="mpprofile" data-nickname="神奇的桑桑" data-alias="magicsang333" data-from="0" '
    'data-headimg="http://mmbiz.qpic.cn/mmbiz_png/RKNUXvIZladcicnduagTEknze8ebeMBvEarfCWuT93a5L62WZrStKV93VAJmLeU2cT9yczA7iaMuBYlJpwBYYuYA/0?wx_fmt=png" '
    'data-signature="为中小企业或个人提供全域流量思维策略，搭建 Ai 运营内容矩阵，实现全域精准内容获客，助力企业完善私域会员运营。🛰 MagicSang666 🔗全域俱乐部" '
    'data-id="MzA5MzYxNjM2Ng==" data-is_biz_ban="0" data-service_type="1" data-verify_status="0"></mp-common-profile></section>')

# ---------- 固定页尾模板（从对标文章提取，逐字保留：居中两行 + 搜索卡 + 细线 + 商业引导 + 推荐阅读）----------
_CENTER_P = ('margin:8px 0 16px;padding:0;clear:both;min-height:1em;'
             'font-family:Optima-Regular,PingFangTC-light,"PingFang SC",-apple-system-font,BlinkMacSystemFont,"Helvetica Neue",sans-serif;'
             'font-size:16px;line-height:1.75em;color:rgb(17,17,17);letter-spacing:1px;text-align:center;')
_PITCH_S = ('margin:8px 0 16px;font-family:Optima-Regular,PingFangTC-light,"PingFang SC",-apple-system-font,BlinkMacSystemFont,"Helvetica Neue",sans-serif;'
            'font-size:16px;line-height:1.75;letter-spacing:1px;color:rgb(0,0,0);')
_LINK_P = 'margin:8px 0;line-height:1.75em;font-size:16px;'
FOOTER = '''
<p style="%(cp)s">感谢你的<span style="color:%(brand)s;font-weight:bold;">点赞，关注，在看，转发</span>为我加油~</p>
<p style="%(cp)s">👇👇关注我👇👇</p>
<section class="mp_search_iframe_wrp" nodeleaf=""><mp-common-search class="js_mpsearch appmsg_search_iframe js_uneditable custom_select_card" data-headimg="https://wx.qlogo.cn/mmopen/ajNVdqHZLLAB2jzkbQria4yHP5X5DeWXMEKU8gJppOmkcLgPFoBSmdGzGhA52rP5ud7jT4W7CKuIWDrciavv5iaG2KtkuYzzq444gxPCWl8MQiaCDFyibcH594klUEtvRnY2d/64" data-keywords="%%5B%%7B%%22label%%22%%3A%%22AiSkills%%22%%7D%%2C%%7B%%22label%%22%%3A%%22%%E8%%A1%%8C%%E5%%8A%%A8%%E6%%8C%%87%%E5%%8D%%97%%22%%7D%%2C%%7B%%22label%%22%%3A%%22%%E7%%A5%%9E%%E5%%A5%%87%%E6%%A1%%91%%E6%%A1%%91%%22%%7D%%2C%%7B%%22label%%22%%3A%%22%%E5%%A2%%9E%%E9%%95%%BF%%E4%%BF%%B1%%E4%%B9%%90%%E9%%83%%A8%%22%%7D%%5D" data-nickname="神奇的桑桑" data-pluginname="insertsearch"></mp-common-search></section>
<hr style="border-style:solid;border-width:1px 0 0;border-color:rgba(0,0,0,0.1);transform-origin:0 0;transform:scale(1,0.5);margin:16px 0;"/>
<section style="%(ps)s">如果你是中小企业老板、业务负责人，正在思考怎么用 AI 做降本增效，但还不清楚应该从哪个业务环节开始，欢迎链接我。</section>
<section style="%(ps)s">我擅长的不是简单推荐工具，而是帮你把复杂业务流程拆开：从获客、成交、交付、客服、复购到内部协作，找出最耗人、最重复、最适合被 AI 放大的环节，先做一版能落地的业务流梳理和提效方案。</section>
<section style="%(ps)s">我们可以语音聊 30 分钟，一起看看你的业务里，哪些地方可以先省成本、提效率、跑出结果。</section>
<section style="%(ps)s">我是神奇桑桑（MagicSang666），持续公开普通人和中小企业如何把 AI 真正用进业务。欢迎来我的 AI 实验室：</section>
<p style="%(lp)s;color:rgb(0,0,0);">推荐阅读：</p>
<p style="%(lp)s"><a href="https://mp.weixin.qq.com/s?__biz=MzA5MzYxNjM2Ng==&amp;mid=2648168454&amp;idx=1&amp;sn=684797bc9944dd929b256a7422ad1a60&amp;scene=21#wechat_redirect" style="color:#576b95;text-decoration:none;">微信开放小程序 AI 能力：为什么它可能成为重要入口？</a></p>
<p style="%(lp)s"><a href="https://mp.weixin.qq.com/s?__biz=MzA5MzYxNjM2Ng==&amp;mid=2648168449&amp;idx=1&amp;sn=e82352dbbe017ac878e38433b7c5adfa&amp;scene=21#wechat_redirect" style="color:#576b95;text-decoration:none;">不知道你们有没有这种体感，如果你长期只用...</a></p>
<p style="%(lp)s"><a href="https://mp.weixin.qq.com/s?__biz=MzA5MzYxNjM2Ng==&amp;mid=2648168443&amp;idx=1&amp;sn=dba5d0df395300a81e9300906ddb03d4&amp;scene=21#wechat_redirect" style="color:#576b95;text-decoration:none;">AI 手记：260501-260531</a></p>
''' % {"brand": BRAND, "cp": _CENTER_P, "ps": _PITCH_S, "lp": _LINK_P}

def main():
    src, out = sys.argv[1], sys.argv[2]
    raw = open(src, encoding="utf-8").read()
    # 去 frontmatter
    raw = re.sub(r'^---.*?---\n', '', raw, count=1, flags=re.S)
    lines = raw.split("\n")
    body = []
    in_summary = False
    for line in lines:
        s = line.rstrip()
        if not s.strip():
            continue
        if s.startswith("# "):           # 文章大标题 -> 跳过（公众号标题单独传）
            continue
        if s.startswith("> "):            # 摘要 blockquote + 紧跟公众号名片卡
            body.append(blockquote(s[2:].strip()))
            body.append(PROFILE_CARD)
        elif s.startswith("## "):
            body.append(h2(s[3:].strip()))
        elif s.startswith("【配图"):
            body.append(figure(s.strip("【】")))
        elif re.match(r'^\d+\.\s', s):     # 有序列表项 -> 当作段落（带序号）
            body.append(para(s))
        else:
            body.append(para(s))
    content = "\n".join(body) + FOOTER
    wrapper = ('<div style="font-family:-apple-system,system-ui,\'Segoe UI\',sans-serif;'
               'color:%s;">\n%s\n</div>' % (TEXT, content))
    open(out, "w", encoding="utf-8").write(wrapper)
    print("WROTE", out, len(wrapper), "bytes")

if __name__ == "__main__":
    main()
