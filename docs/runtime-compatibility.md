# 运行环境兼容

本仓库里的 Skills 应尽量兼容国内外常见 Agent / AI 工作台，而不是绑定某一个工具。

## 目标环境

当前按这些环境做兼容说明：

- Codex
- Claude
- ima
- WorkBuddy
- OpenClaw
- Hermes

## 兼容层级

### 标准 Skill 模式

如果平台支持本地 Skills 目录或类似机制，直接安装：

- `skills/magic-recorder`
- `skills/magic-kb-compiler`

平台读取 `SKILL.md` 后，按里面的流程执行。

### 规则源模式

如果平台没有原生 Skills 机制，把本仓库当作规则源：

1. 让 Agent 读取对应 `SKILL.md`。
2. 根据任务需要读取 `references/` 下的补充说明。
3. 用平台自己的文件、浏览器、API 或命令能力执行。

### 降级模式

如果平台不能直接运行脚本或访问本机文件，只输出可人工操作的结果：

- 整理后的 Markdown
- ima 导入包
- Obsidian 文件清单
- 手动导入步骤

不要在没有实际写入动作时声称已经更新目标平台。

## 平台边界

- Codex / Claude：优先使用本机文件系统、shell、Git 和本地 Skills。
- ima：优先作为知识库目标，接收 Markdown 知识包或平台支持的导入格式。
- WorkBuddy / OpenClaw / Hermes：按可读取 `SKILL.md` 的 Agent 工作台处理；如果它们有自己的 Skill/Plugin 格式，只做格式适配，不改核心规则。

## 不做的事

- 不提交任何平台 token、cookie 或 `.env`。
- 不把平台私有 API 写成默认必需能力。
- 不把 Obsidian 的目录结构强行套到 ima。
- 不把 ima 的导入包说成已经自动写入平台。
