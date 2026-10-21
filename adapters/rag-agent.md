---
title: "KBE Skill — RAG / Agent Adapter"
created: 2026-10-21
tags:
  - "项目/知识库维护"
  - "维度/技能"
  - "类型/参考"
---

# RAG / Agent Adapter

## 目标

把治理过的库变成可信上下文，而不是把整库塞进模型。

## 上下文包

每条内容至少带：

- `source`：正本路径 / URL
- `version`：文件版本或修改时间
- `scope`：域（USER / SYSTEM / SHARED / RUNTIME）
- `confidence`：原文 / 用户观点 / AI 推断 / 待验证
- `timestamp`：内容时点
- `permission`：可读 / 可引用 / 需脱敏

## 检索前

1. 先确认库范围与规则版本。
2. 过滤：断链、空壳、占位、无源镜像、越权域。
3. 优先正本；重复候选标注，不并列当事实。
4. 用口径四问检查数字；没有时点的数字标“未校验”。

## 输出

`context-pack.md` + `source-manifest.json` + 调用审计记录。

## 禁止

- 把 AI 推断写成原文事实。
- 把没有来源的内容伪装成可信知识。
- 用检索相似度代替正本判断。
- 让 Agent 直接删除/覆盖原件。
