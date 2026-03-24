---
id: mem-playbook-langgraph-backend-quickstart-001
title: LangGraph 后端新环境安装与启动（新用户/新机器）
type: playbook
tags: [langgraph, backend, quickstart, env-setup, agent_team_project]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, continue, openai-codex, generic]
source_change_ids: [migrate-langgraph-backend]
created_at: 2026-03-14
last_reviewed_at: 2026-03-14
maturity: stable
related:
  - memory/patterns/pattern-scenario-memory-trigger-governance.md
---

# LangGraph 后端新环境安装与启动

## 适用场景

| 场景 | 行动 |
|------|------|
| **新机器 / 新环境首次使用** | 执行「步骤 1：安装依赖」 |
| **遇到「未安装 langchain-openai」报错** | 执行「步骤 1」后，**用同一 .venv 重启后端** |
| **后端已装好后日常启动** | 执行「步骤 2：一键启动」 |
| **验证环境是否正常** | 执行「步骤 3：健康检查」 |

---

## 步骤 1：安装依赖（新环境必做）

> ⚠️ **重要**：系统不会自动安装，必须手动执行一次。

**一键安装（推荐）**：

```bash
cd agent_team_project
bash setup-langgraph-env.sh
```

**手动安装（备用）**：

```bash
cd agent_team_project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**安装完成标志**：

```bash
python3 -c "import fastapi, langgraph, langchain_openai; print('✅ 全部依赖已就绪')"
```

---

## 步骤 2：配置 API 与启动后端

### 2.1 配置 API 密钥

```bash
cd agent_team_project
cp .env.example .env
# 编辑 .env 填入 OPENAI_API_KEY
```

### 2.2 启动后端（二选一）

**方案 A：一键启动脚本（推荐）**

```bash
cd agent_team_project
./start-langgraph-backend.sh
```

- ✅ 自动设置 `AGENT_TEAM_PROJECT_ROOT`
- ✅ 启动前检查依赖完整性
- ✅ 缺失时提示修复并安全退出

**方案 B：手动启动**

```bash
cd agent_team_project
source .venv/bin/activate
export AGENT_TEAM_PROJECT_ROOT="/你的/agentsystem 仓库根路径"
uvicorn langgraph_backend.server:app --host 127.0.0.1 --port 8000
```

---

## 步骤 3：验证后端就绪

```bash
curl -s http://127.0.0.1:8000/health
```

**预期输出**：
```json
{"status":"healthy"}
```

---

## 快速问题排查

| 报错 | 立即修复 |
|------|----------|
| 「未安装 langchain-openai」 | `bash setup-langgraph-env.sh` → 重启后端 |
| 「AGENT_TEAM_PROJECT_ROOT 未设置」 | 用 `./start-langgraph-backend.sh` 或手动 export |
| 端口 8000 被占用 | `lsof -ti:8000 \| xargs kill -9` 或换端口 |

---

## 相关文档索引

| 文档 | 内容 |
|------|------|
| **`新用户快速开始.md`** §5.1 / §5.2 | 详细依赖清单、完整启动流程、MCP 配置 |
| **`platform-adapters/cursor/mcp-setup.md`** §6 | Cursor MCP 配置详解 |
| **`scripts/check-langgraph-backend/README.md`** | 一键自检脚本说明（验证环境健康） |
