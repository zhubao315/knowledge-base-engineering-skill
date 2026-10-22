<div align="center">

# Knowledge Base Engineering

**知识库工程治理 · 通用 AI Skill**

把知识库当成一套持续运行的信息系统来治理，  
而不是替用户整理几篇笔记。

![version](https://img.shields.io/badge/version-1.1.0-blue)
![tests](https://github.com/zhubao315/knowledge-base-engineering-skill/actions/workflows/tests.yml/badge.svg)
![license](https://img.shields.io/badge/license-MIT-green)
![python](https://img.shields.io/badge/python-3.10%2B-3776AB)
![mode](https://img.shields.io/badge/mode-read--only--first-orange)

[快速开始](#快速开始) · [安全模型](#安全模型) · [仓库结构](#仓库结构) · [测试](#测试) · [边界](#当前边界)

</div>

---

> [!IMPORTANT]
> **默认只读。** 写入默认关闭；软归档、移动、基线调整、跨域写入必须人工签字；**物理删除永远不在 AI 权限集合内**。

## 这是什么

一个可迁移的、可测试的知识库工程 Skill。

它不替用户判断“什么值得留”，而是把事实、证据、方案和边界交给人类：先诊断，再治理；先保护原件，再处理副本；没有授权不写入，没有证据不报完成。

方法来自《知识库工程学》的 13 章工程架构与 5 个附录，但这个仓库是**独立可运行的包**，不依赖书稿正文。

```text
诊断 → 准入 → 消化 → 治理 → 度量 → 运营 → 交付
```

## 它能做什么

| 模块 | 作用 | 主要输出 |
|---|---|---|
| 01 健康诊断与基线 | 清点、元数据、内容、引用、重复、占位 | `health-report.md`、`baseline.json` |
| 02 准入防火墙 G0–G7 | 格式、连接、注水、重复、时效、索引、正本、事实 | `admission-report.md`、`rejected-items.json` |
| 03 消化与分级 L0–L7 | 判断内容停在“文件”还是已经“能用” | 分级清单、候选正本、去向台账 |
| 04 语义拓扑 | 孤岛、断链、重复正本、语义连接 | `link-audit.json`、`link-repair-plan.md` |
| 05 度量与独立审计 | 指标定义、排除项、版本、基线、复算 | `metric-registry.yaml`、审计报告 |
| 06 安全归档与恢复 | 非知识资产、备份副本、软归档、回滚 | `retirement-plan.md`、事故记录 |
| 07 持续运营与 90 天 | 周任务、月审计、季复测、阶段验收 | `operations-runbook.md`、`90-day-plan.md` |
| 08 AI 上下文 | 给 RAG / Agent 提供带来源、版本、权限的上下文 | `context-pack.md`、`source-manifest.json` |

八个模块共享同一套指标注册表、权限策略、文件身份规则和审计机制。模块是功能边界，不是八套规则。

## 快速开始

### 1. 作为 Agent Skill 加载

把整个目录复制到你的 Agent 技能目录，或作为项目级 Skill 加载。

```bash
git clone https://github.com/zhubao315/knowledge-base-engineering-skill.git
cd knowledge-base-engineering-skill
python3 tests/run_tests.py
```

预期：

```text
25 passed, 0 failed
```

### 2. 先探测环境，再决定建库方式

```bash
python3 scripts/detect_environment.py --json
```

- 沙箱共享库可达：可以生成镜像/同步计划，但实际同步交给外部工具并由人批准。
- 本地不可达：**不要**把 `/app/.hermes/obsidian` 当默认路径；按本地独立库处理。

### 3. 只读扫描一个现有库

```bash
python3 scripts/inventory.py <库根> --json
python3 scripts/metadata_audit.py <库根> --json
python3 scripts/placeholder_audit.py <库根> --json
python3 scripts/link_audit.py <库根> --json
```

默认不写任何文件。发现问题也不直接改原件。

### 4. 安全创建新 Obsidian 库

```bash
# 默认 dry-run：只打印计划，不落盘
# profile auto：本地→para，沙箱→ulife
python3 scripts/scaffold_obsidian.py --target ~/new-vault

# 确认后执行
python3 scripts/scaffold_obsidian.py --target ~/new-vault --execute
```

规则：

- 目标必须是**不存在或空目录**；
- 非空目录直接拒绝；
- 不覆盖、不移动、不删除；
- 写 `00-META/scaffold-manifest.json`；
- 不创建 `.obsidian/` 配置，Obsidian 打开后自己生成。

三个 profile：

| profile | 创建什么 | 适合 |
|---|---|---|
| `para` | `00-Inbox / 01-Projects / 02-Areas / 03-Resources / 04-Archives` | 本地默认，直觉最好 |
| `minimal` | `00-META / 01-BRAIN / 02-BUILD / 07-SOURCES / 09-REFERENCE / 99-归档` | 先跑通一个最小库 |
| `ulife` | 在 minimal 上补 `11-概念 / 12-模型 / 13-框架 / 14-原则 / 15-洞察`、`22-uSkill`、`28-创作`、`74-影音`、`93-脚本` | 沙箱默认 / 想按 uLife 分层起步 |

### 5. 验证报告证据

```bash
python3 scripts/report_validate.py <report.json>
```

`PASS` 必须带 `timestamp`、`scope`、`method`；缺一项就退回草稿。

## 安全模型

| 操作 | AI 默认 | 要求 |
|---|---|---|
| 只读扫描、检索、统计 | ✅ 允许 | 范围明确，记录范围 |
| 生成治理建议 / 差异清单 | ✅ 允许 | 不修改原件 |
| 草稿区生成候选 | ✅ 允许 | 与正本隔离，标来源 |
| 写入正式知识库 | ⛔ 默认禁止 | 明确授权 + 受控工具 |
| 移动 / 批量重命名 | ⛔ 不允许自动 | 变更计划 + 人工确认 |
| 软归档 | ⛔ 不允许自动 | 人工批准 + 恢复路径 |
| 基线 / 阈值调整 | ⛔ 不允许自行 | 提案 + 版本记录 |
| 跨域写入 | ⛔ 默认禁止 | 范围、目标、期限 |
| **物理删除** | **绝对禁止** | 不向 AI 暴露删除工具 |

> [!WARNING]
> 提示词不能代替工具权限。如果底层 Agent 仍持有删除工具，写“不要删”不等于安全。

五种状态：

`PASS` · `FAIL` · `NOT_RUN` · `BLOCKED` · `NEEDS_REVIEW`

**`NOT_RUN` 和 `BLOCKED` 不得计入 `PASS`。**

## 仓库结构

```text
knowledge-base-engineering/
├── SKILL.md               # 主入口：S0–S7 状态机、权限、交付
├── references/            # 9 份权威规则
├── templates/             # 5 份标准交付物
├── scripts/               # 7 个脚本：6 个只读 + 1 个安全 scaffold
├── adapters/              # 文件系统 / Obsidian / Notion / RAG
├── config/                # 规则版本、指标、权限、适配
├── tests/                 # 9 个异常样本 + 25 项回归测试
├── CHANGELOG.md
├── README.md
└── LICENSE
```

## 测试

9 个 fixture 覆盖：

- 缺 frontmatter
- 缺 title
- 断链
- 原始孤岛
- 占位 / 空标题
- 归档与附件排除
- 提示注入（只当数据，不执行）
- scaffold：dry-run 不落盘、execute 创建、拒绝非空目录、ulife 分层、环境探测、auto 本地 PARA / 沙箱 uLife

当前结果：

```text
25 passed, 0 failed
0 fixture files changed
0 deletes
```

> 这是 fixture 测试，不是 10k 库生产基准。真实库的召回率、误报率、耗时，仍需在你自己的库上建立基线。

## 设计原则

| 原则 | 行为 |
|---|---|
| 可测量 | 每个指标带定义、范围、单位、时点、算法 |
| 可复现 | 相同数据、规则版本、脚本可复跑对照 |
| 可回滚 | 修改前保留备份、差异或版本记录 |
| 可交接 | 报告、变更记录、未解决问题、下次复测日 |
| 先诊断，再治理 | 默认只读；先出证据，再出方案 |
| 先搬价值，再退役 | 合并 / 归档前确认价值去向与恢复路径 |
| 人类保留最终控制权 | 不可逆动作停在签字点 |
| 不自证 | AI 不用自己的报告证明自己跑过 |

## 环境自适应

初始化不再假设 `/app/.hermes/obsidian` 一定存在：

```bash
python3 scripts/detect_environment.py --json
```

- `sandbox`：可生成镜像计划；实际同步由外部工具执行，必须人工批准。
- `local`：切换到本地独立库，默认 `para`；绝不把沙箱路径当默认值。
- `scaffold_obsidian.py --profile auto` 自动选择：本地 → `para`，沙箱 → `ulife`。

详见 `references/environment.md`。

## 当前边界

- 扫描器是启发式：不解析 Dataview / Canvas / Notion 全部属性。
- 孤岛是原始无入链列表；日记 / 归档 / uWise / 出版等豁免必须人工分类。
- 跨库引用、块引用、标题级断链需人工抽检。
- Notion API、RAG 适配尚未实机联调。
- 未在 10k 库上做性能基准；fixture 只证明流程与权限，不证明生产规模。
- 不提供自动写入执行器；写入必须由受控工具与人签字完成。

## 版本

- **v1.1.0**：主入口、9 references、5 templates、7 scripts、4 adapters、9 fixtures、25 tests；新增环境探测与 `para` profile。
- 规则修订后先跑 `tests/run_tests.py`，再更新 `CHANGELOG.md` 与 `config/skill.yaml`。

## License

[MIT](LICENSE) © 2026 朱宝

---

<div align="center">

**收藏不是资产，架构与运营才是。**

先修尺子，再量库；先建闸门，再谈规模。

</div>
