# 质量门禁使用指南

## 概述

Hybrid 质量门禁（Python + LLM）是一套量化验证 PRD/方案/代码/交付质量的工具集。

## 核心执行逻辑

### 两层判断机制

| 层级 | 判断条件 | 执行行为 |
|------|----------|----------|
| **第一层** | 命中"不使用LLM" | 仅执行 Python 自动化检查 |
| **第一层** | 未命中"不使用LLM" | 先 Python 自动化检查，再 LLM 语义增强 |
| **第二层** | 命中"请使用API模型" | 调用 API 模型，失败则 Agent 兜底 |
| **第二层** | 未命中"请使用API模型" | 直接由当前会话 Agent 完成评审 |

### 执行流程

```
analyze_*(content, file_path, user_input)
    │
    ├─ 第一层: 不使用LLM?
    │       │
    │       ├─ 是 → 仅 Python 自动化检查 → 返回
    │       │
    │       └─ 否 → 执行 Python 自动化检查
    │                   │
    │                   ▼
    │       第二层: 请使用API模型?
    │               │
    │               ├─ 是 → 调用 API 模型
    │               │       ├─ 成功 → 返回 API 结果 + Python 检查
    │               │       └─ 失败 → Agent 兜底 + Python 检查
    │               │
    │               └─ 否 → Agent 执行 + Python 检查
```

### 兜底机制

| 场景 | 行为 |
|------|------|
| 优先策略 | 直接由当前会话 Agent 完成评审 |
| 显式调用 API | 命中"请使用API模型"时调用 API |
| API 失败 | 兜底由当前会话 Agent 完成评审 |

### 返回值结构

```python
{
    "analysis": "...",           # LLM 分析内容
    "score": 80,                 # 综合评分
    "passed": true,              # 是否通过
    "source": "api/agent_fallback/python_only",
    "python_check": {...}        # Python 自动化检查结果
}
```

## 架构

```
┌─────────────────────────────────────────────────────────┐
│              Hybrid 质量门禁 v2.0                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Gate 1: PRD 质量门禁（Blocking，阈值80）               │
│  ├── Python: 结构/格式/关键词                           │
│  └── LLM: 逻辑/设计/建议                               │
│                                                          │
│  Gate 2: 方案质量门禁（Warning，阈值75）                │
│  ├── Python: PRD对应性/接口定义                         │
│  └── LLM: 风险/可行性                                   │
│                                                          │
│  Gate 3: 代码质量门禁（Blocking，阈值80）               │
│  ├── Python: pytest/bandit/flake8                       │
│  └── LLM: 逻辑评审（可选）                              │
│                                                          │
│  Gate 4: 交付质量门禁（Blocking，阈值85）               │
│  ├── Python: Checklist/文档                            │
│  └── 人工: 最终确认                                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 调用链路

```
┌─────────────────────────────────────────────────────────────────────┐
│  Agent (dev-workflow-orchestration)                                 │
│  │                                                                  │
│  ├─ 加载 Memory 上下文                                             │
│  ├─ 判断当前所处阶段                                                │
│  ├─ 确认准入条件满足                                                │
│  │                                                                  │
│  ▼                                                                  │
│  直接调用 Python 脚本:                                              │
│    python check_<gate>.py <参数> --config config.yaml --json       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  check_*.py (质量门禁脚本)                                          │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  1. 自动发现 change-id                                        │   │
│  │  2. 执行 Python 自动化检查                                    │   │
│  │  3. 调用 llm_enhancer.py 进行 LLM 语义增强                   │   │
│  │  4. 返回 JSON 结果                                             │   │
│  └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘

## Gate 与 Step 对应关系

| Step | 阶段 | 应调用的脚本 | 严格度 |
|------|------|-------------|--------|
| 2 | PRD评审 | `check_prd.py` | Blocking |
| 4 | 方案评审 | `check_solution.py` | Warning |
| 6 | 代码评审 | `check_code.py` | Blocking |
| 8 | 归档 | `check_delivery.py` | Blocking |

## 配置

### 1. 环境变量

在 `.env` 中配置 API 密钥：

```bash
SILICONFLOW_API_KEY=your_key
MINIMAX_API_KEY=your_key
```

### 2. 模型配置

编辑 `config.yaml` 中的路由配置：

```yaml
models:
  routing:
    prd_review: "kimi-k2.5"
    solution_review: "kimi-k2.5"
    code_review: "minimax-m2.7"
    default: "qwen3-8b"
```

### 3. 安装依赖

```bash
pip install pyyaml pytest bandit flake8 pytest-cov
```

## 使用方法

### 直接运行

```bash
# PRD 质量门禁
python check_prd.py <prd_file> --json

# 方案质量门禁
python check_solution.py <solution_file> --json

# 代码质量门禁
python check_code.py <project_dir> --json

# 交付质量门禁
python check_delivery.py <change_id> --project <project_dir> --json
```

### 启用 LLM 增强

```bash
python check_prd.py <prd_file> --llm --json
```

### 使用统一入口

```bash
python run_gates.py prd <prd_file>
python run_gates.py solution <solution_file>
python run_gates.py code <project_dir>
python run_gates.py delivery <change_id> --project <project_dir>
python run_gates.py all <project_dir> --change-id <change_id>
```

## 输出示例

### JSON 输出

```json
{
  "gate": "交付质量门禁",
  "score": 160.0,
  "threshold": 85,
  "passed": false,
  "requires_human_confirmation": true,
  "human_confirmation_received": false,
  "checks": [
    {
      "item": "验收 Checklist",
      "passed": false,
      "score": 0,
      "details": "未找到: ...验收Checklist.md"
    }
  ]
}
```

### CLI 文本输出

```
============================================================
🚪 交付质量门禁
============================================================
总分: 160.0/100 (阈值: 85)
严格度: blocking
状态: ⏳ 待人工确认
```

## 门禁阈值与严格度

| 门禁 | 阈值 | 严格度 | 说明 |
|------|------|--------|------|
| PRD 质量 | 80 | Blocking | 不通过无法进入方案设计 |
| 方案质量 | 75 | Warning | 不通过提示警告，但可继续 |
| 代码质量 | 80 | Blocking | 不通过无法进入验收 |
| 交付质量 | 85 | Blocking | 不通过无法归档 |

## 文件结构

```
quality-gates/
├── config.yaml              # 门禁配置（阈值/权重/模型路由）
├── model_selector.py         # 模型选择器
├── llm_enhancer.py          # LLM 语义增强
├── check_prd.py             # PRD 质量门禁
├── check_solution.py         # 方案质量门禁
├── check_code.py            # 代码质量门禁
├── check_delivery.py        # 交付质量门禁
├── run_gates.py             # 统一入口
├── prompts/                 # LLM Prompt 模板
│   ├── prd_review_prompt.md
│   └── solution_review_prompt.md
├── mcp-wrappers/            # MCP Server（保留备选）
│   ├── mcp_server.py
│   └── README.md
└── README.md                # 本文档
```

## 依赖全局配置

| 配置项 | 位置 |
|--------|------|
| API 密钥 | `sys-root/config/.env` |
| 模型配置 | `sys-root/config/models.json` |
