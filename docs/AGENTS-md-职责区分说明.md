# AGENTS.md 职责区分说明

> **文档类型**: 架构设计说明  
> **主题**: openspec/AGENTS.md vs devclaw-config/AGENTS.md 职责划分  
> **日期**: 2026-03-21
> **背景**：用户提问：openspec下的agent.md和project.md是否还有必要保留，能否删除？避免多头说明
---

## 核心结论

**不建议删除，两者职责不同**

`devclaw-config/AGENTS.md` 和 `openspec/AGENTS.md` **不是重复**，而是**不同层级的定义**。

---

## 职责对比

| 文件 | 层级 | 内容 | 作用 |
|------|------|------|------|
| `openspec/AGENTS.md` | **治理层**（标准） | 定义"Agent 应该遵循什么规范"<br>例如：必须读取 SKILL.md、必须遵循 10 步流程、必须记录迭代日志 | **约束所有 Agent**（包括 devclaw） |
| `devclaw-config/AGENTS.md` | **运行时层**（实例） | 定义"这个 Agent 具体怎么工作"<br>例如：Curiobuddy 是教育助手、使用哪些技能、什么语气 | **具体项目 Agent 的配置** |

---

## 举例说明

### openspec/AGENTS.md（治理标准）

```markdown
# openspec/AGENTS.md

## 所有 Agent 必须遵守

1. 执行技能前必须读取对应 SKILL.md
2. 完成任务后必须更新迭代日志
3. 设计阶段必须遵循 OpenSpec 变更流程
4. 代码提交前必须通过质量门禁

→ 这是"规矩"，所有 Agent 都要遵守
```

### devclaw-config/AGENTS.md（具体配置）

```markdown
# devclaw-config/AGENTS.md

## Curiobuddy 专属配置

- 角色：K12 教育助手
- 语气：鼓励性、亲和
- 技能：content-generation、student-assessment
- 禁止：直接给答案，必须引导思考

→ 这是"人设"，只针对 Curiobuddy
```

---

## 层级关系

```
openspec/AGENTS.md （父规则 - 治理标准）
    ↓ 约束、引用
    
devclaw-config/AGENTS.md （子配置 - 运行时实例）
    ↓ 补充、特化
    
具体 Agent 运行时行为
```

---

## 避免"多头说明"的建议

如果觉得混乱，可以在 `devclaw-config/AGENTS.md` 中**明确引用**治理规则：

```markdown
# devclaw-config/AGENTS.md

## 治理规范遵循

本 Agent 遵循项目 OpenSpec 治理规范：
- 规范文件：../../../openspec/AGENTS.md
- 变更流程：遵循 OpenSpec 第六节变更启动顺序
- 质量标准：必须通过 4 个质量门禁

## Curiobuddy 专属配置

...（具体人设、技能）
```

这样既避免了重复定义，又明确了层级关系。

---

## 能否删除的情况

| 情况 | 建议 |
|------|------|
| 项目很小，只有 1 个 Agent | 可以合并到 devclaw-config/，openspec/ 只保留极简规则 |
| 严格遵循 agentsystem 治理 | 保留两者，devclaw-config/AGENTS.md 引用 openspec/ |
| 完全自定义，不遵循外部规范 | 可以删除 openspec/AGENTS.md，只保留 devclaw-config/ |

---

## 总结

**保留两者，但明确关系**：

- `openspec/AGENTS.md` = 项目治理规则（如果有变更流程、质量标准等）
- `devclaw-config/AGENTS.md` = 具体 Agent 配置（人设、技能、语气）

如果 openspec/ 下确实没有内容（只有空文件），可以删除。但如果包含治理规则，建议保留并建立引用关系。

---

**文档状态**: 架构设计说明  
**维护者**: agentsystem 架构组  
**日期**: 2026-03-21
