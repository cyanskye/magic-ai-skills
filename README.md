# magic-ai-skills

AI Skills · SKILL

装一次，多平台复用。

把我自制的 Magic AI 工作流 Skills 接入你正在使用的 Agent 平台。一句话触发口述整理、知识编译、公众号发布，并按 Obsidian / ima / 微信草稿输出。

## 安装提示词

发给支持 GitHub / Skill 安装的 Agent：

```text
请从 GitHub 私有仓库安装 Magic AI Skills。

仓库地址：git@github.com:cyanskye/magic-ai-skills.git

只安装这三个自制 Skills：
- skills/magic-recorder
- skills/magic-kb-compiler
- skills/magic-wechat

不要安装 getnote、系统 Skills、插件缓存 Skills、第三方 Skills 或历史版本。
```

前提：当前环境必须有这个私有仓库的 GitHub 访问权限。

如果平台不能从 GitHub 自动安装，就手动复制对应目录：

```bash
git clone git@github.com:cyanskye/magic-ai-skills.git
cd magic-ai-skills

mkdir -p ~/.codex/skills
cp -R skills/magic-recorder ~/.codex/skills/
cp -R skills/magic-kb-compiler ~/.codex/skills/
cp -R skills/magic-wechat ~/.codex/skills/
```

Claude 等其他 Agent，把目录复制到它自己的 `skills` 目录即可。

## 使用提示词

整理口述或粗糙转写：

```text
请使用 magic-recorder，把下面这段口述整理成个人 Markdown 思考记录：
...
```

编译到 Obsidian / Magic AI 知识库：

```text
请使用 magic-kb-compiler，把这份材料编译成 Obsidian 知识资产。
目标知识库路径是：...
```

导出给 ima：

```text
请使用 magic-kb-compiler，把这份材料整理成 ima 可导入的 Markdown 知识包。
不要写入 Obsidian，保留来源、摘要、主题和导入说明。
```

不确定目标平台时：

```text
请使用 magic-kb-compiler，先判断这份材料应该写入 Obsidian 还是导出 ima 知识包。
如果依赖外部输入源，请先说明依赖关系。
```

发布公众号文章：

```text
请使用 magic-wechat，把这篇 Markdown 整理成公众号草稿：
套用固定排版、本地生成纯文字封面、存到草稿箱（不直接群发）。
```

## 当前包含

| Skill | 作用 | 主要依赖 |
| --- | --- | --- |
| `magic-recorder` | 把口述、粗糙转写、Get 笔记材料整理成结构化 Markdown 思考记录 | Get 笔记官方能力（可选）、本地 Markdown 工作区（可选） |
| `magic-kb-compiler` | 把语音笔记、Get 笔记、剪藏、AI 对话和松散想法编译成可迁移的知识资产 | Get 笔记官方能力（可选）、Obsidian / ima |
| `magic-wechat` | 把 Markdown 文章套固定排版、本地出纯文字封面（可商用字体）、一键存公众号草稿 | 微信公众号官方 API、Pillow + 阿里普惠体；思路源自宝玉 `baoyu-post-to-wechat`（见「来源标注」） |

## 适用场景

- 日常记录：口述、转写稿、临时想法、Get 笔记内容整理成个人 Markdown。
- 知识编译：把原始材料拆成 cards、wiki、views、logs 等可追踪知识资产。
- 平台迁移：把同一套知识资产输出给 Obsidian 或 ima。
- Agent 复用：让 Codex、Claude、ima、WorkBuddy、OpenClaw、Hermes 等环境读取同一套 `SKILL.md` 规则。

## 依赖边界

`getnote` 不在本仓库里。它是 Get 笔记官方 OpenAPI / 官方 Skill / 外部服务适配层，只作为可选输入源。

Obsidian 和 ima 是 `magic-kb-compiler` 当前明确支持的目标知识库：

- Obsidian：完整本地知识库模式，支持 raw、cards、wiki、views、logs。
- ima：导入包模式，输出 Markdown 知识包和导入说明。

## 不收录

- 第三方或他人创建的 Skills
- 系统内置 Skills
- 插件缓存 Skills
- 外部服务配套 Skills
- 历史版本
- 真实 token、cookie、`.env`、私密笔记内容

## 来源标注

规矩：**凡是从他人 Skill 衍生或运行时依赖的，都在此标注原 Skill 的位置/来源。**

- `magic-wechat`：公众号发布的整套思路源自**宝玉 `baoyu-post-to-wechat`**（宝玉 Skills 系列，安装于 `~/.claude/skills/baoyu-post-to-wechat`）。本仓库的 `scripts/publish.py` 为自建实现，直调微信官方 `draft/add` API，**不含宝玉源码**；排版样式取自神奇桑桑本人公众号文章。

## 详细文档

- [docs/install.md](docs/install.md)
- [docs/runtime-compatibility.md](docs/runtime-compatibility.md)
- [docs/external-dependencies.md](docs/external-dependencies.md)
- [registry/dependencies.md](registry/dependencies.md)
- [registry/skills.json](registry/skills.json)
