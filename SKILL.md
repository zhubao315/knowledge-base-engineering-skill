---
name: knowledge-base-engineering
description: "知识库工程治理通用 Skill：按 OESA（Observe-Evaluate-Standardize-Apply）四阶段闭环，对一个 Markdown / Obsidian / Notion / RAG 知识库做可测量、可复现、可回滚、可交接的治理。默认只读诊断，先探测环境并按需降级；不直接修改知识库，物理删除永远不在 AI 权限集合内。"
version: "1.2.0"
license: "MIT"
title: "Knowledge Base Engineering — Skill"
created: 2026-10-21
updated: 2026-10-22
tags:
  - "项目/知识库维护"
  - "维度/技能"
  - "类型/框架"
  - "来源/项目"
---

# Knowledge Base Engineering

> 库的终点不是被收藏，而是在你开口时被调用；Skill 不是聊天框，而是 OESA 闭环的工程契约。

## 1. 这个 Skill 做什么

把知识库当成一套持续运行的信息系统来治理，而不是替用户整理几篇笔记。

它只做四件事：

1. **O-观测**：先看清环境、急症、体检 12 项与真实读数。
2. **E-评估**：用 G0–G7 与口径四问决定什么能进。
3. **S-固化**：用 L0–L7 把文件变成可调用资产；清理只做软归档候选。
4. **A-调用**：用四域权限与语义路由，把库接给人机共用，并在签字点停下。

它不替用户决定“什么值得留”，也不拥有物理删除权。它把事实、证据、方案和边界交给人类。

## 2. 触发语与适用边界

**使用**：

- “库乱了”“笔记体检”“初始化知识库”“这篇该不该入库”
- “断链太多”“孤岛怎么处理”“这条笔记消化了吗”
- “帮我定指标口径”“做一份 90 天治理计划”“复盘这次事故”
- “给 RAG / Agent 准备可信上下文”“把这个库封装成 Skill”

**不使用**：

- 单篇写作润色、翻译、无关问答
- 没有明确库范围的“帮我整理一下”
- 要求 AI 直接物理删除、绕过签字、批量覆盖正本
- 医疗、法律、财务等需要专业判断的最终结论

## 3. 第一步：环境预检（Environment Probe）

初始化、建库或第一次接触一座库之前，先做**只读**环境探测。不要假设某个绝对路径一定存在。

默认探测 `KBE_SANDBOX_ROOT`，未设置时用 `/app/.hermes/obsidian`；只检查 `exists` / `is_dir` / `readable`，不创建、不写入、不删除。

| 结果 | 分支 | 默认结构 | 推荐动作 |
|---|---|---|---|
| 沙箱路径可达 | 沙箱 / 团队库 | `ulife` | 只读扫描；可生成镜像/同步**计划**，实际同步交外部工具并需人批准 |
| 路径不可达 | 本地个人库 | `para` 或 `minimal` | 友好询问本地路径，初始化个人库；**绝不展示不可达路径** |
| 用户提供本地源 | 本地迁移 | 用户指定 | 校验可读，先出迁移计划；不自动复制、不覆盖 |
| 目标目录非空 | 拒绝覆盖 | — | 列现有文件，建议换目录或先备份 |

`--profile auto` 自动选择：本地 → `para`，沙箱 → `ulife`。`para` 是 `00-Inbox / 01-Projects / 02-Areas / 03-Resources / 04-Archives`；`minimal` 是最小可跑结构；`ulife` 是分层结构。三者都不创建 `.obsidian/` 配置。

本地降级话术：

> 检测到当前处于本地环境，我们将初始化一个纯个人本地知识库。你希望创建在哪个本地路径？默认结构是 PARA（Inbox / Projects / Areas / Resources / Archives）；也可以选 uLife 分层或最小结构。

沙箱可达也只出镜像计划；**Skill 不自动双向同步**。

## 4. OESA 总线路由

Skill 被触发后，不直接进入“整理”，按固定顺序流转：

| 段 | 名称 | 做什么 | 输出 | 停点 |
|---|---|---|---|---|
| 1 | **O-观测** | 环境预检、急症四联、只读扫描、体检 12 项 | 环境报告、体检底稿、异常清单 | 命中急症：只出应急四联，不进入体检 |
| 2 | **E-评估** | G0–G7、口径四问、质量门分开报 | 准入回执、拒收/挂起清单 | 不过门：只进收件箱；缺口径：标“未校验” |
| 3 | **S-固化** | L0–L7 定级、正本候选、软归档候选 | 分级清单、正本候选、软归档候选 | 物理删除不进入；软归档只出候选 |
| 4 | **A-调用** | 四域权限、语义拓扑、签字点、输出契约 | 路由计划、权限表、签字记录 | 无签字：动作停在建议 |

四段不是四个按钮，是一条总线：上一段的证据是下一段的输入，下一段的异常回到上一段。

## 5. 输入契约

每次任务先确认六项；缺项必须提问或降级，不能猜。

| 输入 | 必须明确 | 缺失时 |
|---|---|---|
| 环境 | 沙箱共享库 / 本地独立库 / 本地迁移源 | 静默探测；不可达则本地降级 |
| 知识库范围 | 根目录、include、exclude | 不推断全库；只分析明确范围 |
| 任务与验收 | 目标、对象、期望结果 | 只读任务给默认建议；写入先问 |
| 候选内容与证据 | 原文、来源、引用、文件身份 | 标缺失，不编造出处 |
| 权限边界 | 只读、提案、获批写入、禁止动作 | 未授权只读，只出方案 |
| 口径与规则版本 | 指标定义、阈值、排除项、版本 | 标“未校验”，不擅自沿用 |

