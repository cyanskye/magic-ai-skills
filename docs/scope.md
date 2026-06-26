# 收录范围

本仓库只收录自己创建并稳定使用的 Magic AI 工作流 Skills。

## 当前收录

- `magic-recorder`
- `magic-kb-compiler`

## 不收录

- Get 笔记官方 Skill 或 Get 笔记 OpenAPI 适配层
- 第三方 Skills
- 系统内置 Skills
- 插件缓存 Skills
- 只是在本机安装过、但不是自己创建维护的 Skills
- 历史版本
- 真实密钥、cookie、token、私密笔记内容

## 判定规则

一个 Skill 进入本仓库，需要同时满足：

1. 是自己创建或长期维护的 Magic AI 工作流。
2. 当前版本稳定可用。
3. 与 Magic AI 记录、整理、知识库编译直接相关。
4. 依赖关系清楚。
5. 不包含真实凭据或私密内容。

外部服务只写依赖说明，不复制服务方 Skill。

## 兼容范围

知识库目标当前只兼容：

- Obsidian / Magic AI 知识库
- ima

运行环境尽量兼容：

- Codex
- Claude
- ima
- WorkBuddy
- OpenClaw
- Hermes

兼容的含义是：这些环境可以读取或迁移本仓库的 `SKILL.md` 规则；不是承诺每个平台都已有自动安装、自动导入或 API 写入能力。
