---
title: "KBE Skill — Notion Adapter"
created: 2026-10-21
tags:
  - "项目/知识库维护"
  - "维度/技能"
  - "类型/参考"
---

# Notion Adapter

## 映射

- 文件身份：page ID + 标题；不要只用标题，标题会重名。
- 双链：page mention / relation 属性；不是 wikilink。
- 元数据：数据库属性（created、tags、status、source）。
- 排除：归档数据库、模板数据库、回收站。

## 注意

- API 能力取决于集成权限；没有读取权限时标 `BLOCKED`，不猜。
- Relation 反向检查可找“无入链”页面；但 relation 可能为空，需人工确认。
- 不自动修改数据库 schema；变更提案交人审批。
- 软归档用状态属性或归档数据库，不直接删除页面。

## 输出

页面清单、属性缺失、relation 断裂、无入链候选、重复候选；每条带 page ID 与 URL。
