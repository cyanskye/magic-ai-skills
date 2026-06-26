# 安装说明

## 安装本仓库 Skills

### Codex

```bash
mkdir -p ~/.codex/skills
cp -R skills/magic-recorder ~/.codex/skills/
cp -R skills/magic-kb-compiler ~/.codex/skills/
```

### Claude

```bash
mkdir -p ~/.claude/skills
cp -R skills/magic-recorder ~/.claude/skills/
cp -R skills/magic-kb-compiler ~/.claude/skills/
```

### 其他 Agent / AI 工作台

ima、WorkBuddy、OpenClaw、Hermes 等环境如果支持本地 Skills 或类似机制，把这两个目录放到对应平台的 Skills 目录：

```text
skills/magic-recorder
skills/magic-kb-compiler
```

如果平台没有原生 Skills 目录，就把本仓库当作规则源，让 Agent 读取对应 `SKILL.md`。详细边界见 [runtime-compatibility.md](runtime-compatibility.md)。

## Get 笔记接入

本仓库不安装也不复制 Get 笔记官方 Skill。

如果要让 `magic-recorder` 或 `magic-kb-compiler` 读取 Get 笔记，请按官方页面配置：

- https://www.biji.com/openapi?tab=docs
- https://www.biji.com/openapi?tab=skill

常见需要准备的配置包括：

```bash
GETNOTE_API_KEY=...
GETNOTE_CLIENT_ID=...
GETNOTE_OWNER_ID=... # optional
```

不要把真实 `.env`、token、cookie 或私密笔记内容提交到这个仓库。

## 知识库目标平台

`magic-kb-compiler` 当前只承诺两个知识库目标：Obsidian 和 ima。

### Obsidian 模式

Obsidian 模式默认依赖这些目录或文件：

```text
magic-ai-kb/
  00-index.md
  schema/
  raw/
  cards/
  wiki/
  views/
  logs/
```

如果你的 vault 路径变化，请在使用 Skill 时明确告诉 Agent 当前 `magic-ai-kb` 路径。

### ima 模式

ima 可以作为目标，但不要直接套用 Obsidian 的文件结构。

使用这类平台时，应先明确：

- ima 支持导入什么格式：Markdown、PDF、docx、网页链接、文件夹、API。
- 是否需要保留 raw 原文。
- 是否需要输出 cards/wiki/views/logs，还是合并成平台友好的知识条目。
- 增量更新如何处理：覆盖、追加、版本化，还是人工确认后导入。
- 是否需要单独的发布脚本或手动导入说明。
