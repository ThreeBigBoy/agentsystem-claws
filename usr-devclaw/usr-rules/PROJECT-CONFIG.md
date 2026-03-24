# PROJECT-CONFIG：新业务项目仓库一次性初始化（目录与文件）

## 文档定位

- **用途**：**新建**「产品开发」类业务仓库时，按本文**创建目录与占位文件**，执行**一次**即可。  
- **非用途**：日常研发流程、变更门禁、OpenSpec 目录语义等**不在此展开**——见 **`OpenSpec.md`**。  
- **示例**：下文以 **`curiobuddy`** 为参照；`{project}` 替换为你的项目名/仓库名。

---

## 与 `OpenSpec.md` 的边界（只引用、不重复）

| 主题 | 权威位置 |
|------|----------|
| `docs/` 下各路径用途（立项、PRD、复盘、SOP 等） | **`OpenSpec.md` 第一节** |
| `openspec/` 标准结构、`specs` / `changes` / 归档概念 | **`OpenSpec.md` 第三节** |
| 新建 change-id 的**启动顺序** | **`OpenSpec.md` 第六节** |
| `proposal.md` / `tasks.md` / `design.md` / `spec.md` 要点 | **`OpenSpec.md` 第四节** |
| 10 步质量闭环与人工确认 | **`OpenSpec.md` 第二节** |

初始化时**仅**按本文创建**空壳与占位**；填写内容与流程约束一律以 **`OpenSpec.md`** 为准。

---

## 初始化总览（仓库根）

```text
{业务项目仓库根}/
├── claw-config/                    # ① 运行时：Agent 与技能索引（见下节）
├── openspec/                       # ② 治理与 OpenSpec：变更与能力基线（见下节）
├── docs/                           # ② 需求侧与 OpenSpec 配套文档（见下节）
├── src/                            # ③ 业务源码根（**唯一合法**名称，见 §③）
├── project-rules/                  # ④ 工程与协作补充规范（可空）
└── （可选）README.md               # 人类读者入口，指向 openspec / claw-config
```

> **空目录**：须保留的目录（如 `openspec/changes/archive/`、`docs/project-prd-changes/`）若暂无文件，可放 **`.gitkeep`** 以便 Git 跟踪。  
> **源码根**：**必须**为仓库根下 **`src/`**；**`openspec/project.md`** 中「业务源码根目录」须写 **`src/`**，与磁盘一致。

---

## ① `claw-config/`（运行时）

**作用**：与 `agentsystem` 协作时，`workspace/{project}` 软链通常指向此处；门禁与 Agent 规则默认读取 **`claw-config/AGENTS.md`**。目录名全仓库统一为 **`claw-config`**（或历史名 `devclaw-config`，**二选一**）。

**建议文件（与 `curiobuddy` 对齐；可逐文件从示例项目复制再改）**：

| 文件 | 说明 |
|------|------|
| **`AGENTS.md`** | **必选**：运行时人设、协作习惯、与 `openspec/AGENTS.md` 的分层关系 |
| `SOUL.md` | 可选：语气/品牌补充 |
| `MEMORY.md` | 可选：项目级 memory 摘要或指针 |
| `SKILLS.md` | 可选：质量闭环与技能索引 |
| `TOOLS.md` | 可选：脚本与工具说明 |
| `skills/<skill-name>/SKILL.md` | 可选：仅当项目**私有**技能包时建立 |

**不要求**在初始化阶段写满正文；可先有最小 **`AGENTS.md`**（含 frontmatter 可），其余按项目需要补全。

---

## ② `openspec/` 与 `docs/`（治理 + OpenSpec 规范落地）

### 2.1 `openspec/`（结构见 `OpenSpec.md` 第三节 §3.1）

至少包含：

| 路径 | 说明 |
|------|------|
| **`openspec/AGENTS.md`** | 治理层：项目类型、变更目录、日志、技能原则等（见各业务项目 `curiobuddy` 示例） |
| **`openspec/project.md`** | 项目定位、技术栈、**业务源码根目录：`src/`**、`project-rules/` 引用 |
| **`openspec/specs/`** | 能力基线目录（空即可，内按 capability 分子目录，见 §3.2） |
| **`openspec/changes/`** | 进行中变更；**尚未有 change-id 时可空** |
| **`openspec/changes/archive/`** | 已完成变更归档目录（**建议**初始化时创建并置 `.gitkeep`，与 `OpenSpec.md` 第三节「Archive」一致） |

