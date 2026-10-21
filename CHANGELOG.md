# Changelog

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
