# `logs/` 目录说明

## `agent.log`

| 项 | 说明 |
|----|------|
| **用途** | **集中**记录 **本仓 agentsystem** 与 **所有业务项目** 的 **Agent 执行日志**（同一文件追加，文本行或 JSON Lines，由接入方约定）。 |
| **范围** | 含：`agentsystem` 内核/治理侧操作；以及通过 `workspace/{project}/`（含 `claw-config` 软链）关联的各业务项目（如 **curiobuddy** 等）的 Agent 执行与门禁结果。 |
| **典型内容** | 会话/任务 id、**project 标识**、门禁执行结果、`models.json` 路由摘要、错误摘要等（**勿**写入 API Key、Cookie）。 |
| **建议格式** | 每条日志带 **project**（或 `change-id`）字段，便于过滤与检索；例如前缀 `project=curiobuddy` 或单行 JSON：`{"project":"curiobuddy","event":"..."}`。 |
| **谁写入** | 当前仓库 **无默认写入进程**；由你后续接入的 CLI、MCP、调度脚本等 **按行 `append`**。 |
| **为空** | 表示尚未产生任何记录，属正常。 |
| **轮转** | 体积变大时建议按日期或大小切分（如 `agent-2025-03-21.log`），避免单文件过大。 |
| **版本控制** | 若日志可能含项目路径或敏感信息，可将 `agent.log` 加入根目录 `.gitignore`；本目录保留 `README.md` 即可。 |

文件开头的 `#` 注释行为**人工说明**，接入日志管线时可选择跳过以 `#` 开头的行，或删除说明段后仅保留追加内容。
