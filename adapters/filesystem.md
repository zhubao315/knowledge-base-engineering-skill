---
title: "KBE Skill — Filesystem Adapter"
created: 2026-10-21
tags:
  - "项目/知识库维护"
  - "维度/技能"
  - "类型/参考"
---

# Filesystem Adapter

## 适用

普通 Markdown 目录、Git 仓库、静态站点内容。

## 映射

- 文件身份：相对库根路径 + 文件名。
- 双链：`[[note]]` / `[[path/note|alias]]`。
- 元数据：YAML frontmatter。
- 排除：`.git/`、`.obsidian/`、`.runtime/`、`.venv/`、`node_modules/`、`attachments/`、`archive/`（按库调整）。

## 命令

```bash
python3 scripts/inventory.py <root> --json
python3 scripts/metadata_audit.py <root> --json
python3 scripts/link_audit.py <root> --json
python3 scripts/placeholder_audit.py <root> --json
```

## 限制

- 不解析嵌入块、Canvas、数据库属性。
- 大小写敏感由文件系统决定。
- 符号链接不跟随，避免循环。
