---
id: pattern-product-requirement-review-4d-checklist
type: pattern
title: 「必要性-合理性-优先级-内容质量」四维需求评审法
applicable_projects:
  - Proj01ShopifyTheme
  - generic-product-projects
source_change_ids:
  - update-theme-v1.0.2-mvp-health-compliance
tags:
  - requirements
  - review
  - product-management
  - spec-driven-development
related:
  - pattern-spec-system-overview-v2-4
  - pattern-scenario-memory-trigger-governance
  - pattern-iteration-log-enforcement-and-usage
---

## 背景

在 Proj01ShopifyTheme 项目中，针对 `update-theme-v1.0.2-mvp-health-compliance` 变更，主 Agent 在进入 OpenSpec 规范增量与编码前，先对 PRD 做了一轮「必要性、合理性、优先级、内容质量」四维度的需求评审，并同步回写到 PRD 与 records 中，效果良好。

本条记忆沉淀这一做法，供后续变更复用。

## 模式概要

在 **进入 OpenSpec/specs 与编码实现前**，先对单个变更的 PRD 做一轮轻量需求评审，固定四个问题：

1. **必要性**：这个变更是否真的直击项目初心或当前关键短板？  
2. **合理性**：产品方案在用户视角（toC）与编辑/运营视角（toB）上是否成立？是否有明显设计坑？  
3. **优先级**：在当前阶段，与其它候选需求相比，这个需求是否值得排在前面？  
4. **内容质量**：现有 PRD 是否已经达到「可执行/可验收」的粒度，还是仍停留在描述性层面？

评审结论不单独存放在脑海或对话中，而是**显式回写**到：

- PRD 本身（增加设计原则、验收 Checklist、边界场景等章节）；
- `docs/project-prd-changes/[change-id]/records/` 下的「需求评审结论」文档。

## 推荐执行步骤

1. **读取上下文**
   - 读取当前变更的 PRD（如 `docs/project-prd-changes/[change-id]/迭代需求说明.md`）；
   - 读取项目初心/背景文档与已归档变更的总结（如 MVP 方案、上一版本迭代进度检查）。

2. **按四个问题逐项评审**
   - 对每个问题给出一句结论（例如「必要性强」「优先级高但范围需收敛」）；
   - 用 2–4 个要点支撑结论，尽量引用现有文档与项目初心。

3. **回写 PRD**
   - 若 PRD 缺乏可执行约束，建议增加：
     - 设计取舍与交互原则（如字段取舍、交互上限、富文本 vs 结构化的取舍）；  
     - 验收 Checklist（toC/toB 分开列举若干场景）；  
     - 边界与异常场景（字段缺失、多设备响应式、未来多语言兼容性等）。
   - 修改应保持章节编号清晰，避免打乱原有结构。

4. **沉淀评审结论**
   - 在 `docs/project-prd-changes/[change-id]/records/` 下创建一份「需求评审结论」文档，结构包括：
     - 对四个维度的简要结论；
     - 已在 PRD 中完成的修改摘要；
     - 对下一步行动（OpenSpec/specs、编码、测试）的建议。

5. **再进入 OpenSpec/specs 与实现**
   - 在完成以上回写后，再开始为该变更补充/修改 `openspec/changes/[change-id]/specs/**/spec.md`；  
   - 编码与测试严格对齐 PRD 中的 Checklist 与边界场景。

## 使用时机

- 新变更刚完成 PRD 草稿，但尚未进入 OpenSpec/specs 与编码实现时；  
- 对已有需求存在「感觉有点虚」「不知道从哪里减范围」的直觉时；  
- 希望在一次迭代中把产品侧思考显式沉淀到文档，而不仅仅是在对话中达成共识。

## 反模式对比

- 反模式：PRD 写成“大作文”，直接进入编码，验收时再临时补 Checklist，导致实现与需求多次错位；  
- 本模式：先用四个问题把需求“拎干净”，再将评审结论结构化回写到 PRD + records，形成可追溯的产品决策链路。

