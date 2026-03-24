---
id: preference-prd-architecture-naming-convention
title: PRD 命名与 design.md（技术方案正文唯一）
type: preference
description: PRD 推荐 PRD-[change-id]-[关键词].md；技术方案正文固定为 openspec/changes/[change-id]/design.md，不在 docs 下另写第二份「技术方案-*.md」正文。
description_long: |
  PRD 推荐 PRD-[change-id]-[关键词].md；技术方案正文固定为 openspec/changes/[change-id]/design.md（唯一），不在 docs 下另写一份「技术方案-*.md」正文。
  适用于所有 OpenSpec 项目。
applicable_projects:
  - agentsystem
  - "*"
tags:
  - 命名规范
  - 文档管理
  - 可追溯性
  - 文档规范
related:
  - pattern-prd-architecture-review-audit-trail
  - pattern-product-requirement-review-4d-checklist
created_by: 复盘-2026-03-14-naming-convention-upgrade
version: 1.0
---

# PRD 命名与 design.md（技术方案正文唯一）

## 核心洞察

PRD 旧命名（如「迭代需求说明.md」）存在识别性与可追溯性不足；**技术方案正文**在 OpenSpec 体系下**固定为** `openspec/changes/[change-id]/design.md`，**唯一**，不以「技术方案-[change-id]-*.md」在 `docs/project-prd-changes/` 重复维护第二份正文。

新命名规范通过引入 `PRD-[change-id]-[关键词].md` 格式，提升 PRD 侧识别与追溯。

## 命名原则

| 原则 | 说明 | 示例 |
|-----|------|------|
| **可识别性** | PRD 从文件名可识别；技术方案正文路径固定为 `design.md` | PRD 含 `PRD-` 前缀 |
| **可追溯性** | 文件名包含 change-id | 与 `openspec/changes/[change-id]/` 一一对应 |
| **可读性** | 文件名简洁明了 | 附加关键词增强可读性 |
| **一致性** | 同一项目内保持命名风格一致 | 统一采用 "PRD-" 前缀或统一采用 "迭代需求说明-" |

## 推荐命名格式

### PRD 命名格式

```
PRD-[change-id]-[关键词].md
```

- **change-id**: 变更 ID，kebab-case（如 `check-langgraph-backend`、`add-homepage`）
- **关键词**（可选）: 简短描述本次迭代的主题，便于快速理解（如 `一键自检`、`首页改版`）

**推荐示例**:
```
PRD-check-langgraph-backend-一键自检.md
PRD-add-homepage-首页改版.md
PRD-update-auth-flow-登录优化.md
```

**兼容格式**（仍支持）:
```
迭代需求说明-[change-id]-[关键词].md
```

### 技术方案正文（固定）

```
openspec/changes/[change-id]/design.md
```

- **唯一**：全变更仅此一份技术方案正文；图示等可放 `docs/project-prd-changes/[change-id]/architecture/` 并在 `design.md` 中引用。
- **评审纪要**（非正文）可放在 `docs/project-prd-changes/[change-id]/records/`，命名见 architecture-review 技能。

## 对比：旧命名 vs 新命名

| 维度 | 旧命名 | 新命名 | 改进 |
|-----|-------|--------|------|
| **识别性** | 迭代需求说明.md | PRD-check-langgraph-backend-一键自检.md | ✅ 可识别是 PRD |
| **可追溯性** | 无法对应 change-id | 包含 change-id，与 OpenSpec 目录对应 | ✅ 可追溯 |
| **可读性** | 无法快速理解主题 | 包含关键词「一键自检」 | ✅ 可读性强 |
| **技术方案正文** | 仅 `design.md` | 多份「技术方案-*.md」与 `design.md` 并存 | ❌ 禁止第二份正文 |

## 多文档拆分命名

### PRD 多文档命名（仍允许）

当 PRD 拆分为多文档时：

| 文档类型 | 命名格式 | 示例 |
|---------|---------|------|
| **主 PRD 文档** | `PRD-[change-id]-[关键词].md` | `PRD-add-homepage-首页改版.md` |
| **市场研究与产品方案** | `PRD-[change-id]-市场研究.md` | `PRD-add-homepage-市场研究.md` |
| **功能需求说明书** | `PRD-[change-id]-功能需求.md` | `PRD-add-homepage-功能需求.md` |
| **需求验收 Checklist** | `PRD-[change-id]-验收清单.md` | `PRD-add-homepage-验收清单.md` |
| **评审纪要** | `PRD-[change-id]-评审纪要.md` | `PRD-add-homepage-评审纪要.md` |

