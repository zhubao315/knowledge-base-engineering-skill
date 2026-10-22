# Changelog

## 1.2.0 — 2026-10-22

- 新增 `oesa-core/`：`O-observe.md`、`E-evaluate.md`、`S-standardize.md`、`A-apply.md`，把 Skill 重构成 OESA 四阶段调度总线。
- `SKILL.md` 重写为轻量主入口：触发语、环境预检、OESA 总线、S0–S7、权限硬约束、按需加载。
- `README.md` 重写为新手入口：30 秒上手、Claude/Cursor/Gemini 安装、环境降级、安全模型、核心 4 件与工程增强件。
- `oesa-core/` 四个模块补齐体检 12 项、G0–G7、L0–L7、四域权限与签字点。
- `config/skill.yaml` 增加 `oesa_core` 映射，版本升至 1.2.0。
- 包内文件数 50 → 54；回归测试仍为 25 项。

## 1.1.0 — 2026-10-22

- 环境自适应初始化：新增 `scripts/detect_environment.py`，探测 `KBE_SANDBOX_ROOT`（默认 `/app/.hermes/obsidian`）是否可达。
- 本地分支新增 `para` profile（`00-Inbox / 01-Projects / 02-Areas / 03-Resources / 04-Archives`）；`--profile auto` 本地→para、沙箱→ulife。
- 新增 `references/environment.md`：沙箱镜像只出计划，实际同步交外部工具 + 人批准；本地不展示沙箱路径。
- `scaffold_obsidian.py` 增加 `--detect` / `--sandbox-root`；目标缺失时给本地路径建议，不报死。
- 测试从 21 增至 25：环境探测、auto 本地 PARA、auto 沙箱 uLife。
- GitHub homepage README + GitHub Actions（Python 3.10/3.11/3.12）。

## 1.0.0 — 2026-10-21

- 主入口 `SKILL.md`：S0–S7 状态机、五项输入、五状态、权限与证据规范。
- 8 个 references：架构、G0–G7、L0–L7、体检指标、拓扑、权限、事故、运营。
- 5 个模板：健康报告、变更计划、退役记录、口径披露、事故记录。
- 5 个只读脚本：inventory、metadata_audit、link_audit、placeholder_audit、report_validate。
- 1 个安全 provisioning 脚本：scaffold_obsidian；默认 dry-run，只允许新目录/空目录，拒绝覆盖与非空目录。
- 4 个适配器：filesystem、Obsidian、Notion、RAG/Agent。
- 4 个 config：skill、metric registry、policy、adapters。
- 9 个 fixture 文件 + 21 项回归测试：异常检出、报告校验、权限约束、只读保证、提示注入不执行、scaffold 空目录/拒绝覆盖。

## 未做

- 真实 10k 库性能基准。
- Notion API 实机联调。
- Dataview / Canvas / 块引用深度解析。
- 自动写入执行器（故意不提供；写入必须由受控工具与人签字完成）。
