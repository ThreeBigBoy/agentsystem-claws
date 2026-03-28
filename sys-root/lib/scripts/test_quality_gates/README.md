# 质量门禁两层判断机制测试脚本

## 概述

本测试脚本用于验证 Hybrid 质量门禁的**两层判断机制**是否正常工作。

## 架构

```
┌─────────────────────────────────────────────────────────────────────┐
│  第一层：check_*.py（显式调用入口，由 SKILL.md 触发）              │
│                                                                      │
│  --skip-llm → 仅 Python 自动化检查                                  │
│  --llm（默认）→ 调用 llm_enhancer.analyze_*()                       │
│                     │                                               │
│                     ↓                                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  第二层：llm_enhancer.py（内部判断）                          │  │
│  │                                                              │  │
│  │  "请使用API模型" → _call_api() → API 模型评审                 │  │
│  │  其他 → _agent_fallback() → Agent 直接执行评审                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## 测试场景矩阵

| 层级 | 参数/输入 | check_*.py 行为 | llm_enhancer 行为 |
|------|-----------|-----------------|-------------------|
| 第一层 | `--skip-llm` | 跳过 LLM | 不调用 | python_only |
| 第一层 | `--llm` + `""` | 调用 LLM | `_should_skip_llm=False` | → 第二层 |
| 第二层 | `""` | - | `_should_use_api=False` | Agent 评审 |
| 第二层 | `"请使用API模型"` | - | `_should_use_api=True` | API 评审 |

## 测试内容

| 测试模块 | 测试数 | 内容 |
|---------|-------|------|
| 第一层测试（--skip-llm） | 1 | 验证跳过 LLM 时无 llm_analysis |
| 第一层测试（--llm） | 1 | 验证启用 LLM 时有 llm_analysis |
| 第二层测试（llm_enhancer） | 6 | 验证 agent/api/python_only 分支 |
| Prompt结构测试 | 2 | 验证 agent/api 分支 prompt 差异 |
| 全门禁测试（PRD/方案/代码） | 6 | 验证三个门禁脚本的第一层判断 |
| 集成测试 | 2 | 验证两层判断协作 |
| **总计** | **18** | **全部通过** |

## 使用方法

### 基本执行

```bash
cd /Users/billhu/agentsystem
python sys-root/lib/scripts/test_quality_gates/test_quality_gates_full.py
```

### 环境要求

- Python 3.8+
- 需要配置 API Key（用于测试 API 评审分支）：

```python
os.environ["SILICONFLOW_API_KEY"] = "sk-..."
os.environ["MINIMAX_API_KEY"] = "sk-..."
```

### 测试文件依赖

- PRD 文件：`/Users/billhu/aiprojects/curiobuddy/docs/project-prd-changes/wechat-miniprogram-v0.1beta/PRD-wechat-miniprogram-v0.1beta-功能需求.md`
- 方案文件：`/Users/billhu/aiprojects/curiobuddy/openspec/changes/wechat-miniprogram-v0.1beta/proposal.md`
- 代码目录：`/Users/billhu/aiprojects/curiobuddy/src`

## 测试输出示例

```
======================================================================
质量门禁两层判断机制完整测试 v2
======================================================================

【第一层测试】--skip-llm 跳过 LLM
======================================================================

1. check_prd.py --skip-llm
   ✅ llm_analysis=无
   score=260.0

【第一层测试】--llm 启用 LLM（调用 llm_enhancer）
======================================================================

1. check_prd.py --llm
   ✅ llm_analysis=有
   llm_score=80.0
   score=152.0

...

======================================================================
【最终结果】
======================================================================
✅ 所有测试通过！两层判断机制工作正常。
======================================================================
```

## 测试对象源代码路径

本测试脚本测试的是 **Hybrid 质量门禁** 的两层判断机制，源代码位于：

```
sys-root/lib/skills/dev-workflow-orchestration/references/quality-gates/
├── check_prd.py              # PRD 质量门禁（第一层入口）
├── check_solution.py        # 方案质量门禁（第一层入口）
├── check_code.py            # 代码质量门禁（第一层入口）
├── check_delivery.py        # 交付质量门禁
├── llm_enhancer.py          # LLM 语义增强（第二层判断）
├── model_selector.py        # 模型选择器
├── config.yaml              # 门禁配置
└── run_gates.py             # 统一入口
```

**完整路径**：
```
/Users/billhu/agentsystem/sys-root/lib/skills/dev-workflow-orchestration/references/quality-gates/
```

## 相关文件

| 文件 | 路径 | 说明 |
|------|------|------|
| `llm_enhancer.py` | `quality-gates/llm_enhancer.py` | LLM 语义增强模块（第二层判断） |
| `check_prd.py` | `quality-gates/check_prd.py` | PRD 质量门禁脚本（第一层入口） |
| `check_solution.py` | `quality-gates/check_solution.py` | 方案质量门禁脚本 |
| `check_code.py` | `quality-gates/check_code.py` | 代码质量门禁脚本 |
| `config.yaml` | `quality-gates/config.yaml` | 质量门禁配置 |

## 修复记录

### v2 - 修复无限递归问题

**问题**：原实现中 `llm_enhancer._run_python_check()` 调用 `check_*.py --json`，当 `check_*.py` 默认启用 LLM 时会形成无限递归。

**修复**：
1. `_run_python_check()` 改用 `--skip-llm` 参数，只做纯 Python 检查
2. 超时从 30 秒增加到 60 秒
3. JSON 输出包含 `llm_analysis` 和 `llm_score` 字段

### v1 - 初始版本

初始版本存在 JSON 解析失败、超时等问题。

## 创建信息

- **创建日期**: 2026-03-28
- **作者**: Agent
- **用途**: 验证质量门禁两层判断机制
