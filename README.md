# magic-ai-skills

这是一个私有的个人 AI Skills 仓库，只收录当前稳定使用、由我自己维护的 Magic AI 工作流 Skills。

当前只包含 3 个 Skills：

| Skill | 用途 | 依赖 |
| --- | --- | --- |
| `magic-recorder` | 把中文/双语口述、粗糙转写、Get 笔记整理成结构化 Markdown 思考记录 | `getnote`（当输入来自 Get 笔记时） |
| `magic-kb-compiler` | 把语音笔记、Get 笔记、剪藏、AI 对话、松散想法编译进 Magic AI 知识库 | `getnote`（当输入来自 Get 笔记时） |
| `getnote` | 读取、搜索、保存、管理 Get 笔记，并作为 Magic AI 知识库输入源 | 外部 Get 笔记 OpenAPI 凭据 |

## 为什么是一个仓库

这 3 个 Skills 是同一个工作流的不同层：

1. `getnote` 负责从 Get 笔记读取原始材料。
2. `magic-recorder` 负责把口述或笔记整理成个人思考记录。
3. `magic-kb-compiler` 负责把原始材料编译成 Magic AI 知识库资产。

把它们放在一个仓库里，依赖关系更清楚，也方便同步到不同 Agent 环境。

## 依赖关系

详细依赖见：

- [registry/dependencies.md](registry/dependencies.md)
- [registry/skills.json](registry/skills.json)
- [registry/dependency-graph.mmd](registry/dependency-graph.mmd)

## 安装

这个仓库不保存密钥，也不保存历史版本。使用时把需要的目录复制或软链接到对应 Agent 的 skills 目录。

示例：

```bash
# Codex
mkdir -p ~/.codex/skills
cp -R skills/getnote ~/.codex/skills/
cp -R skills/magic-recorder ~/.codex/skills/
cp -R skills/magic-kb-compiler ~/.codex/skills/
```

`getnote` 需要本地环境变量或本机私有配置：

```bash
GETNOTE_API_KEY=...
GETNOTE_CLIENT_ID=...
GETNOTE_OWNER_ID=... # optional
```

不要把真实 `.env`、token、cookie 或私密笔记内容提交到这个仓库。

## 当前范围

本仓库只保留自己创建并稳定使用的 Skills。

明确不包含：

- 第三方或他人创建的 Skills
- 系统内置 Skills
- 插件缓存 Skills
- 外部服务配套 Skills
- 历史版本

## 维护规则

- 新增 Skill 前先确认它是不是自己创建和维护。
- 如果一个自制 Skill 依赖另一个自制 Skill，两个都要放进仓库，并更新依赖登记。
- 如果依赖外部服务或第三方 Skill，只在 registry 里注明，不复制外部 Skill。
- 提交前扫描敏感信息和无关依赖目录。
