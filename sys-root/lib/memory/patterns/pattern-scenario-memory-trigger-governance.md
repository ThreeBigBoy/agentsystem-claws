---
type: pattern
title: 场景与记忆/检查清单的触发式执行保障
change-id: sys-rules-memory-refactor-v2-4
tags: [rules, governance, memory, execution-guarantee, scenario-trigger]
applicable-projects: [agentsystem]
host-scope: [cursor, vscode, generic]
related:
  - memory/patterns/pattern-rules-and-memory-evolution-governance.md
  - memory/patterns/pattern-iteration-log-enforcement-and-usage.md
  - memory/patterns/pattern-openspec-change-workflow.md
  - memory/patterns/pattern-openspec-scripts-and-spec-for-tooling.md
---

# 场景与记忆/检查清单的触发式执行保障

## 背景与目标

「检查并同步 README/快速开始/SOP」只是**一种**场景下的执行保障；治理体系中存在多种**治理关键场景**，若仅靠临时记忆或用户提醒，容易遗漏。本模式定义一套**通用机制**：为每类场景绑定「触发条件」与「必读 memory / 必做 checklist」，使正确行为由**结构化的场景→记忆/清单绑定**保障，而不是依赖外部提醒。

## 通用原则

1. **场景**：任一在治理上敏感、易漏或易错的行为（如改规则、记迭代日志、写 runtime-logs、新建变更、判定 simple/heavy、新增 memory、提交前 review 等）。  
2. **触发**：当主 Agent 或执行方**进入该场景**（由任务类型、正在编辑的文件、或阶段判断）时，在**执行关键动作前**应加载对应的 memory 或执行对应的 checklist。  
3. **绑定**：在规则或 Agent 文档中**显式写出**「当 X 时，必须先读 Y / 必须执行 Z」，使绑定可被检索、可维护；新增场景时，在本模式的「场景→绑定表」与对应触发点同步更新。

## 场景 → 必读 memory / 必做 checklist 绑定表

