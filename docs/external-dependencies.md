# 外部依赖

本仓库里的 Skills 不独立完成所有工作。它们依赖输入源和目标平台。Get 笔记是典型输入源；Obsidian 和 ima 是当前明确支持的知识库目标平台。

## Get 笔记

Get 笔记是外部输入源，不属于本仓库收录的自制 Skills。

官方页面：

- OpenAPI 文档：https://www.biji.com/openapi?tab=docs
- Skill 说明：https://www.biji.com/openapi?tab=skill

### 在本工作流里的角色

Get 笔记提供原始材料，例如：

- 最新笔记
- 指定笔记
- 分享链接里的笔记内容
- 音频转写稿
- 文本笔记

`magic-recorder` 可以把这些材料整理成个人思考记录。

`magic-kb-compiler` 可以把这些材料编译成 Obsidian / Magic AI 知识库资产，或 ima 可导入知识包。

### 接入方式

优先使用 Get 笔记官方提供的 OpenAPI / Skill 能力。仓库内不复制官方 Skill。

通常需要本机具备：

```bash
GETNOTE_API_KEY=...
GETNOTE_CLIENT_ID=...
GETNOTE_OWNER_ID=... # optional
```

Agent 在使用时应遵守：

- 不打印真实凭据。
- 不把 `.env` 提交进仓库。
- 默认把 Get 笔记内容视为私密材料。
- 只在当前任务需要时读取具体笔记内容。

## 知识库目标平台

`magic-kb-compiler` 的核心能力是把原始材料编译成可复用知识资产。当前只承诺两个目标平台：Obsidian / Magic AI 知识库、ima。

### 在本工作流里的角色

在完整本地知识库模式下，`magic-kb-compiler` 会把输入材料编译成：

- `raw/` 原始材料
- `cards/` 原子卡片
- `wiki/` 主题页面
- `views/` 问题池、选题池、待办视图
- `logs/` 编译日志

### Obsidian / Magic AI 知识库模式

这是当前最完整、最可追溯的落地模式。使用前应确认知识库里存在：

```text
magic-ai-kb/
  00-index.md
  schema/mvp-definition.md
  schema/compile-rules.md
  schema/card-types.md
  schema/recompile-rules.md
```

这些 schema 决定如何拆卡、去重、更新 wiki/views，以及如何写 compile log。

### ima 模式

ima 可以作为目标平台。它更像“导入/检索/问答空间”，不应该原样承载 Obsidian 的 raw/cards/wiki/views/logs 文件结构。

面向 ima 的适配可以输出：

- 整理后的 Markdown 文档
- 按主题拆分的知识条目
- 带来源和摘要的导入包
- 可人工确认后导入的平台材料

如果 ima 提供稳定 API 或官方导入能力，可以再补自动化发布脚本。没有稳定 API 时，Skill 应先生成可导入文件包和操作说明，不要假装已经完成平台写入。

### 重要边界

本仓库不保存 Obsidian vault 内容，也不保存 ima 中的知识库内容。

本仓库只保存 Skills 规则；实际知识资产保存在用户选择的目标平台中。
