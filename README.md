# Knowledge Base Engineering Skill

把一个 Markdown / Obsidian / Notion / RAG 知识库，按《知识库工程学》的规则做**可测量、可复现、可回滚、可交接**的治理。

它不是“知识库整理助手”。它先诊断，再给方案；默认只读；所有写入必须经过授权；物理删除永远不在 AI 权限集合内。

## 1. 安装

把整个 `knowledge-base-engineering/` 目录复制到你的 Agent 技能目录，或作为项目级 Skill 加载。

最低要求：Python 3.10+，只用标准库，无第三方依赖。

```bash
cd knowledge-base-engineering
python3 tests/run_tests.py
```

## 2. 快速开始

```bash
# 只读清点
python3 scripts/inventory.py <库根> --json

# 元数据 / 占位 / 链接
python3 scripts/metadata_audit.py <库根> --json
python3 scripts/placeholder_audit.py <库根> --json
python3 scripts/link_audit.py <库根> --json

# 验证报告口径
python3 scripts/report_validate.py <report.json>
```

默认不写库。需要变更时：

1. 先生成 `templates/change-plan.md`；
2. 人看“改什么 / 证据 / 回滚”；
3. 签字后由受控工具执行；
4. 用独立脚本复验。

## 3. 目录

```text
knowledge-base-engineering/
├── SKILL.md               # 主入口：路由、状态机、权限、交付
├── references/            # 按需加载的权威规则
├── templates/             # 健康报告、变更计划、退役、口径披露、事故
├── scripts/               # 确定性只读扫描
├── adapters/              # 文件系统 / Obsidian / Notion / RAG
├── config/                # 规则版本、指标、权限、适配
├── tests/                 # 9 个异常样本 + 回归测试
├── CHANGELOG.md
├── README.md
└── LICENSE
```

## 4. 设计边界

- 规则单一来源：G0–G7、L0–L7、体检 12 项、口径四问只在 references/config 定义一次。
- 主入口不堆整本书：`SKILL.md` 负责路由，细节按需加载。
- 脚本只做确定性检查，不判断知识价值。
- 平台差异放 adapters，不改核心规则。
- 测试不仅测成功路径，还测权限越界、恶意注入、只读保证。

## 5. 安全模型

- 默认只读；写入默认关闭。
- 软归档、移动/批量重命名、基线调整、跨域写入必须人工签字。
- 物理删除：AI 永远不执行；只输出候选清单。
- 提示词不能代替工具权限；部署时先只挂只读工具。

## 6. 已知限制

- 扫描器是启发式，不解析 Dataview / Canvas / Notion 全部属性。
- 孤岛是原始无入链列表，日记/归档/uWise/出版等豁免必须人工分类。
- 跨库引用、块引用、标题级断链需人工抽检。
- 未在真实 10k 库上做性能基准；fixture 测试证明流程与权限，不证明生产规模。

## 7. 版本

- v1.0.0：主入口、8 个参考、5 个模板、6 个脚本（含安全 scaffold）、4 个适配器、9 个异常样本、21 项回归测试。

规则修订后先跑 `tests/run_tests.py`，再更新 `CHANGELOG.md` 与 `config/skill.yaml` 的版本。
