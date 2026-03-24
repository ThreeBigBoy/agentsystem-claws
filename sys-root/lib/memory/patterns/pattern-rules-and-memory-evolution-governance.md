---
type: pattern
title: 规则与记忆协同演进治理模式
change-id: sys-rules-memory-refactor-v2-4
tags: [rules, governance, memory, evolution]
applicable-projects: [agentsystem]
host-scope: [cursor, vscode, generic]
related:
  - memory/patterns/pattern-iteration-log-enforcement-and-usage.md
  - memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md
  - memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md
---

# 规则与记忆协同演进治理模式

## 背景

- `agentsystem` 将治理内核拆分为：  
  - 规则层：OpenSpec、`global-rules/*.md`、`agents/*.md`、`skills-rules-for-agent.md`；  
  - 技能与实现层：`skills/*/SKILL.md` 与运行后端；  
  - 记忆层：`memory/` 下的 patterns / anti-patterns / reflections / preferences / playbooks 等。  
- V2.4.2 开始，要求规则层 **只回答「谁/何时/必须做什么」和结论级 HOW**，执行细节与经验沉淀统一由 SKILL 与 memory 承接。

本条目给出一套可复用的「规则 × 记忆协同演进」模式，避免后续演进时把 HOW 再次堆回 rules，或忘记补齐对应的 SKILL/memory/adapter。

## 模式一：规则只管 When / Who / Must + 结论级 HOW

1. **规则文件职责**  
   - 明确：角色与职责（Who）、时机与流程骨架（When）、必须动作与红线（Must）；  
   - 为每个必须动作给出**最小可执行 HOW 结论**：  
     - 写到哪（路径）；  
     - 至少要包含哪些字段/元素；  
     - 在什么时机执行（例如「完成性回复前」）。  
   - 所有更细的 HOW（步骤、示例、脚本、模版等）不放在 rules，而是放到 SKILL/memory。

2. **记忆与 SKILL 职责**  
   - SKILL：定义特定能力在某角色下的执行步骤、注意事项与产出结构（How to do）；  
   - memory：沉淀跨 change-id / 跨项目可复用的模式、反模式、反思与剧本（经验与案例），不重复硬规则。

## 模式二：改 rules 前先看 SKILL/memory

### 自检 checklist（建议写入 `openspec/changes/[change-id]/` 变更留痕与 review 流程）

当需要修改 `global-rules/projects-rules-for-agent.md` 或其它治理 rules 时，按以下顺序自检：

1. **这是新的「红线/必须动作/时机」吗？**  
   - 是：可以考虑改 rules（新增或调整 Must 级规则）。  
   - 否：很可能只是 HOW 或示例，应优先改 SKILL/memory。

2. **这是结论级 HOW 还是过程级 HOW？**  
   - 结论级 HOW：可以在 rules 中以 1–2 行形式存在（例如「必须向 X 路径追加一行，至少包含 A/B/C 字段」），并**必须**给出指向的 SKILL/memory 路径。  
   - 过程级 HOW：只能写入 SKILL（步骤、字段细节）或 memory（模式/反模式/反思/剧本），不得写到 rules 中。

3. **对应 SKILL / memory 是否已存在？**  
   - 若没有：先在 `skills/*/SKILL.md` 或 `memory/patterns/*` / `memory/anti-patterns/*` / `memory/reflections/*` 中补齐，再在 rules 中写结论级 HOW 与索引；  
   - 若已存在：更新 SKILL/memory 以反映最新实践，然后在 rules 中仅更新结论级表述与路径。

## 模式三：在设计与记录层面留痕

1. **挂载 change-id**  
   - 所有涉及规则层变更（特别是 `projects-rules-for-agent.md`）的改动，须挂在某个 change-id 下（如 `sys-rules-memory-refactor-v2-4`）。  

2. **在 docs/project-prd-changes/[change-id]/records/ 中记录一次「规则 × 记忆协同演进」说明**  
   - 简要回答：  
     - 本次是否先检查/补齐了对应的 SKILL 与 memory；  
     - rules 中新增/修改部分是否仅为结论级 HOW；  
     - 是否在 rules 中写明了指向的 SKILL/memory 路径。

3. **在迭代日志中追加一条记录**  
   - 按 `projects-rules-for-agent.md` 第三章约定，为本次 change-id 的规则改动追加一条迭代日志，说明：  
     - 角色（主 Agent）、涉及的规则文件、是否影响执行流程；  
     - 是否建议其他项目按同样模式更新。

4. **审视是否需要同步更新 README / 快速开始文档 / 宿主 SOP**  
   - 当**规则层或入口层**发生影响用户理解或初始化方式的调整时，应执行本审视。适用变更包括但不限于：  
     - `global-rules/*.md`、`agents/*.md`、`skills-rules-for-agent.md` 的修改；  
     - **`agents/*.md`、`.cursor/rules/*.mdc`、根 `AGENTS.md`、`memory/schema.md`** 等入口与治理说明文档的修改（如主动记忆唤醒、改规则必走 checklist、memory 克制机制等）。  
   - 检查项：  
     - 根 `README.md` 中对规则层职责、版本演进、加载策略与记忆唤醒/执行机制的描述是否需要更新；  
     - `新用户快速开始.md` 是否需要补充/修正对规则瘦身、simple/heavy 加载、memory 联动与克制、改规则 checklist 的说明；  
     - 各宿主的初始化 SOP 与 adapter README 是否需要同步调整默认加载顺序或注意事项。  
   - 若需要更新，应将相关文档一并纳入本 change-id 的变更说明（如 `openspec/changes/[change-id]/` 内 tasks/proposal 更新记录）中，便于后续复盘。

## 与宿主 adapter 与运行后端的关系

- 在各宿主的 `platform-adapters/*/README.md` 与运行后端 `agent_team_project/README.md` 中，推荐：  
  - 用一小段说明遵循何种「rules × SKILL × memory」加载顺序（如 V2.4.2 中的 simple/heavy 渐进式加载）；  
  - 对 heavy 模式下如何自动拉取 SKILL/memory 做简要说明；  
  - 明确 adapter 与 backend 不改变治理层规则，只负责具体实现。

## 适用范围

- 所有直接使用本仓库作为 OpenSpec / 多 Agent 治理内核的项目；  
- 所有在本仓库内对 `global-rules/*.md`、`agents/*.md` 与 `skills-rules-for-agent.md` 做修改的变更。  

通过遵循本模式，可以在长期演进中保持：  
- rules 简洁、稳定、可审计；  
- SKILL 与 memory 按需扩展、承载执行经验；  
- 不同宿主与运行后端在加载行为上保持一致。

## 关联模式

- 当你计划对 rules 层做调整（尤其是 `projects-rules-for-agent.md`、`agents/*.md`），建议联动阅读：  
  - `memory/patterns/pattern-iteration-log-enforcement-and-usage.md`：确保所有规则改动都有完备的迭代日志留痕；  
  - `memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md`：评估此次规则演进是否需要同步调整 runtime-logs 与 memory 的协作方式；  
  - `memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md`：在涉及运行成本/稳定性的规则变更中，设计合适的 runtime-logs 观测点。  
- 若在这些联动检查中发现大量 HOW 被堆在 rules 层或记忆条目缺失，应把本条目作为「规则 × 记忆协同演进」的起点，发起一个独立 change-id 做结构性治理。

