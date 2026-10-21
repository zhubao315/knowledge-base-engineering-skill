---
title: "KBE Skill — Architecture"
created: 2026-10-21
tags:
  - "项目/知识库维护"
  - "维度/技能"
  - "类型/参考"
---

# Architecture

## 1. 分层

| 层 | 负责 | 不负责 |
|---|---|---|
| `SKILL.md` | 任务路由、状态机、权限边界、交付规范 | 堆整本书全文 |
| `references/` | 权威规则、完整操作规程 | 自行改阈值 |
| `scripts/` | 确定性统计与验证 | 判断知识价值 |
| `adapters/` | 文件系统、笔记平台、AI 环境差异 | 改变治理原则 |
| `config/` | 可审计参数与版本 | 多处重复维护同一规则 |
| `tests/` | 证明规则正确、权限有效 | 只测成功路径 |

## 2. 主入口 + 八模块 + 共享内核

```text
S0 识别任务
  └─ S1 事故前置（应急四联）
      └─ S2 只读扫描
          └─ S3 调用规则
              ├─ 01 健康诊断与基线
              ├─ 02 准入 G0–G7
              ├─ 03 消化 L0–L7
              ├─ 04 拓扑
              ├─ 05 度量与审计
              ├─ 06 归档与恢复
              ├─ 07 运营与 90 天
              └─ 08 AI 上下文
                  └─ S4 方案 → S5 签字 → S6 执行/复验 → S7 交付
```

共享内核：配置与平台适配、权限策略、备份与回滚、审计日志、口径注册表、独立验收。

## 3. 目录

```text
knowledge-base-engineering/
├── SKILL.md
├── references/
├── templates/
├── scripts/
├── adapters/
├── config/
├── tests/
├── CHANGELOG.md
├── README.md
└── LICENSE
```

## 4. 规则版本

- 规则集版本：`config/skill.yaml` 的 `ruleset_version`。
- 指标版本：`config/metric-registry.yaml` 的 `version`。
- 书稿版本：与《知识库工程学》版本对应；书稿修订后，先改规则集、跑回归测试，再升 Skill 版本。
- 不允许各模块复制阈值；只引用 `config/metric-registry.yaml` / `references/health-metrics.md`。

## 5. 适配原则

- 通用层：原则、状态机、输入输出、权限。
- 适配层：路径、双链、数据库属性、检索接口。
- 平台差异不得污染核心规则；适配器只能翻译，不得改判定线。
