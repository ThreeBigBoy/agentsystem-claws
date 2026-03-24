# PRD 与 proposal 的定位区分（避免混用）

> **用途**：说明 **`docs/project-prd-changes/[change-id]/`** 下 **PRD（需求主文档）** 与 **`openspec/changes/[change-id]/proposal.md`**（OpenSpec **变更提案**）的职责边界，供执行 **`request-analysis`** 技能时对照。业务仓库的 **`claw-config/SKILLS.md`**、**`openspec/AGENTS.md`** 仅作指针，**不重复**展开全文。

---

## 对照表

| 文档 | 路径（相对业务仓库根） | 回答什么 | 与另一者的关系 |
|------|------------------------|----------|----------------|
| **PRD（需求主文档）** | `docs/project-prd-changes/[change-id]/`（如 `PRD.md` 或项目约定的等价文件名） | **做什么、为谁、验收标准、范围与非目标** | **需求侧权威**；评审与验收优先对齐 PRD |
| **proposal（变更提案）** | `openspec/changes/[change-id]/proposal.md` | **为何做本次变更、影响与风险、与 PRD 的对应关系** | **治理 / OpenSpec 侧**；**不是** PRD 的副本或别名；**须引用** PRD 路径（启动顺序见业务仓库 **`openspec/AGENTS.md`** §2.1 与 **`agentsystem/usr-devclaw/usr-rules/OpenSpec.md`** 第六节） |

---

## 与 `request-analysis` 全流程的关系

本技能 **`SKILL.md`** 中：

- **步骤 2**：在 **`docs/project-prd-changes/[change-id]/`** 产出或补充 PRD 侧文档（需求主文档落点）。
- **步骤 5**：在 **`openspec/changes/[change-id]/`** 创建或更新 **`proposal.md`**、`tasks.md`、`specs/...` 等变更包内容。

**常见误区**：把「需求分析阶段的产出」**仅**等同于 **`proposal.md`**，或把 **PRD** 与 **proposal** 当作同一文档。

**正确定位**：

- **需求主文档**在 **`docs/project-prd-changes/`**。
- **`proposal.md`** 用于衔接 **PRD** 与 OpenSpec **任务 / spec**，**不能替代 PRD**。
- 若某次任务**只**修订 PRD、尚未更新 `openspec/changes/`，仍属需求侧迭代，**不应**被描述成「`proposal.md` 是 `request-analysis` 的唯一产出」。

---

## 与「与 OpenSpec 的对应关系」表的关系

`request-analysis/SKILL.md` 中「与 OpenSpec 的对应关系」表列出各产出物路径；**PRD 类**落 **`docs/project-prd-changes/`**（按 usr-rules / 业务仓库约定），**变更提案**落 **`openspec/changes/[change-id]/proposal.md`**。二者语义以本文为准。
