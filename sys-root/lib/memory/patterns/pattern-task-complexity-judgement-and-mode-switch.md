---
type: pattern
title: 任务复杂度判定与 simple/heavy 模式切换
change-id: sys-rules-memory-refactor-v2-4
tags: [rules, governance, task-complexity, mode-switch]
applicable-projects: [agentsystem]
host-scope: [cursor, vscode]
related:
  - memory/patterns/pattern-model-tiering-and-quota-governance.md
  - memory/patterns/pattern-openspec-change-workflow.md
---

# 任务复杂度判定与 simple/heavy 模式切换

## 背景与适用场景

- 适用所有采用 OpenSpec + `projects-rules-for-agent.md` 的项目。  
- 目标是在「保证治理质量」与「控制上下文成本/体验」之间取得平衡：  
  - 简单任务（simple）时不过度加载厚规则；  
  - 重规则任务（heavy）时确保完整遵守 OpenSpec 与 global-rules。

## 推荐做法（模式）

### 1. 判定流程（主 Agent 执行）

1. 收到用户任务指令后，主 Agent 先基于指令内容与当前上下文进行一次轻量判定：  
   - 是否触达 OpenSpec 文档/接口签名/数据结构/安全边界；  
   - 是否需要多 Agent × 多 Skill 的协作（需求分析、架构设计、实现、评审、验收等完整链路）；  
   - 是否与某个 change-id 的完整迭代强绑定。
2. 判定结果为：  
   - **heavy**：立即按 `projects-rules-for-agent.md` 与 `skills-rules-for-agent.md` 要求执行；  
   - **simple**：可暂不加载完整 rules，仅在需要时按章节或按主题补充加载。

> 规则来源：`global-rules/projects-rules-for-agent.md` 第 1.6 节。

### 2. 典型 heavy 判定信号

- 用户显式提到：  
  - 「根据某个 change-id 做方案/实现/验收」；  
  - 「按 OpenSpec/变更单完成本次交付」等。  
- 需要对 `openspec/changes/[change-id]/` 下的文档做新增或重要修改：  
  - `proposal.md`、`tasks.md`、`design.md`、`specs/*/spec.md`。  
- 改动会影响：  
  - 对外接口签名或数据结构；  
  - 权限、访问控制、安全边界；  
  - 金额/结算等高风险业务逻辑。  
- 需要调用明显属于专业子 Agent 职责范围的工作：  
  - PRD/需求说明、架构设计、核心实现、代码评审、功能验收等。

### 3. 典型 simple 判定信号

在下列条件同时满足时，一般可视为 simple：

- 只涉及单个或极少数文件的小改动；
- 不改变对外接口签名、数据库结构或安全边界；
- 更像一次性本地/工具类操作（如重命名、文案微调、注释补充）；
- 与 `openspec/`、`docs/project-prd-changes/[change-id]/` 等核心文档几乎无交集。

simple 模式下：

- 可主要依赖：  
  - `.cursor/rules/*.mdc` 中的轻量规则；  
  - 当前会话上下文与必要的规则片段；  
  - 相关 `memory/` 条目。  
- 不强制创建或修改 `openspec/changes/*`；  
- 是否写入迭代日志，按对项目长期脉络的价值判断。

### 4. simple → heavy 的动态切换

在执行过程中，如发现：

- 实际改动已经触达 OpenSpec 文档或对外接口；  
- 发现原先认为是「小修小补」的任务，背后有更大范围的结构/规则影响；

则必须：

1. 立即将本轮任务升级为 heavy；  
2. 在迭代日志或 runtime-logs 中记录「从 simple → heavy」的模式切换与简短理由；  
3. 自该点起补齐 heavy 模式要求：  
   - 按 `skills-rules-for-agent.md` 读 SKILL 并执行；  
   - 补建/补读 `docs/project-prd-changes/[change-id]/` 与 `openspec/changes/[change-id]/`；  
   - 确保迭代日志记录到位。

### 5. 面向用户的可见反馈

- simple：一句话说明「本次按简单任务处理，仅做文件级别改动，不写入变更单」。  
- heavy：一句话说明「本次按重规则执行，会加载完整规则并记录到迭代日志」。  
- 只有在需要用户在「治理强度 vs 成本」之间做显式权衡时，才把选择权抛给用户。

## 常见误区（反模式提示）

1. **默认把一切任务都当 heavy 处理**：  
   - 结果是简单小改动也要加载完整 rules，导致上下文与心智负担过重。  
2. **过度依赖 simple 模式，迟迟不升级为 heavy**：  
   - 在已经触达 OpenSpec/接口/安全边界的情况下仍不读 rules 与 SKILL，导致与规范脱节。  
3. **未记录 simple/heavy 判定与调整**：  
   - 看不到长期统计与体验反馈，难以改进判定策略。

> 对这些误区的更细节讨论，可在后续为此模式增加专门的 anti-pattern 条目。

## 与现有规范/技能的关系

- 本条目只是 `projects-rules-for-agent.md` 第 1.6 节的「扩展说明与操作化解读」，不改变其约束力。  
- 主 Agent 在实际工作中依然以 `projects-rules-for-agent.md` 为治理权威源；本 pattern 只作为判定与执行的操作指南。  
- 对于具体技能触发（request-analysis、project-analysis、coding-implement、code-review、func-test 等），仍须以 `skills-rules-for-agent.md` 与各技能 `SKILL.md` 为准。

## 关联模式

- 在做 simple/heavy 判定和动态切换时，建议同时考虑：  
  - `memory/patterns/pattern-model-tiering-and-quota-governance.md`：结合任务复杂度，决定是否需要升级到更高能力/成本的模型层级；  
  - `memory/patterns/pattern-openspec-change-workflow.md`：一旦判定为 heavy 且涉及 OpenSpec/变更单，应按 OpenSpec 变更标准流程挂载 change-id 与补齐文档。

