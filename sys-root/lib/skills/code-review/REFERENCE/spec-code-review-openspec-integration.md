---
title: Code Review 与 OpenSpec 集成规范
description: 规范在 OpenSpec 项目中如何将 Code Review 结果与 change-id、spec 文档、任务与记录进行集成管理。
---

# Code Review 与 OpenSpec 集成规范

本规范专注于说明：在采用 OpenSpec 的项目中，如何将 Code Review 与变更目录、规范文档与任务管理集成，形成可追溯的质量记录。

---

## 一、以 change-id 为评审单位

- 每次 Code Review 必须绑定一个明确的 `change-id`，其上下文为：
  - `openspec/changes/[change-id]/proposal.md`
  - `openspec/changes/[change-id]/design.md`
  - `openspec/changes/[change-id]/specs/*/spec.md`
  - `openspec/changes/[change-id]/tasks.md`

- 如一次 review 涉及多个 change-id，应拆分为多次评审或在记录中分章节说明各自的 change-id 范围。

---

## 二、review 记录文件约定

- 统一将 Code Review 记录输出到 **`docs/project-prd-changes/[change-id]/records/`** 下，建议文件名 **`[change-id]-code-review.md`**（与 func-test 验收记录同目录，符合 OpenSpec 1.1 表约定）。

- 建议的记录结构：
  1. **基本信息**
     - change-id；
     - 评审日期与轮次（如 First/Second Round）；
     - reviewer 与参与者；
     - 涉及模块/文件列表。
  2. **整体结论**
     - 通过 / 需修改 / 需重大调整；
     - 关键风险点或注意事项。
  3. **问题清单**
     - 按优先级（Blocking / Major / Minor）列出问题；
     - 对应位置、描述、类型与建议方案。
  4. **后续行动**
     - 需要补充的任务（可同步到 `tasks.md`）；
     - 是否需要追加变更提案或更新规范文档。

---

## 三、与 tasks.md 的联动

- **将问题转化为任务**
  - 对 Blocking/Major 级问题，应在 `openspec/changes/[change-id]/tasks.md` 中新增或更新相应任务项；
  - 在任务描述中可引用 review 记录中的问题编号，便于追溯。

- **任务勾选与验收**
  - 问题修复完成后，对应任务应在 `tasks.md` 中打勾 `[x]`；
  - 如修复过程引入新问题或改动范围扩大，应在 review 记录中追加补充说明。

---

## 四、与规范文档的联动

- **更新规范文档的触发条件**
  - 若在 review 中多次发现同类问题（如分层越界、命名不一致、接口文档缺失等），说明现有 `project-rules/` 或层级规范可能不够清晰或不被遵守；
  - 建议在适当时机（例如重大版本或专题优化）：
    - 更新相关规范文档；
    - 在 review 记录中附上规范更新链接或说明。

- **避免文档与实现长期偏离**
  - 对于 review 中发现的「规范已不符合现实」的情况，应优先确定新的统一做法：
    - 或者修正代码以回归规范；
    - 或者修改规范以反映新的约定；
  - 不建议长期保留「文档写 A，代码做 B」的状态。

---

## 五、与 release / 验收的关系

- 在重要里程碑（如 MVP 上线、版本发布）前，建议：
  - 确认所有 P0/P1 级 change-id 至少完成一轮 Code Review；
  - `docs/project-prd-changes/[change-id]/records/` 中存在相应的 code-review 记录；
  - 关键问题已在 `tasks.md` 中闭环或在记录中说明延期/降级的原因。

---

## 六、在工具与流程中的应用

- 在自动化流程或工具集成中，可将本规范作为：
  - Code Review Checklist 的元数据来源（例如 PR 模板、Review Bot 规则）；
  - 质量度量（如每个 change-id 是否有 review 记录、问题关闭率等）的参考标准。

