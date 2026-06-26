# magic-ai-skills

这是一个私有的个人 AI Skills 仓库，只收录我自己创建并稳定使用的 Magic AI 工作流 Skills。

当前只包含 2 个 Skills：

| Skill | 用途 | 外部依赖 |
| --- | --- | --- |
| `magic-recorder` | 把口述、粗糙转写、Get 笔记材料整理成结构化 Markdown 思考记录 | Get 笔记官方能力（输入源，可选）、本地 Markdown 工作区（输出目标，可选） |
| `magic-kb-compiler` | 把语音笔记、Get 笔记、剪藏、AI 对话和松散想法编译成可迁移的知识资产 | Get 笔记官方能力（输入源，可选）、Obsidian / ima 目标知识库 |

## 这个仓库不包含什么

`getnote` 不再放进本仓库。它属于 Get 笔记官方 OpenAPI / 官方 Skill / 外部服务适配层，不是我的自制 Magic AI Skill。

本仓库也不包含：

- 第三方或他人创建的 Skills
- 系统内置 Skills
- 插件缓存 Skills
- 外部服务配套 Skills
- 历史版本
- 真实 token、cookie、`.env`、私密笔记内容

## 工作流关系

这两个 Skills 的核心边界是“处理规则”，不是某一个平台：

1. `magic-recorder`：把一段原始表达整理成个人思考记录。它可以接收粘贴文本、文件、转写稿，也可以接收来自 Get 笔记的材料。
2. `magic-kb-compiler`：把原始材料编译成知识资产，包括 raw、cards、wiki、views、logs、导入包或平台发布稿。
3. Get 笔记：是外部输入源。接入方式参考 Get 笔记官方 OpenAPI 文档和官方 Skill 页。
4. Obsidian：是当前成熟的本地落地目标，适合保留 raw、schema、cards、wiki、views 和 logs。
5. ima：是当前兼容的知识库目标，优先输出可导入的 Markdown 知识包、主题条目和来源摘要。只有实际调用平台 API 或完成导入后，才说明已经写入 ima。

## 运行环境兼容

这些 Skills 尽量保持为普通 `SKILL.md` 规则和本机文件/命令约定，不绑定某一个 Agent 产品。

当前目标运行环境：

- Codex
- Claude
- ima
- WorkBuddy
- OpenClaw
- Hermes

兼容原则：

- Skill 本体只依赖 Markdown 指令、相对路径和可选脚本。
- 平台私有能力只写成可选能力，不写成默认必需条件。
- 如果某个平台不能直接安装 Skills，先把本仓库当作规则源，让该平台读取对应 `SKILL.md`。
- 不在仓库中保存任何平台 token、cookie、`.env` 或私密知识库内容。

详细说明见 [docs/runtime-compatibility.md](docs/runtime-compatibility.md)。

## 外部依赖

详细说明见 [docs/external-dependencies.md](docs/external-dependencies.md)。

### Get 笔记

官方入口：

- OpenAPI 文档：https://www.biji.com/openapi?tab=docs
- Skill 说明：https://www.biji.com/openapi?tab=skill

我们的 Skills 只声明“可以使用 Get 笔记作为输入源”，不在仓库内复制 Get 笔记官方 Skill。

### 知识库目标平台

`magic-kb-compiler` 支持两个目标知识库：

- Obsidian / Magic AI 知识库
- ima

Obsidian 是当前最完整的本地实现，适合保存 raw、schema、cards、wiki、views 和 logs。

ima 模式不照搬 Obsidian 文件结构，默认生成平台友好的 Markdown 导入包、主题知识条目和来源摘要。

如果用户没有指定目标平台，优先使用 Obsidian；如果本机没有可用的 `magic-ai-kb`，输出 ima/Markdown 导入包，并明确说明尚未写入任何平台。

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
cp -R skills/magic-recorder ~/.codex/skills/
cp -R skills/magic-kb-compiler ~/.codex/skills/
```

Get 笔记接入请单独按官方说明配置。目标知识库当前只承诺兼容 Obsidian 和 ima。

## 维护规则

- 新增 Skill 前先确认它是不是自己创建和维护。
- 如果依赖外部服务或官方 Skill，只在 registry 里注明，不复制外部 Skill。
- 如果依赖 Obsidian、本地 vault 或其他工作区，要在 README 和 registry 中明确写出。
- 提交前扫描敏感信息和无关依赖目录。
