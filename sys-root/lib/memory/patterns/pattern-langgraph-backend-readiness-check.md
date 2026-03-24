---
id: mem-pattern-langgraph-backend-readiness-check-001
title: LangGraph 后端就绪检查（执行前环境自检）
type: pattern
tags: [langgraph, backend, readiness-check, env-check, migrate-langgraph-backend]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [migrate-langgraph-backend]
created_at: 2026-03-14
last_reviewed_at: 2026-03-14
maturity: stable
related:
  - memory/patterns/pattern-scenario-memory-trigger-governance.md
  - memory/playbooks/playbook-langgraph-backend-quickstart.md
  - memory/patterns/pattern-change-full-lifecycle-delivery.md
---

# LangGraph 后端就绪检查（执行前环境自检）

## 背景与来源

自 **migrate-langgraph-backend**（v2.6 相关变更）起，多 Agent 协同执行依赖 LangGraph 独立后端（`agent_team_project/langgraph_backend/`），通过 MCP 工具 `run_langgraph`、`resume_langgraph` 或 HTTP `/run`、`/status`、`/health` 与后端交互。若后端未启动，调用会失败且报错不直观。

用户在一次 IDE 启动后主动要求「检查环境是否已全部启动」，主 Agent 执行了：  
- 对 `GET http://localhost:8000/health` 的可用性检查（返回 200 即就绪）；  
- 可选对其它工作区依赖（如 Shopify theme dev 端口）的检查。  

本 pattern 将此类**环境就绪检查**沉淀为可复用、可在恰当时机**主动执行**的步骤，避免依赖用户每次手动提醒。

## 何时做（触发时机）

主 Agent 应在以下任一情况**执行前**主动做一次 LangGraph 后端就绪检查（不限于用户明确说「检查环境」时）：

1. **用户明确要求检查环境**  
   - 例如：「检查环境是否已全部启动」「环境都起来了吗」「确认一下后端在跑」等。

2. **即将通过 MCP 或 HTTP 调用 LangGraph 后端时**  
   - 例如：用户说「用 run_langgraph 执行某 change」「请通过 MCP 跑一下任务」等，在真正调用 `run_langgraph` 或 POST `/run` **之前**先检查 `/health`。

3. **任务上下文强烈暗示会用到后端时**  
   - 例如：当前对话或打开文件涉及 `agent_team_project/`、`langgraph_backend/`、`migrate-langgraph-backend` 等，且用户指令可能触发任务执行时，可先做一次轻量检查再继续。

**不做**：无需在每次会话或每条消息开始时都检查；仅在「可能用到后端」或「用户明确要求检查」时执行，避免无谓请求。

## 必做步骤（检查清单）

1. **检查 LangGraph 后端健康**  
   - 请求 `GET http://localhost:8000/health`（或 `http://127.0.0.1:8000/health`）。  
   - 若返回 HTTP 200 且 body 含 `"status":"healthy"`（或等价），视为**就绪**，可继续执行 run_langgraph 或其它调用。  
   - 若请求失败（连接拒绝、超时、非 2xx），视为**未就绪**。

2. **未就绪时的响应**  
   - 明确告知用户「LangGraph 后端未检测到运行」。  
   - 提示用户先启动后端，并引用 **`memory/playbooks/playbook-langgraph-backend-quickstart.md`**（或 `agent_team_project/langgraph_backend/README.md`）中的启动步骤：  
     - `cd agent_team_project && source .venv/bin/activate`  
     - 设置 `AGENT_TEAM_PROJECT_ROOT` 指向含 `openspec/changes` 的仓库根  
     - `uvicorn langgraph_backend.server:app --host 127.0.0.1 --port 8000`  
   - 不代替用户执行启动命令（除非用户明确要求），仅给出指引与文档引用。

3. **可选：多工作区下的其它环境**  
   - 若当前工作区包含 Proj01ShopifyTheme 等且任务可能涉及主题预览，可顺带说明「Shopify theme dev 未检测到」并给出 `shopify theme dev --path theme-health-food` 等提示；  
   - 此类检查为**可选**，不写入强制绑定，由主 Agent 根据上下文判断。

## 与场景绑定的关系

本 pattern 已纳入 **`pattern-scenario-memory-trigger-governance`** 的「场景→必读/必做」绑定表：  
- 场景名：「**用户请求检查环境 / 即将通过 MCP 执行 run_langgraph 或变更任务**」  
- 触发时执行上述「必做步骤」，并在未就绪时引用 playbook。  

主 Agent 在「主动记忆唤醒」或执行 run_langgraph 前，应加载本 pattern（或通过场景绑定表间接触发），按步骤执行检查。

## 关联模式

- **playbook-langgraph-backend-quickstart.md**：安装依赖与启动后端的完整步骤，在「未就绪」时引用。  
- **pattern-scenario-memory-trigger-governance.md**：本检查作为表中新增场景，在恰当时机由主 Agent 主动执行，无需用户每次提醒。
