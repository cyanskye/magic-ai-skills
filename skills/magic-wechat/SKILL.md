---
name: magic-wechat
description: 神奇桑桑自用公众号发布。把 markdown 文章套用固定排版（页头名片卡+橙竖条标题+固定页尾）、本地生成纯文字封面（可商用字体、2.35:1 兼容朋友圈 1:1）、一键存草稿并带上可自动化的设置（留言/只关注可评/原文链接/指定微信号预览）。Use when 神奇桑桑 wants to 发公众号文章 / 出文字封面 / 存草稿.
---

# magic-wechat（神奇桑桑自用公众号发布）

只发**草稿**，绝不直接群发。文章**纯文字、不放图**（约定，省掉配图步骤）。

## 生产约定（写 markdown 时遵守）

- frontmatter：`title` / `author` / `summary`
- 正文用 `## 小标题`（自动渲染成橙色左竖条分割区）
- 关键词/关键句用 `**包起来**` → 黑色加粗（**只包关键词，别包整句**，否则像全文加粗）
- **不要插图**

## 三步流程

> 脚本均在本 skill 的 `scripts/` 下，下方命令以 skill 目录为基准（或写绝对路径）。

### ① 套排版出 HTML
```bash
python3 scripts/build_html.py 文章.md 文章.html
```
- 自动加：页头摘要 blockquote + 公众号名片卡、正文 17px/字距 1px、橙竖条 H2、固定页尾（感谢点赞橙加粗居中 + 关注我居中 + 搜索卡 + 商业引导4段 + 推荐阅读3链接）
- 微调旋钮在 `build_html.py` 顶部：`LINE_HEIGHT`（行高，默认 1.9）、`PARA_MARGIN`（段距）、`FONT_SIZE`

### ② 本地生成纯文字封面（零 API、不侵权）
```bash
python3 scripts/build_cover.py --label "写给爱折腾的 AI 同好" \
  --line1 "你做的 AI 小工具" --line2 "一半人" --hl "「打不开」" \
  --sub "GitHub → Gitee 自动镜像 · 零维护" --out images/cover.png
```
- 阿里巴巴普惠体（免费商用）；2.35:1，关键字在中心 1:1 安全区，自动导出 `*-1x1.png` 预览
- ⚠️ 禁用 macOS 苹方/黑体（Apple 专用，商用侵权）
- 想要**插画封面**：用提示词去 GPT 出，焦点元素居中（裁 1:1 不丢主体），存成 `images/cover.png`

### ③ 存草稿（带可自动化的设置 + 预览）
```bash
python3 scripts/publish.py 文章.html --cover images/cover.png \
  --title "标题" --author "神奇桑桑" --digest "摘要" \
  --source-url "阅读原文链接" --preview-to MagicSang666
```
默认 `--open-comment 1 --only-fans 1`（留言开、只关注可评）。

## 哪些能自动 / 哪些只能手动

| 设置 | 自动？ |
|------|------|
| 封面 2.35:1 / 留言开关 / 只关注可评 / 原文链接 | ✅ publish.py 已带 |
| 指定微信号预览 | ⚠️ 代码已带，但本号无群发接口权限（报 `48001`），实际**手动**预览 |
| 原创声明+快捷转载 / 赞赏 / 自动精选留言 / 合集 / 创作来源(AI生成) / 平台推荐 | ❌ 微信无 API，**编辑器手动** |

> 存草稿后，去 mp.weixin.qq.com 草稿箱手动补：勾原创+快捷转载、自动精选留言、合集选「行动指南」、创作来源选「内容由AI生成」、需要时手动预览。其余默认即可。

## 凭据
读 `<cwd>/.baoyu-skills/.env` 或 `~/.baoyu-skills/.env` 的 `WECHAT_APP_ID` / `WECHAT_APP_SECRET`。需在公众号后台把本机出口 IP 加进白名单。

## 踩坑备忘
- 正文字重必须 `normal`——`font-weight:430` 在微信会被渲染成粗体。
- 公众号名片卡 `<mp-common-profile>` / 搜索卡 `<mp-common-search>` 直接写进 HTML，API 草稿能保留。
- AI 出图若用 baoyu-danger-gemini-web：必须 `-m gemini-3-flash`（默认 pro 不返图），且不稳，故默认走本地文字封面。
