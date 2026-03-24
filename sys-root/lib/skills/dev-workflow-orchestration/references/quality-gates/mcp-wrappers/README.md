# MCP Server (保留备选)

> **状态**: 保留备选，当前链路已简化为 Agent 直接调用脚本
> **日期**: 2026-03-24

## 说明

本目录包含 MCP Server 实现，作为备选方案保留。

**当前实际使用**：Agent 直接通过 `subprocess` 调用 `check_*.py` 脚本，无需 MCP 中间层。

## 架构对比

### 简化后（当前采用）

```
Agent → subprocess.run() → check_*.py
```

### MCP 方案（保留备选）

```
Agent → Trae MCP Client → mcp_server.py → check_*.py
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `mcp_server.py` | MCP Server 实现（使用 MCP SDK） |
| `mcp_config.yaml` | MCP 配置 |

## MCP Server 用途

如果未来需要通过 MCP 协议对外提供服务（如供其他 MCP Client 调用），可启用此方案。

启用方式：
1. 在 `~/Library/Application Support/Trae CN/User/mcp.json` 中配置
2. 重启 Trae

## 自动发现逻辑

MCP Server 实现了以下自动发现逻辑：
- 从 cwd 向上查找 `openspec/changes/<change-id>`
- 根据 change-id 构建正确的文件路径
- 读取 config.yaml 获取模型路由配置
