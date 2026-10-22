---
title: "KBE Skill — Environment-Aware Initialization"
created: 2026-10-22
tags:
  - "项目/知识库维护"
  - "维度/技能"
  - "类型/参考"
---

# Environment-Aware Initialization

初始化知识库时，**先探测环境，再询问目标**。不要把某个绝对路径当成所有环境都存在的默认值。

## 1. 探测

```bash
python3 scripts/detect_environment.py --json
```

默认探测 `KBE_SANDBOX_ROOT`，未设置时用 `/app/.hermes/obsidian`。只检查 `exists`、`is_dir`、`readable`，不创建、不写入。

| 结果 | 环境 | 推荐 profile | 可选模式 |
|---|---|---|---|
| 路径可达 | `sandbox` | `ulife` | `mirror`（只出计划）/ `local` |
| 路径不可达 | `local` | `para` | `local` |

## 2. 分支

### 分支 A：沙箱共享库可达

- 可以提供“镜像/双向同步”的**计划**：源、目标、目录映射、排除项、冲突策略。
- 实际同步必须交给外部同步工具（rsync / Syncthing / Git 等），并由人批准；**本 Skill 不自动执行同步**。
- 不把共享库内容直接写进用户本地库；先出 `change-plan.md`。

### 分支 B：本地环境

- **绝不**把 `/app/.hermes/obsidian` 展示为默认路径。
- 默认给两个选项：
  1. 纯个人本地库：`para`（`00-Inbox` / `01-Projects` / `02-Areas` / `03-Resources` / `04-Archives`），或 `minimal` / `ulife`。
  2. 从用户明确提供的本地文件夹/压缩包迁移：先校验路径是否可读，只出迁移计划；不自动复制、不覆盖。
- 用户说不清路径时，给一个示例：`--target ~/notes`，不要替他猜。

## 3. 落盘

```bash
# 只探测，不写
python3 scripts/scaffold_obsidian.py --detect

# 本地：默认 para；也可 --profile minimal|ulife
python3 scripts/scaffold_obsidian.py --target ~/notes --execute

# 沙箱：默认 ulife
python3 scripts/scaffold_obsidian.py --target ~/notes --sandbox-root /app/.hermes/obsidian --execute
```

规则不变：默认 dry-run；目标必须不存在或为空；非空目录拒绝；不覆盖、不移动、不删除；不创建 `.obsidian/` 配置；写 `00-META/scaffold-manifest.json`。

## 4. 推荐话术

本地：

> 检测到当前处于本地环境，我们将初始化一个纯个人本地知识库。你希望创建在哪个本地路径？默认结构是 PARA（Inbox / Projects / Areas / Resources / Archives）；也可以选 uLife 分层或最小结构。

沙箱：

> 检测到共享库可达。你可以选择把它作为镜像源先生成同步计划，或只建一个本地独立库。镜像计划需要你确认源、目标和排除项；实际同步由外部工具执行。

## 5. 防呆

- 路径不可达时，不报“路径不存在”就结束；给本地替代方案。
- 目标非空时，不覆盖；列出现有文件，建议换目录或先备份。
- 没有写入权限时，标 `BLOCKED`，不假装创建成功。
- 不把“镜像计划”说成“已经同步”。