**每个 change-id 下的** `proposal.md`、`tasks.md`、`design.md`、`specs/...` 等**不**在仓库初始化时批量创建；在 **首个研发 change-id 启动时**按 **`OpenSpec.md` 第六节** 建。

### 2.2 `docs/`（与 OpenSpec 第一节一致）

按 **`OpenSpec.md` 第一节** 建齐以下**目录**（可无文件，用 `.gitkeep`）：

| 路径 | 说明 |
|------|------|
| `docs/project-early-phase/` | 首个研发 change-id 之前的立项资料 |
| `docs/project-prd-changes/` | 每 change-id 的 PRD 侧；可先空 |
| `docs/retrospective/` | 复盘；可先空 |
| `docs/sop-product-use/` | 可选；可先空 |
| **`docs/项目事件日志.md`** | **建议**初始化时即创建（若项目约定「唯一项目日志」则写清规则，见 `curiobuddy` 示例） |

`docs/project-early-phase/README.md` 可作为**可选**占位，说明本目录用途（一句话 + 指向 `OpenSpec.md` 第一节）。

---

## ③ 业务源码根（**固定为 `src/`**）

- **命名**：业务项目仓库根下**唯一合法**的源码根目录名为 **`src/`**。**不得**使用 `app_<project_code>/`、`app_curiobuddy/`、`packages/app` 等作为源码根（与 **`OpenSpec.md` 第一节** 一致）。  
- **`openspec/project.md`**：须写明 **业务源码根目录：`src/`**，并与仓库内实际目录一致。  
- **初始化**：创建 **`src/`**（可仅 `.gitkeep`）；微信小程序等工程的小程序根目录**置于 `src/` 内**（如 `src/miniprogram/`），由 **`openspec/project.md`** 结合技术栈说明子结构。

---

## ④ `project-rules/`（工程补充规范）

- **作用**：仓库根级工程与协作补充规范（语言、提交、Lint、微信/平台约定等），由 **`openspec/project.md`** 的「工程补充约束」引用。  
- **初始化**：至少建目录；可放 **`.gitkeep`**，或从 **`curiobuddy`** 复制一份占位说明后再替换为项目正文。  
- **注意**：工程补充规范路径以 **`OpenSpec.md` 第四节**（`project.md` 一行）与 **`openspec/project.md`** 为准；本 usr-rules 约定为仓库根 **`project-rules/`**（与 `curiobuddy` 一致）。

---

## 与 agentsystem 的衔接（初始化后）

| 步骤 | 说明 |
|------|------|
| 软链 | 在 `~/agentsystem/workspace/{project}/` 下将 **`claw-config`** 指向项目内 **`claw-config/`**（名称与仓库内一致） |
| 门禁 | 若使用 `agents-md-enforcer` 等，确认 `claw_config_dirname` 与仓库目录名一致 |

详见 agentsystem 根目录 **`README.md`**（若存在）。

---

## 一次性初始化自检清单

- [ ] **`claw-config/AGENTS.md`** 已存在（最小可运行）  
- [ ] **`openspec/AGENTS.md`**、**`openspec/project.md`** 已存在  
- [ ] **`openspec/specs/`**、**`openspec/changes/`**、**`openspec/changes/archive/`** 已存在（空 + `.gitkeep` 可）  
- [ ] **`docs/`** 下 **`OpenSpec.md` 第一节** 所列目录已建；**`docs/项目事件日志.md`** 已按项目约定创建（若采用）  
- [ ] **`src/`** 已建；**`openspec/project.md`** 已声明业务源码根为 **`src/`**  
- [ ] **`project-rules/`** 已建  
- [ ] （可选）`agentsystem` **workspace** 软链已配置  

---

## 版本与维护

- 本文随 **usr-rules** 与示例项目（如 `curiobuddy`）结构微调；**业务仓库日常**以 **`OpenSpec.md`** 与项目内 **`openspec/AGENTS.md`** / **`openspec/project.md`** 为准。
- **目录结构大改**时：同步更新本文、**`OpenSpec.md` 第一节表格**（若约定变更）及示例项目。
