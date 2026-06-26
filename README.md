# magic-ai-skills

这是我的私有 Skills 仓库，只保留我自己创建并稳定使用的两个 Skill。

## 一句话安装

把需要的 Skill 目录放进你当前 Agent 的 `skills` 目录。

如果你的 Agent 支持自然语言安装，可以直接说：

- `请安装 magic-recorder 技能`
- `请安装 magic-kb-compiler 技能`

仓库源地址：

- `git@github.com:cyanskye/magic-ai-skills.git`

如果你的 Agent 支持从 GitHub 仓库安装，就直接指向这个仓库。

```bash
# Codex
mkdir -p ~/.codex/skills
cp -R skills/magic-recorder ~/.codex/skills/
cp -R skills/magic-kb-compiler ~/.codex/skills/

# Claude
mkdir -p ~/.claude/skills
cp -R skills/magic-recorder ~/.claude/skills/
cp -R skills/magic-kb-compiler ~/.claude/skills/
```

只装一个也可以，直接复制对应目录即可。

## 一句话调用

- `请使用 magic-recorder，把这段口述整理成 Markdown。`
- `请使用 magic-kb-compiler，把这份材料编译成 Obsidian 知识卡。`
- `请使用 magic-kb-compiler，把这份材料编译成 ima 可导入的知识包。`

## 当前包含

| Skill | 作用 | 主要依赖 |
| --- | --- | --- |
| `magic-recorder` | 把口述、粗糙转写、Get 笔记材料整理成结构化 Markdown 思考记录 | Get 笔记官方能力（可选）、本地 Markdown 工作区（可选） |
| `magic-kb-compiler` | 把语音笔记、Get 笔记、剪藏、AI 对话和松散想法编译成可迁移的知识资产 | Get 笔记官方能力（可选）、Obsidian / ima |

## 这仓库不放什么

- 第三方或他人创建的 Skills
- 系统内置 Skills
- 插件缓存 Skills
- 外部服务配套 Skills
- 历史版本
- 真实 token、cookie、`.env`、私密笔记内容

`getnote` 不在仓库内。它属于 Get 笔记官方 OpenAPI / 官方 Skill / 外部服务适配层。

## 兼容范围

运行环境：Codex、Claude、ima、WorkBuddy、OpenClaw、Hermes。

目标知识库：Obsidian、ima。

这表示这些环境可以读取或迁移本仓库的 `SKILL.md` 规则，不表示每个平台都内置自动安装、API 写入或导入能力。

详细说明见：

- [docs/install.md](docs/install.md)
- [docs/runtime-compatibility.md](docs/runtime-compatibility.md)
- [docs/external-dependencies.md](docs/external-dependencies.md)

## 依赖关系

详细依赖见：

- [registry/dependencies.md](registry/dependencies.md)
- [registry/skills.json](registry/skills.json)
- [registry/dependency-graph.mmd](registry/dependency-graph.mmd)

## 维护规则

- 只收录我自己创建和维护的 Skill。
- 依赖外部服务或官方 Skill 时，只在 registry 和说明里注明，不复制外部 Skill。
- 依赖 Obsidian、本地 vault 或其他工作区时，要明确写出目标路径和边界。
- 提交前扫描敏感信息和无关依赖目录。
