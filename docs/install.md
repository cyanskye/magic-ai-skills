# 安装说明

## Codex

```bash
mkdir -p ~/.codex/skills
cp -R skills/getnote ~/.codex/skills/
cp -R skills/magic-recorder ~/.codex/skills/
cp -R skills/magic-kb-compiler ~/.codex/skills/
```

## Claude

```bash
mkdir -p ~/.claude/skills
cp -R skills/getnote ~/.claude/skills/
cp -R skills/magic-recorder ~/.claude/skills/
cp -R skills/magic-kb-compiler ~/.claude/skills/
```

## Getnote 凭据

仓库不保存真实凭据。使用 `getnote` 时，在本机配置：

```bash
export GETNOTE_API_KEY="..."
export GETNOTE_CLIENT_ID="..."
export GETNOTE_OWNER_ID="..." # optional
```

也可以继续使用本机私有 `.env`，但不要提交到仓库。

