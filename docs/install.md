# 安装说明

## 安装源

GitHub 仓库：

```text
git@github.com:cyanskye/magic-ai-skills.git
```

安装前提：

- 当前机器或 Agent 已有这个仓库的 GitHub 访问权限。
- 只安装 `skills/magic-recorder` 和 `skills/magic-kb-compiler`。
- 不安装 `getnote`、系统 Skills、插件缓存 Skills、第三方 Skills 或历史版本。

## 推荐安装提示词

发给支持 GitHub / Skill 安装的 Agent：

```text
请从 GitHub 仓库安装 Magic AI Skills。

仓库地址：git@github.com:cyanskye/magic-ai-skills.git

只安装这两个自制 Skills：
- skills/magic-recorder
- skills/magic-kb-compiler

不要安装 getnote、系统 Skills、插件缓存 Skills、第三方 Skills 或历史版本。
```

## 手动安装

### Codex

```bash
git clone git@github.com:cyanskye/magic-ai-skills.git
cd magic-ai-skills

mkdir -p ~/.codex/skills
cp -R skills/magic-recorder ~/.codex/skills/
cp -R skills/magic-kb-compiler ~/.codex/skills/
```

### Claude

```bash
git clone git@github.com:cyanskye/magic-ai-skills.git
cd magic-ai-skills

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

如果平台没有原生 Skills 目录，就把本仓库当作规则源，让 Agent 读取对应 `SKILL.md`。

## 使用提示词

### magic-recorder

```text
请使用 magic-recorder，把下面这段口述整理成个人 Markdown 思考记录：
...
```

适合：

- 口述整理
- 语音转写稿整理
- Get 笔记内容整理
- 粗糙想法沉淀成 Markdown

### magic-kb-compiler 写入 Obsidian

```text
请使用 magic-kb-compiler，把这份材料编译成 Obsidian 知识资产。
目标知识库路径是：...
```

适合输出：

- `raw/` 原始材料
- `cards/` 原子卡片
- `wiki/` 主题页面
- `views/` 问题池、选题池、待办视图
- `logs/` 编译日志

### magic-kb-compiler 导出给 ima

```text
请使用 magic-kb-compiler，把这份材料整理成 ima 可导入的 Markdown 知识包。
不要写入 Obsidian，保留来源、摘要、主题和导入说明。
```

适合输出：

- Markdown 文档
- 分主题知识条目
- 来源摘要
- 导入说明

## Get 笔记接入

本仓库不安装也不复制 Get 笔记官方 Skill。

Get 笔记在这里只是可选输入源。需要读取 Get 笔记时，按官方文档配置外部能力：

- https://www.biji.com/openapi?tab=docs
- https://www.biji.com/openapi?tab=skill

常见配置包括：

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

如果 vault 路径变化，请在使用 Skill 时明确告诉 Agent 当前 `magic-ai-kb` 路径。

### ima 模式

ima 是导入包目标，不直接套用 Obsidian 的文件结构。

使用 ima 模式时，Skill 应输出平台友好的 Markdown 知识包，并明确：

- 来源材料
- 摘要
- 主题条目
- 导入方式
- 是否保留 raw 原文
