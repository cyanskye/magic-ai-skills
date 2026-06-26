# magic-ai-skills

这是一个私有的个人 AI Skills 仓库，只收录我自己创建并稳定使用的 Magic AI 工作流 Skills。

## 包含内容

当前仓库只保留 2 个自制 Skills：

| Skill | 作用 | 主要依赖 |
| --- | --- | --- |
| `magic-recorder` | 把口述、粗糙转写、Get 笔记材料整理成结构化 Markdown 思考记录 | Get 笔记官方能力（可选）、本地 Markdown 工作区（可选） |
| `magic-kb-compiler` | 把语音笔记、Get 笔记、剪藏、AI 对话和松散想法编译成可迁移的知识资产 | Get 笔记官方能力（可选）、Obsidian / ima |

## 仓库边界

本仓库只保存 Skills 规则，不保存：

- 第三方或他人创建的 Skills
- 系统内置 Skills
- 插件缓存 Skills
- 外部服务配套 Skills
- 历史版本
- 真实 token、cookie、`.env`、私密笔记内容

`getnote` 不在仓库内。它属于 Get 笔记官方 OpenAPI / 官方 Skill / 外部服务适配层。

## 怎么理解这两个 Skills

这两个 Skills 处理的是“规则”，不是绑定某一个平台。

1. `magic-recorder` 负责把原始表达整理成个人思考记录。
2. `magic-kb-compiler` 负责把原始材料编译成知识资产。
3. Get 笔记是外部输入源。
4. Obsidian 是当前最完整的本地知识库目标。
5. ima 是当前兼容的知识库目标，输出以可导入的 Markdown 知识包为主。

## 兼容范围

仓库里的 Skills 尽量保持为通用 `SKILL.md` 规则，不绑定单一 Agent 产品。

当前兼容说明：

- 运行环境：Codex、Claude、ima、WorkBuddy、OpenClaw、Hermes
- 目标知识库：Obsidian、ima

兼容的意思是：这些环境可以读取或迁移本仓库的 `SKILL.md` 规则；不代表每个平台都内置自动安装、API 写入或导入能力。

详细说明见：

- [docs/runtime-compatibility.md](docs/runtime-compatibility.md)
- [docs/external-dependencies.md](docs/external-dependencies.md)

## 安装

把需要的目录复制或软链接到对应 Agent 的 skills 目录。

```bash
# Codex
mkdir -p ~/.codex/skills
cp -R skills/magic-recorder ~/.codex/skills/
cp -R skills/magic-kb-compiler ~/.codex/skills/
```

如果平台没有原生 Skills 目录，就把本仓库当作规则源，让 Agent 直接读取对应 `SKILL.md`。

## 依赖关系

详细依赖见：

- [registry/dependencies.md](registry/dependencies.md)
- [registry/skills.json](registry/skills.json)
- [registry/dependency-graph.mmd](registry/dependency-graph.mmd)

## 维护规则

- 新增 Skill 前先确认它是不是自己创建和维护。
- 如果依赖外部服务或官方 Skill，只在 registry 里注明，不复制外部 Skill。
- 如果依赖 Obsidian、本地 vault 或其他工作区，要在 README 和 registry 中明确写出。
- 提交前扫描敏感信息和无关依赖目录。
