---
id: mem-pattern-new-pipeline-trace-vs-design-docs
title: 新管线留痕与 docs/project-prd-changes 职责分离
type: pattern
tags: [langgraph, runtime-logs, trace, design-documents, audit]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [migrate-langgraph-backend]
created_at: 2026-03-14
last_reviewed_at: 2026-03-14
maturity: stable
related:
  - memory/patterns/pattern-langgraph-mcp-multi-workspace-config.md
  - docs/project-prd-changes/新管线留痕与业务项目openspec-需求落实.md
  - docs/project-prd-changes/问题反馈-agent_decision-feedback-skill-log-为空-排查.md
---

# 新管线留痕与 docs/project-prd-changes 职责分离

## 背景与适用场景

新管线（LangGraph，run_langgraph）的执行审计、是否执行过、执行结果判定，应与「需求落实说明、问题排查、预期校对」等文档职责分离，避免误用 docs/project-prd-changes 或旧三件（agent_decision.json、agent_feedback.txt、agent_skill.log）做新管线的审计依据。

## 推荐做法

1. **新管线唯一合法执行留痕**  
   - **位置**：`agentsystem/runtime-logs/langgraph-runs/`，按日分片 `YYYY-MM-DD.jsonl`。  
   - **内容**：ts、change_id、thread_id、workspace_root、project_key、status、task_count、latency_seconds、checkpoint_id、error 等；由 `langgraph_backend/server.py` 在每次 `/run`、`/resume` 成功或失败后追加。  
   - **不依赖**：迭代日志、docs/project-prd-changes 不参与「是否执行过 / 执行结果」的判定与审计。

2. **docs/project-prd-changes 的职责**  
   - 用于需求落实说明、预期效果校对、问题排查结论等**过程与文档**；不参与新管线的执行审计。  
   - 排查「本轮有没有跑新管线」「执行记录在哪」时，应查 **runtime-logs/langgraph-runs/**，不查 docs/project-prd-changes 或旧三件。

3. **排查「无记录」时的顺序**  
   - 先区分是否走了**新管线**（是否调用了 run_langgraph、后端是否启动）。  
   - 若走新管线：留痕在 runtime-logs/langgraph-runs/；**不**写 agent_decision.json / agent_feedback.txt / agent_skill.log，这三份为空是预期。  
   - 若三份都空且声称完成：多为在对话内直接编辑、未走任一管线；应引导显式调用 run_langgraph 并确认后端已启动。

## 反例与常见误区

- **误区**：用 agent_decision.json / agent_feedback.txt / agent_skill.log 判断「新管线是否执行过」——新管线本身不写这三份，应看 runtime-logs/langgraph-runs/。  
- **误区**：把「是否执行过」的审计依赖写在 docs/project-prd-changes 或迭代日志；新管线的审计依据仅为 runtime-logs/langgraph-runs/。

## 与现有规范的关系

- 需求与落实见 `docs/project-prd-changes/新管线留痕与业务项目openspec-需求落实.md`。  
- 旧三件为空的原因与两套管线说明见 `docs/project-prd-changes/问题反馈-agent_decision-feedback-skill-log-为空-排查.md`。

## 关联模式

- 多业务项目 MCP 配置见 `pattern-langgraph-mcp-multi-workspace-config.md`。  
- 场景触发与必读 memory 见 `pattern-scenario-memory-trigger-governance.md`。
