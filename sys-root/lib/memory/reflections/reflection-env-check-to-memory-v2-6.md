---
id: mem-reflection-env-check-to-memory-001
title: 环境检查沉淀为 memory 与主动触发（v2.6 / migrate-langgraph-backend 后续）
type: reflection
tags: [langgraph, env-check, memory, scenario-trigger, migrate-langgraph-backend]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [migrate-langgraph-backend]
created_at: 2026-03-14
last_reviewed_at: 2026-03-14
maturity: stable
related:
  - memory/patterns/pattern-langgraph-backend-readiness-check.md
  - memory/patterns/pattern-scenario-memory-trigger-governance.md
  - memory/playbooks/playbook-langgraph-backend-quickstart.md
---

# 反思：IDE 启动后环境检查 → 转化为 memory 并在恰当时机主动做

## 事件回顾

- **触发**：用户在一次 IDE 启动后提出「请检查环境是否已全部启动？」  
- **执行**：主 Agent 对 agentsystem 与多工作区做了环境检查：  
  - LangGraph 后端：`GET http://localhost:8000/health` → 200，判定已就绪；  
  - 可选：Shopify theme dev（如 Proj01ShopifyTheme）未检测到，给出启动命令提示。  
- **结论**：LangGraph 后端已就绪，可正常使用 MCP run_langgraph；其它环境按需启动。

## 反思问题：是否需要转化为 memory，并在恰当时机主动做？

**结论：需要。**

1. **价值**  
   - 用户不一定会主动说「检查环境」；若在「即将用 run_langgraph 执行任务」前先检查后端是否存活，可减少调用失败后的排查成本。  
   - 将「检查步骤」与「未就绪时如何引导」固化下来，主 Agent 在相同场景下行为一致，且可引用 playbook，避免临时发挥。

2. **恰当时机（不每次会话都查）**  
   - 用户**明确要求**「检查环境」「环境是否启动」时 → 执行检查并汇报。  
   - **即将通过 MCP 执行** run_langgraph 或变更任务时 → 执行前先 GET /health，未就绪则提示启动并引用 playbook，再执行或中止。  
   - 不在每条消息或每次会话开始时自动检查，避免无谓请求与打扰。

3. **已落实的沉淀**  
   - 新增 **`memory/patterns/pattern-langgraph-backend-readiness-check.md`**：定义何时做、必做步骤（检查 /health、未就绪时引用 playbook）、与 playbook 的关系。  
   - 在 **`pattern-scenario-memory-trigger-governance`** 的「场景→必读/必做」绑定表中新增一行：**「LangGraph 后端就绪检查（执行前环境自检）」**，触发条件与必做内容写清，主 Agent 在对应场景下加载该 pattern 并执行检查。  

这样，主 Agent 既能在用户问「检查环境」时按同一套步骤执行，也能在「准备用 run_langgraph 跑任务」时**主动**先做一次就绪检查，再决定是否继续或提示用户启动后端。
