---
id: mem-retrospective-data-driven-001
title: 数据驱动复盘法
type: pattern
tags: [retrospective, data-driven, metrics, analysis, evidence]
applicable_projects: [all]
host_scope: [cursor, vscode, continue, openai-codex, generic]
source_change_ids: [sys-retrospective-methodology-v1]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: draft
related:
  - memory/patterns/pattern-deep-retrospective-five-whys.md
  - memory/patterns/pattern-proactive-retrospective-trigger.md
  - memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md
---

# 数据驱动复盘法

## 背景与适用场景

主观感受和定性描述往往导致复盘结论偏差。数据驱动复盘法强调用可量化的证据替代主观判断，通过系统化的数据收集、分析和可视化，确保复盘结论的客观性和可验证性。

**适用场景：**
- 需要客观证明改进效果的场景
- 涉及多方责任界定的复盘
- 需要向利益相关者汇报的复盘
- 建立可复用的效能基线

## 数据收集体系

### 数据来源分层

```
┌─────────────────────────────────────────┐
│  Layer 1: 原始日志                        │
│  - runtime-logs/langgraph-runs/          │
│  - runtime-logs/model-calls/             │
│  - runtime-logs/system-events/           │
├─────────────────────────────────────────┤
│  Layer 2: 聚合指标                        │
│  - 执行时长分布                           │
│  - 成功率/失败率                           │
│  - 资源消耗统计                           │
├─────────────────────────────────────────┤
│  Layer 3: 分析洞察                        │
│  - 趋势分析                               │
│  - 异常检测                               │
│  - 关联分析                               │
├─────────────────────────────────────────┤
│  Layer 4: 复盘结论                        │
│  - 量化根因贡献度                          │
│  - 改进效果预测                            │
│  - ROI评估                                │
└─────────────────────────────────────────┘
```

### 核心数据维度

**执行数据**
```yaml
metrics:
  execution_time:
    - total_duration
    - step_breakdown
    - wait_time_ratio
  success_rate:
    - overall_completion_rate
    - step_failure_distribution
    - retry_success_rate
  resource_usage:
    - token_consumption
    - api_call_count
    - storage_utilization
```

**质量数据**
```yaml
metrics:
  output_quality:
    - lint_error_count
    - test_pass_rate
    - code_review_score
  process_quality:
    - spec_compliance_rate
    - documentation_coverage
    - decision_traceability
```

**协同数据**
```yaml
metrics:
  collaboration:
    - handoff_latency
    - response_time_by_role
    - context_switch_count
  communication:
    - message_clarity_score
    - feedback_loop_length
    - alignment_meeting_efficiency
```

## 分析方法论

### 对比分析法

**横向对比**
- 同一时间点不同Agent/角色的效能对比
- 不同技能执行成功率的对比
- 跨项目相似场景的对比

**纵向对比**
- 同一指标在不同时间段的演变
- 改进措施实施前后的对比
- 基线与当前的对比

**标杆对比**
- 与业界最佳实践的差距分析
- 内部最佳表现的借鉴

### 相关性分析

```
目标：识别问题根因与影响因素的关联强度

方法：
1. 收集潜在影响因素的数据
2. 计算各因素与问题发生的相关系数
3. 按贡献度排序，聚焦关键因素
4. 使用散点图/热力图可视化关联

示例：
代码审查拒绝率 与 文档完整度 的负相关
Agent重试次数 与 初始提示清晰度 的负相关
```

### 趋势预测法

**移动平均分析**
- 7日/30日移动平均线的趋势判断
- 识别趋势拐点，预判风险

**异常检测**
- 使用3σ原则识别超出正常范围的异常值
- 建立异常事件与问题发生的关联

## 数据可视化规范

### 复盘报告必备图表

1. **时间序列图** - 展示关键指标的历史演变
2. **对比柱状图** - 改进前后的效果对比
3. **帕累托图** - 问题根因的贡献度排序
4. **散点矩阵图** - 多因素相关性分析
5. **流程漏斗图** - 各环节转化率分析

### 数据呈现原则

- **原始数据可溯源** - 每个结论都能追溯到具体日志条目
- **统计方法透明** - 明确说明计算方法和假设条件
- **置信区间标注** - 展示数据的可靠程度
- **假设检验支持** - 关键结论需通过统计显著性检验

## 实施步骤

**Step 1: 数据基础设施建设**
- 确保 `runtime-logs/` 各子目录按规范收集数据
- 建立数据清洗和标准化流程
- 配置自动化数据采集脚本

**Step 2: 指标定义与计算**
- 为每个复盘主题定义核心指标
- 编写指标计算脚本/查询
- 建立指标字典，统一口径

**Step 3: 分析报告生成**
- 设计复盘报告模板
- 开发自动化报告生成工具
- 建立报告评审和校准机制

**Step 4: 数据驱动决策**
- 复盘会议以数据为讨论基础
- 改进措施的优先级按数据排序
- 效果验证以数据为准绳

## 与现有规范的关系

- 依托 `pattern-runtime-logs-usage-playbook-for-agents.md` 的数据收集规范
- 为 `pattern-deep-retrospective-five-whys.md` 的每一层分析提供数据支撑
- 为 `pattern-proactive-retrospective-trigger.md` 提供触发所需的量化指标

## 关联模式

- **运行时日志使用手册**：数据来源和质量保障
- **五层穿透分析法**：数据分析的输出目标
- **主动复盘触发机制**：数据分析的应用场景

