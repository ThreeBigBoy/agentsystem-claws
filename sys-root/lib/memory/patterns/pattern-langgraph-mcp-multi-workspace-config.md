---
id: mem-pattern-langgraph-mcp-multi-workspace
title: LangGraph MCP 多业务项目配置范式
type: pattern
tags: [langgraph, mcp, workspace, multi-project, cursor]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [migrate-langgraph-backend]
created_at: 2026-03-14
last_reviewed_at: 2026-03-14
maturity: stable
related:
  - memory/patterns/pattern-scenario-memory-trigger-governance.md
  - docs/project-prd-changes/新管线留痕与业务项目openspec-需求落实.md
---

# LangGraph MCP 多业务项目配置范式

## 背景与适用场景

在 Cursor 等宿主中配置 LangGraph 后端 MCP 时，若需支持**多个业务项目**（如 Proj01ShopifyTheme、test_bizproject），需解决：如何声明项目列表、如何避免取错项目、是否要「当前项目」配置。本模式沉淀实践结论，避免重复试错。

## 推荐做法

1. **单 key 存项目列表（Cursor env 为键值对象）**  
   Cursor 的 `env` 只能是键值对，无法使用 `"env": [{...}, {...}]`。用**单个 key 存 JSON 数组字符串**表达多项目：
   - **LANGGRAPH_WORKSPACE_PROJECTS**：值为 JSON 字符串，如  
     `"[{\"LANGGRAPH_PROJECT_KEY\":\"Proj01ShopifyTheme\",\"LANGGRAPH_WORKSPACE_ROOT\":\"/path/Proj01\"},{...}]"`  
   - 或扁平串兼容：`"key1|path1:key2|path2"`（项目间 `:` 或 `;` 分隔）。

2. **仅此一项即可，无需「当前项目」key**  
   - 后端**优先本仓**（agentsystem/openspec/changes/），再按列表顺序尝试每个项目根；**第一个存在该 change_id 的 tasks.md 的 root 即命中**（按 change_id 自动解析）。  
   - 因此不需也不推荐单独配置 LANGGRAPH_CURRENT_PROJECT_KEY；若确有「固定当前项目」需求，可可选保留该 key，MCP 则只传该 root。

3. **本仓优先**  
   解析顺序固定：先本仓 → 再业务项目列表。在本仓迭代时，即使用户配置了多个业务项目，也不会取错。

## 反例与常见误区

- **误区**：用多个 env key（如 PROJECT_1_ROOT、PROJECT_2_ROOT）或幻想 env 数组，导致与宿主能力不符、配置冗长。  
- **误区**：强依赖「当前项目」单一 key，导致切换项目必须改配置；按 change_id 解析可避免频繁改配置。

## 与现有规范的关系

- 实现与入口见 `docs/project-prd-changes/新管线留痕与业务项目openspec-需求落实.md`、`platform-adapters/cursor/mcp-setup.md` §6。  
- 配置/排查多业务项目或新管线留痕时，可结合本 pattern 与 `pattern-new-pipeline-trace-vs-design-documents` 使用。

## 关联模式

- 新管线留痕与 docs/project-prd-changes 职责分离见 `pattern-new-pipeline-trace-vs-design-documents.md`。  
- 场景触发与必读 memory 绑定见 `pattern-scenario-memory-trigger-governance.md`。