## 6. S0–S7 状态机

| 状态 | 做什么 | 不通过时 |
|---|---|---|
| S0 识别任务与输入 | 确认环境、范围、目标、工具、权限、规则版本 | 缺项标 `BLOCKED` 或 `NEEDS_REVIEW` |
| S1 事故前置 | 正文丢失、批量误改、断链突增先走应急四联 | 不停手，不进入普通治理 |
| S2 只读扫描 | 清点、元数据、内容、链接、占位、基线 | 发现问题也不改原件 |
| S3 调用规则 | G0–G7 → L0–L7 → 拓扑 → 12 项 → 口径四问 | 规则冲突暂停，不自行拼接 |
| S4 生成方案 | 对象、证据、影响、去向、回滚、验收 | 默认只出计划 |
| S5 人工签字 | 改什么、证据是什么、出错怎么回滚 | 少一样，停在建议 |
| S6 受控执行与复验 | 执行日志、退出码、独立复算 | 新增断链/丢失即停 |
| S7 交付与运营 | 报告、差异、未解决问题、下次复测 | 没回写，不算闭环 |

S1 是硬前置。库正在流血时，不要继续做普通整理；先停手、留证、回滚、复验。

## 7. 权限与硬约束

| 操作 | AI 默认 | 要求 |
|---|---|---|
| 只读扫描、检索、统计 | 允许 | 范围明确，记录范围 |
| 生成治理建议/差异 | 允许 | 不改原件 |
| 草稿区生成候选 | 允许 | 与正本隔离，标来源 |
| 写入正式库 | 默认禁止 | 明确授权 + 受控工具 |
| 移动/批量重命名 | 不允许自动 | 变更计划 + 人工确认 |
| 软归档 | 不允许自动 | 人工批准 + 恢复路径 |
| 基线/阈值调整 | 不允许自行 | 提案 + 版本记录 |
| 跨域写入 | 默认禁止 | 范围、目标、期限 |
| 物理删除 | **绝对禁止** | 不向 AI 暴露删除工具 |

**绝对禁令：AI 绝不执行物理删除。清理产物仅限“软归档候选清单 / 已软归档，待人类签字”。** 没有“签字后可删”这条路径。

签字必须看到三样：改什么、证据是什么、出错怎么回滚。少一样，动作停在建议。

## 8. 输出与状态

四类交付物：

1. **体检报告**：查了什么、发现什么、哪些通过/未执行/受阻。
2. **治理动作清单**：证据、建议、优先级、风险、责任人、验收条件。
3. **归档与变更记录**：原位置、去向、授权、恢复路径、执行结果。
4. **口径披露与复验记录**：时点、范围、算法、排除项、日志、退出码、独立复算。

状态只能是：`PASS` / `FAIL` / `NOT_RUN` / `BLOCKED` / `NEEDS_REVIEW`。**`NOT_RUN` 和 `BLOCKED` 不得计入 `PASS`。**

## 9. 按需加载

按任务读，不要一次全塞进上下文：

- OESA 四阶段：`oesa-core/O-observe.md`、`oesa-core/E-evaluate.md`、`oesa-core/S-standardize.md`、`oesa-core/A-apply.md`
- 详细规则：`references/architecture.md`、`admission-gates.md`、`knowledge-lifecycle.md`、`health-metrics.md`、`topology.md`、`permissions.md`、`incident-response.md`、`operations.md`、`environment.md`
- 模板：`templates/health-report.md`、`change-plan.md`、`retirement-record.md`、`incident-report.md`、`metric-disclosure.md`
- 脚本：`scripts/inventory.py`、`metadata_audit.py`、`link_audit.py`、`placeholder_audit.py`、`report_validate.py`、`detect_environment.py`、`scaffold_obsidian.py`
- 平台适配：`adapters/`
- 配置：`config/`

规则冲突时不得自行拼接或默默覆盖：记录冲突、暂停受影响操作，交规则所有者确认。

## 10. 快速开始

```bash
# 1. 环境探测（只读，不写库）
python3 scripts/detect_environment.py --json

# 2. 只读清点
python3 scripts/inventory.py <库根> --json

# 3. 元数据 / 占位 / 链接扫描
python3 scripts/metadata_audit.py <库根> --json
python3 scripts/placeholder_audit.py <库根> --json
python3 scripts/link_audit.py <库根> --json

# 4. 验证报告口径
python3 scripts/report_validate.py <report.json>

# 5. 安全创建新库（默认 dry-run；只允许新目录/空目录）
# profile auto：本地→para，沙箱→ulife
python3 scripts/scaffold_obsidian.py --target <new-or-empty-dir>
python3 scripts/scaffold_obsidian.py --target <new-or-empty-dir> --execute

# 6. 回归测试
python3 tests/run_tests.py
```

默认只读。需要写入时，先出 `templates/change-plan.md`，经人签字后再用受控工具执行。

## 11. 最终原则

```text
收藏不是资产，架构与运营才是。
先修尺子，再量库。
先保护原件，再治理副本。
没有证据，不报完成。
没有授权，不执行变更。
物理删除永远不属于 AI 的执行权限。
```

版本与变更见 `CHANGELOG.md`；安装与测试见 `README.md`。