### 技术方案：不拆「第二份正文」

- 架构/接口/数据等章节**全部写入** `openspec/changes/[change-id]/design.md`；必要时用二级标题拆分。
- 附图放在 `docs/project-prd-changes/[change-id]/architecture/` 等，由 `design.md` 引用。

## 存放位置

### PRD 存放位置

```
docs/project-prd-changes/[change-id]/PRD-[change-id]-[关键词].md
```

**示例**:
```
docs/project-prd-changes/check-langgraph-backend/
├── PRD-check-langgraph-backend-一键自检.md
└── records/
    ├── PRD-check-langgraph-backend-评审纪要.md
    └── 技术方案-check-langgraph-backend-评审纪要.md
```

### 技术方案存放位置（唯一）

```
openspec/changes/[change-id]/design.md
```

**示例**:
```
openspec/changes/check-langgraph-backend/
├── proposal.md
├── tasks.md
├── design.md
└── specs/
    └── langgraph-backend/
        └── spec.md

docs/project-prd-changes/check-langgraph-backend/
└── records/
    └── 技术方案-check-langgraph-backend-评审纪要.md   # 评审纪要，非第二份方案正文
```

## 升级建议

### 对于新项目

1. **优先采用新命名格式**：从第一个 change-id 开始就使用 `PRD-[change-id]-[关键词].md` 格式
2. **必须包含 change-id**：确保与 `openspec/changes/[change-id]/` 目录一一对应
3. **可附加关键词**：增强可读性，但非强制

### 对于已有项目

1. **渐进式升级**：新 change-id 采用新命名格式，旧文档保持兼容
2. **重命名旧文档**（可选）：在适当时机（如重大改版时）重命名旧文档
3. **更新链接**：确保 proposal.md、tasks.md 中的文档引用链接同步更新

## 常见问题

### Q1: 为什么必须从 change-id？

**A**: change-id 是 OpenSpec 的核心标识符，所有变更相关文档都围绕 change-id 组织。包含 change-id 的命名可以：
- 快速定位到对应的 `openspec/changes/[change-id]/` 目录
- 与迭代日志中的记录对应
- 支持跨文档追溯（PRD → 技术方案 → 代码 → 验收记录）

### Q2: 关键词是必须的吗？

**A**: 关键词是可选但推荐的。关键词的作用是：
- 增强可读性，从文件名快速理解主题
- 当目录下有多个 PRD/技术方案文档时，便于区分
- 支持更精细的文档拆分（如 `PRD-xxx-市场研究.md`、`PRD-xxx-功能需求.md`）

### Q3: 旧文档需要重命名吗？

**A**: 旧文档保持兼容，不强制重命名。但建议：
- 新文档采用新命名格式
- 在文档头部添加说明，标注文档类型和 change-id
- 适当时机（如重大改版）再考虑重命名旧文档

### Q4: 如何检查命名是否规范？

**A**: 在自检清单中：
- PRD：是否符合 `PRD-[change-id]-[关键词].md`（若采用该约定）
- 技术方案：是否**仅**存在 `openspec/changes/[change-id]/design.md`，且无重复的「技术方案-*.md」正文

## 相关文档

- `skills/request-analysis/REFERENCE/迭代需求说明-PRD最小结构与自检.md` - PRD 规范，包含命名规范章节
- `skills/project-analysis/REFERENCE/技术方案与架构产出物-最小结构与自检.md` - 技术方案规范，包含命名规范章节
- `memory/patterns/pattern-prd-architecture-review-audit-trail.md` - 评审留痕机制

## 沉淀来源

- **复盘事件**: check-langgraph-backend PRD/技术方案命名规范升级
- **复盘日期**: 2026-03-14
- **复盘文档**: `docs/project-prd-changes/复盘报告-2026-03-14-最近2天工作内容完整复盘.md`
- **核心洞察**: 旧命名方式缺乏识别性和可追溯性，需要升级命名规范

---

**规范版本**: v1.0  
**最后更新**: 2026-03-14  
**维护者**: agentsystem 架构组
