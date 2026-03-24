---
id: mem-business-project-directory-standard-001
title: 通用业务项目目录结构规范（长期模版）
type: pattern
tags: [project-structure, openspec, business-project, directory-standard]
applicable_projects: ["*"]
host_scope: [cursor, vscode, continue, openai-codex, generic]
source_change_ids: [project-early-phase]
created_at: 2026-03-19
last_reviewed_at: 2026-03-19
maturity: stable
related:
  - memory/patterns/pattern-spec-system-overview-v2-4.md
  - memory/patterns/pattern-openspec-change-workflow.md
  - memory/patterns/pattern-retrospective-one-time-production.md
  - memory/playbooks/playbook-retrospective-routine.md
---

# 通用业务项目目录结构规范（长期模版）

## 背景与适用场景

用于新建业务项目时快速初始化可治理、可追溯、可复用的目录结构，适配 OpenSpec 流程与项目级复盘沉淀。

## 推荐目录模版

```text
<business-project-root>/
├── README.md                          # 业务项目仓库总说明：项目简介、目录角色、协作入口、如何使用本仓库
├── 新用户快速使用手册.md                # 面向新成员/新 Agent 的上手指引：如何打开项目、如何运行、关键规范入口
│
├── src/                               # 业务源码根（**唯一合法**目录名；与 `openspec/project.md` 一致）
│   # 内部结构（如 miniprogram/pages、Web 的 src/components 等）由本项目 `openspec/project.md` 结合技术栈定义。
│
├── openspec/                          # OpenSpec 核心目录：本项目工程宪法与规范体系
│   ├── AGENTS.md                      # AI 工作说明书：项目类型、可用 Skills、需遵循的全局规则
│   ├── project.md                     # 项目工程宪法：技术栈、目录结构、命名与 change-id 规则
│   ├── specs/                         # 已实现能力规范（按 capability 划分子目录）
│   └── changes/                       # 进行中的变更提案（每个 change-id 一个子目录）
│
├── docs/                              # 需求侧与复盘（与 usr-rules OpenSpec 第一节一致）
│   ├── 项目事件日志.md                # 项目级日志（若项目约定唯一日志；记录里程碑与 Agent/技能调用）
│   ├── project-early-phase/           # 首个研发 change-id 之前的立项资料
│   ├── project-prd-changes/           # 每 change-id 的 PRD、records/、reference/
│   ├── retrospective/                 # 复盘（按 change-id 子目录或根下项目级）
│   └── sop-product-use/               # 可选：产品使用类 SOP
│
├── project-rules/                     # 仓库根：工程补充规范（由 openspec/project.md 引用）
│
└── scripts/                           # 自动化脚本统一目录（本项目脚本入口）
    └── README.md                      # 说明各脚本用途、使用方式与约束
```

## 各目录详细说明

### `<business-project-root>/`
业务项目仓库根目录名可自定义，但应在 `openspec/project.md` 中明确根目录与子目录角色映射。

### `src/`
业务源码根目录，**固定为仓库根下 `src/`**（usr-rules / `OpenSpec.md` 第一节），并在 `openspec/project.md` 固化。内部结构由本项目 `openspec/project.md` 结合技术栈定义。

### `openspec/`
OpenSpec 核心目录，存放本项目工程宪法与规范体系。标准结构包括：
- `AGENTS.md`：AI 工作说明书，定义项目类型、可用 Skills、需遵循的全局规则
- `project.md`：项目工程宪法，定义技术栈、目录结构、命名与 change-id 规则
- `specs/`：已实现能力规范（按 capability 划分子目录）
- `changes/`：进行中的变更提案（每个 change-id 一个子目录）

### `docs/项目事件日志.md`
位置与强制性源自 `OpenSpec.md` 第 1.1 节与第 6 节，以及 `global-rules/projects-rules-for-agent.md` 第三章。用于记录所有 change-id 下的 Agent/技能调用。

### `docs/project-early-phase/`
用于项目前期保留 change-id 的文档，遵循 `OpenSpec.md` 5.1 与 6.3 节。存放立项研究、市场/需求分析等前期文档。

### `docs/retrospective/<YYYY-MM>/`
项目级复盘（非单一 change-id）挂载点。路径风格参考 `memory/playbooks/playbook-retrospective-routine.md` 与 `memory/patterns/pattern-retrospective-one-time-production.md`。

### `docs/project-prd-changes/<change-id>/records/`
沿用 `OpenSpec.md` 对变更级记录类文档定位。存放该变更的验收记录、评审纪要、变更级复盘报告等。项目级复盘不放在单一 change-id 下。

### `scripts/`
脚本集中目录，与 `global-rules/projects-rules-for-agent.md` 第 4.1 节的脚本规则一致。

## 命名模版

- 业务项目根目录：`<business-project-root>/`（可自定义）。
- 业务源码根目录：**`src/`**（唯一合法名称）。
- 项目级复盘时间目录：`<YYYY-MM>`（例如 `2026-03`）。

## 关键约束

1. 项目级复盘统一放在 `docs/retrospective/<YYYY-MM>/`，不与单一 change-id 目录混放。
2. 变更级记录继续使用 `docs/project-prd-changes/<change-id>/records/`。
3. 迭代日志统一写入 `docs/项目事件日志.md`。

## 规范来源

- `OpenSpec.md` 第 1.1 节：`project-rules/`、`docs/`（按 usr-rules OpenSpec 第一节）、`scripts/`、`openspec/` 的定位说明。
- `OpenSpec.md` 第 3.1 节：`openspec/` 标准结构（`AGENTS.md`、`project.md`、`specs/`、`changes/`）。
- `OpenSpec.md` 第 5.1、6.1、6.3 节：`project-early-phase` 保留 change-id 与「先 `docs/project-prd-changes/[change-id]/` 后 `openspec/changes/[change-id]/`」顺序。
- `global-rules/projects-rules-for-agent.md` 第三章：`docs/项目事件日志.md` 的强制记录口径。
- `global-rules/projects-rules-for-agent.md` 第九章补充规则（项目结构）：通用业务项目目录结构模版与命名模版。
- `memory/patterns/pattern-retrospective-one-time-production.md`：复盘产出路径应归入 `docs/retrospective/[level]/`。
- `memory/playbooks/playbook-retrospective-routine.md`：项目级复盘目录与文件命名实践（项目级复盘与 change-id 级复盘分层）。
- `memory/patterns/pattern-spec-system-overview-v2-4.md`：规范体系分层与权威源关系（治理内核、项目工程宪法、补充约束）。