| 场景 | 触发条件（何时进入） | 必读 / 必做 | 触发写入位置（谁要求执行） |
|------|----------------------|-------------|----------------------------|
| **修改规则层文件** | 本次任务涉及修改 `global-rules/*.md`、`agents/*.md`、`skills-rules-for-agent.md` | 必须先读 `memory/patterns/pattern-rules-and-memory-evolution-governance.md` 并按其中 checklist 执行（含 change-id 挂载、`openspec/changes/[change-id]/` 下留痕、项目日志、README/新用户快速开始/宿主 SOP 审视） | `.cursor/rules/agent.mdc` |
| **任务启动（任一任务）** | 每次收到用户任务指令并完成 simple/heavy 判定后 | 主动记忆唤醒：按任务类型与上下文检索并按需加载相关 memory（见 `agents/主Agent.md` 第 7 条与关键 memory 列表），遵守一跳克制 | `agents/主Agent.md` 第 7 条 |
| **迭代日志记录/收尾** | 在 change-id 上下文中完成 Agent/技能调用，即将作出完成性/交付性回复前 | 收尾前须自检已追加迭代日志；**heavy 模式或易漏场景下**建议先读 `pattern-iteration-log-enforcement-and-usage.md` 与 `anti-pattern-missing-iteration-log-in-agent-calls.md` 再执行收尾 | `projects-rules-for-agent.md` 第三章、`agents/主Agent.md` 收尾 |
| **写入 runtime-logs 前** | 决定向 runtime-logs 追加 model-calls 或 system-events 前 | 应先读 `pattern-runtime-logs-usage-playbook-for-agents.md` 与 `anti-pattern-runtime-logs-business-data-pitfall.md`，确保不混入业务/敏感数据、粒度符合约定 | `agents/主Agent.md` 运行日志与长期记忆段 |
| **新建 OpenSpec 变更 / 新建 change-id** | 用户发起新需求、新建变更或迭代，第一步执行前 | 必须先读 `OpenSpec.md` 第六节与 4.3 节，以及 `memory/patterns/pattern-openspec-change-workflow.md`，再建 docs/project-prd-changes 与 openspec/changes；**若变更产出含脚本/工具**，须另读 `memory/patterns/pattern-openspec-scripts-and-spec-for-tooling.md`，按其中约定：脚本放在项目根 `scripts/` 下子目录（.py + README），且对归属的 capability 建 `openspec/changes/[change-id]/specs/[capability]/spec.md` 增量 | `projects-rules-for-agent.md` 2.1 |
| **simple/heavy 判定** | 每次收到任务指令，做复杂度判定时 | 按 `projects-rules-for-agent.md` 1.6 执行；需操作化细节时读 `pattern-task-complexity-judgement-and-mode-switch.md` | `projects-rules-for-agent.md` 1.6、`agents/主Agent.md` 第 4 条 |
| **模型/配额选择** | 需要选择模型层级或做额度决策时 | 按 `projects-rules-for-agent.md` 第六章；需策略细节时读 `pattern-model-tiering-and-quota-governance.md` | `projects-rules-for-agent.md` 第六章 |
| **新增 memory 条目** | 决定沉淀长期记忆并调用 create_memory_entry 或手写 memory 前 | 必须先读 `memory/schema.md`，遵守 `related`、正文「关联模式」与克制机制（3～5 条 related、一跳加载） | `agents/主Agent.md` 长期记忆沉淀段 |
| **提交/合并前 review（规则或治理相关变更）** | 对涉及 rules、agents、memory/schema、入口 mdc 的变更做 review 时 | 检查：rules 是否仅结论级 HOW、对应 SKILL/memory 是否已更新、README/新用户快速开始/宿主 SOP 是否需同步并已在 `openspec/changes/[change-id]/`（或项目约定的变更记录路径）中记录；可复用 pattern-rules-and-memory-evolution-governance 中的审视项 | 本 pattern、pattern-rules-and-memory-evolution-governance |
| **变更实施前方案评审** | 用户或主 Agent 要求在按 tasks.md 实施前对变更做方案详细评审（查缺补漏）时 | 必须先读 `memory/patterns/pattern-change-pre-implementation-review.md`，并按其中步骤执行：OpenSpec 6.2 符合性、规则/记忆审视、四维方案评审、文档间一致性、任务统计一致；产出评审记录至 `docs/project-prd-changes/[change-id]/records/`，同步更新方案细节 | 本 pattern；主 Agent 执行评审时加载 |
| **变更完整落地复盘 / 沉淀方法论为 memory** | 用户要求对某 change-id 做「复盘」「总结方法论」「转化为 memory」或变更已从方案到 code review 全阶段完成需沉淀经验时 | 先读 `memory/reflections/reflection-change-full-lifecycle-migrate-langgraph.md` 与 `memory/patterns/pattern-change-full-lifecycle-delivery.md`，按复盘阶段梳理决策与可复用做法，再按 `memory/schema.md` 与「新增 memory 条目」场景沉淀为 reflection/pattern；related 控制在 3～5 条，并视需在本表补充「变更完整落地」类触发 | 本 pattern；主 Agent 执行复盘时加载 |
| **新用户/新环境安装或启动 LangGraph 后端** | 用户询问如何在新机器或新环境安装依赖、解决「未安装 langchain-openai」或如何配置并启动 LangGraph 后端时 | 先读 `新用户快速开始.md` §5.1、§5.2 与 `memory/playbooks/playbook-langgraph-backend-quickstart.md`，按步骤执行：agent_team_project 下 `bash setup-langgraph-env.sh` 或 `pip install -r requirements.txt`；.env 配置 OPENAI_API_KEY；AGENT_TEAM_PROJECT_ROOT + uvicorn 启动 | 本 pattern；主 Agent 回答环境/启动类问题时加载 |
| **LangGraph 后端就绪检查（执行前环境自检）** | 用户明确要求「检查环境」「环境是否启动」时，或即将通过 MCP 执行 `run_langgraph`/变更任务、或任务上下文涉及 agent_team_project/langgraph_backend 且可能调用后端时 | 先执行 GET localhost:8000/health 检查；若返回 200 且含 healthy 则视为就绪；若不可用则提示用户先启动后端并引用 `memory/playbooks/playbook-langgraph-backend-quickstart.md` 与 `memory/patterns/pattern-langgraph-backend-readiness-check.md`，不代替用户执行启动 | 本 pattern；主 Agent 在调用 run_langgraph 或回答环境检查时加载 |
| **执行 OpenSpec 变更归档** | 用户或主 Agent 准备对已闭环的 change-id 执行 OpenSpec CLI 归档时 | 必须先读 `memory/patterns/pattern-openspec-archive-and-specs-sync.md`，按情形选择 `archive --yes` 或 `archive --skip-specs --yes`，归档后按需手动合并 ADDED 到 `openspec/specs/`、追加迭代日志；可选落实 Minor 与文档/memory 收尾 | 本 pattern；主 Agent 执行归档时加载 |
| **配置或排查 LangGraph 多业务项目 / 新管线留痕** | 用户配置 LANGGRAPH_WORKSPACE_PROJECTS、多项目取错、或询问「为何没有执行记录」「agent_decision/feedback/log 为空」时 | 先读 `memory/patterns/pattern-langgraph-mcp-multi-workspace-config.md`（配置范式：单 key JSON 数组、按 change_id 解析、本仓优先）与 `memory/patterns/pattern-new-pipeline-trace-vs-design-documents.md`（留痕在 runtime-logs/langgraph-runs/，不依赖 docs/project-prd-changes 与旧三件）；排查无记录时看 runtime-logs/langgraph-runs/ | 本 pattern；主 Agent 回答配置/留痕/排查时加载 |

## 使用说明

- **主 Agent**：在任务启动时通过「主动记忆唤醒」覆盖与当前任务匹配的场景；在进入上表某场景时，按「触发写入位置」找到对应规则或 主Agent 段落，执行其中要求的「必读/必做」。  
- **维护者**：新增治理关键场景时，应 (1) 在本表增加一行；(2) 在对应触发位置（agent.mdc、主Agent.md 或 projects-rules）写入「当 X 时须先读 Y / 须执行 Z」，保证自动化保障不依赖临时记忆。

## 关联模式

- 改规则层时的完整 checklist 与 README/SOP 审视见 `pattern-rules-and-memory-evolution-governance.md`。  
- 迭代日志的强制要求与自检见 `pattern-iteration-log-enforcement-and-usage.md` 与 `anti-pattern-missing-iteration-log-in-agent-calls.md`。  
- OpenSpec 变更流程见 `pattern-openspec-change-workflow.md`。  
- LangGraph 后端就绪检查（用户要求检查环境或执行 run_langgraph 前）见 `pattern-langgraph-backend-readiness-check.md`，未就绪时引用 `playbook-langgraph-backend-quickstart.md`。
