---
title: "KBE Skill — Obsidian Adapter"
created: 2026-10-21
tags:
  - "项目/知识库维护"
  - "维度/技能"
  - "类型/参考"
---

# Obsidian Adapter

## 映射

- 双链：`[[note]]`、`[[note|alias]]`、`[[note#heading]]`。
- 元数据：YAML frontmatter（Properties）。
- 索引：`∑` / MOC 页、Dataview 查询、反向链接面板。
- 排除：`.obsidian/`、`.trash/`、`.runtime/`、附件目录、归档目录。

## 注意

- 别名、标题、块引用都可能成为合法目标；脚本当前以文件名/别名为主，复杂块引用需人工复核。
- `[[note#heading]]` 只要 `note` 存在即视为可达；标题级断链需人工抽检。
- 不改 `.obsidian/` 配置；不自动执行 Dataview 查询。
- 归档建议用目录 + frontmatter 标记；保留别名与原路径。

## 零代码替代

反向链接面板找无入链；搜索 `[[` 找链接；用 Dataview 按 `level` / `status` 分组。

## 新库 provisioning

`scripts/scaffold_obsidian.py` 可在**新目录或空目录**创建 starter vault：

```bash
# 默认 dry-run，只打印计划
python3 scripts/scaffold_obsidian.py --target <new-or-empty-dir> --profile ulife

# 确认后执行
python3 scripts/scaffold_obsidian.py --target <new-or-empty-dir> --profile ulife --execute
```

- `minimal`：00-META / 01-BRAIN / 02-BUILD / 07-SOURCES / 09-REFERENCE / 99-归档。
- `ulife`：在 minimal 上补 01-BRAIN 的 11-概念 / 12-模型 / 13-框架 / 14-原则 / 15-洞察，以及 02-BUILD/22-uSkill、02-BUILD/28-创作、07-SOURCES/74-影音、09-REFERENCE/93-脚本。
- 拒绝非空目录；不覆盖、不移动、不删除；写 `00-META/scaffold-manifest.json`。

它不创建 `.obsidian/` 配置，也不修改已有库；Obsidian 自己会生成配置。
