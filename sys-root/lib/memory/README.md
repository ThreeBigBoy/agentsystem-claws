## `memory/`：长期记忆库

本目录用于存放从多次任务复盘、故障修复与成功实践中提炼出的**长期记忆**，通过结构化元数据（frontmatter）标记适用范围，指导后续类似任务的决策与执行。

### 定位

- 与 `docs/project-prd-changes/[change-id]/records/` 下的一次性复盘/验收记录区分：
  - **records/**：针对单个 change-id 的具体记录；
  - **memory/**：跨 change-id / 跨项目具有长期复用价值的模式和经验。
- 记忆条目用于：
  - 复用已验证的最佳实践（patterns）；
  - 显式标注常见陷阱与反模式（anti-patterns）；
  - 记录项目/用户的偏好（preferences，需用户确认）；
  - 描述复杂场景的 SOP（playbooks）；
  - 汇总跨项目的深度反思（reflections）。

### 目录结构

```text
memory/
├── README.md          # 本说明文档
├── memory.json        # 全局索引（manifest）：按「记忆类型」「适用场景」等维度检索；`entries` 由维护者或脚本填充
├── schema.md          # frontmatter 规范与示例
├── patterns/          # 【模式】可复用的成功实践
├── anti-patterns/     # 【反模式】常见坑点与反例
├── preferences/       # 【偏好】项目/用户的偏好（需确认）
├── playbooks/         # 【剧本】复杂场景的标准操作流程
└── reflections/       # 【反思】跨项目的经验总结
```

### 使用建议（简要）

- 在启动新任务或变更分析前，主 Agent 或相关子 Agent 应根据当前项目、宿主与任务类型检索匹配的记忆条目，并将其作为方案设计与执行的参考；
- 记忆条目应在复盘阶段由主 Agent 明确判断与创建，避免自动化记录导致噪音和误导；
- 具体 frontmatter 字段与沉淀流程见 `schema.md`。

### 文件命名建议

为便于人类与 Agent 快速浏览与检索，建议在 `memory/*/` 下为 Markdown 文件采用以下命名约定：

- 基本格式：`{type}-{1~3个英文/拼音关键词}-{可选版本号}.md`
  - `type`：与 frontmatter 中的 `type` 一致，例如 `pattern` / `anti-pattern` / `preference` / `playbook` / `reflection`；
  - 关键词：概括记忆主题的 1～3 个英文或拼音短语（如 `openspec-change-workflow`、`runtime-logs-memory-minimal-practice`）；
  - 版本号（可选）：当同一主题存在多轮演进时，可在末尾追加 `-v1` / `-v2` 等。
- 示例：
  - `pattern-openspec-change-workflow.md`
  - `pattern-runtime-logs-memory-minimal-practice.md`
  - `anti-pattern-runtime-logs-business-data-pitfall.md`
  - `preference-user-coding-style.md`

