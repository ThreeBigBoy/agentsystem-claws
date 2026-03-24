---
title: 功能测试与 OpenSpec 集成规范
description: 规范在 OpenSpec 项目中如何将功能测试与 change-id、spec 文档、任务与记录进行集成管理。
---

# 功能测试与 OpenSpec 集成规范

本规范说明在采用 OpenSpec 的项目中，如何将功能测试/验收流程与变更目录、规范文档和任务管理进行集成。

---

## 一、以 change-id 为测试单元

- 每次功能测试/验收应绑定一个明确的 `change-id`：
  - 对应的上下文为：`openspec/changes/[change-id]/` 下的 `proposal.md`、`design.md`（技术方案文件）、`specs/`、`tasks.md`。

- 如一次测试覆盖多个 change-id，应在记录中分别标注各用例对应的 change-id，或拆分为多次测试记录。

---

## 二、测试记录文件约定

- 推荐将功能测试记录统一输出到：
  - `documents/records/[change-id]-func-test.md` 或
  - `documents/records/[change-id]-acceptance.md`

- 建议的结构：
  1. 基本信息：change-id、测试日期、环境、测试者；
  2. 范围说明：本次测试覆盖/不覆盖哪些模块或场景；
  3. 用例列表与结果汇总（通过/未通过统计）；
  4. 问题与 bug 列表（含严重级别与位置）；
  5. 结论与建议（是否通过、是否需要补充测试或回归）。

---

## 三、与 specs/*/spec.md 的联动

- 在设计用例与记录结果时，应显式引用：
  - Requirement ID；
  - Scenario 名称或编号（如有）。

- 在测试记录中可以将用例与 Scenario 建立对应关系，例如使用表格或清单：
  - Scenario → 覆盖用例 → 结果（通过/未通过）。

- 当测试结果表明 Scenario 不合理或描述不足时，应在记录中提出，并推动对应 spec 做修订。

---

## 四、与 tasks.md 的联动

- 功能测试中发现的功能错误或高优先级问题，应：
  - 在 `tasks.md` 中新增对应任务条目；
  - 任务中引用测试记录中的问题编号或摘要。

- 在修复并重测后：
  - 更新测试记录，注明复测结果；
  - 在 `tasks.md` 中勾选任务为完成。

---

## 五、与 code-review 与 coding-implement 的联动

- 对于在功能测试中发现的问题：
  - 如属于实现层问题，应在下一轮 `coding-implement` 中修复；
  - 如属于设计/架构问题，可在 `code-review` 或 `project-analysis` 中讨论并调整。

- 在重大版本或关键 change-id 的发布前，可综合：
  - Code Review 记录；
  - 功能测试记录；
  - 任务完成情况；
  - 共同作为「是否发布」的决策依据。

---

## 六、OpenSpec CLI 验证（功能验收必含）

功能验收流程中，**OpenSpec 本身需包含**以下两轮 CLI 验证，与功能测试并行或穿插执行：

- **第一轮：`openspec validate [change-id]`**
  - 在锁定本次验收的 change-id 后、或在与用例梳理同一阶段执行；
  - 目的：验证**已开发完代码**所对应的变更目录（proposal、design、specs、tasks 等）结构完整、符合 OpenSpec 规范，且与当前实现范围一致；
  - 未通过时：根据 CLI 输出修正文档或实现，再将结果与修正动作记入验收记录，然后继续测试。

- **第二轮：`openspec validate --strict`**
  - 在功能测试执行完毕、验收记录输出之后执行；在项目根目录下运行；
  - 目的：以**严格模式**对整体 openspec 目录（含当前 change 及与其它变更/规范的一致性）做最终校验，确保可归档、可发布；
  - 未通过时：在验收记录中注明未通过项与建议处理方式，并将相关任务纳入 tasks.md 或后续变更；通过后再给出「推荐通过本次验收」的结论。

两轮验证的结果（通过/未通过及简要说明）应写入当次 `documents/records/[change-id]-func-test.md` 的「OpenSpec 验证」或「结论」小节，便于追溯与审计。

