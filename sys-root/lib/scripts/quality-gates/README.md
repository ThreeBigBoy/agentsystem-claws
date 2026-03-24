# 质量门禁使用指南

## 概述

Hybrid 质量门禁（Python + LLM）是一套量化验证 PRD/方案/代码/交付质量的工具集。

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
│  Agent (会话中自主推进 dev-workflow-orchestration)                    │
│  │                                                                  │
│  ├─ 加载 Memory 上下文                                             │
│  ├─ 判断当前所处阶段                                                │
│  ├─ 确认准入条件满足                                                │
│  │                                                                  │
│  ▼                                                                  │
│  调用 MCP: quality-gates.check_xxx  ← 无需传参                     │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Trae (MCP Client)                                                 │
│  读取 ~/Library/Application Support/Trae CN/User/mcp.json          │
│  启动 mcp_server.py                                                 │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  mcp_server.py (MCP Server SDK)                                     │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  1. 自动发现 change-id                                        │   │
│  │     从 cwd 向上查找 openspec/changes/<change-id>              │   │
│  │                                                               │   │
│  │  2. 动态构建路径                                              │   │
│  │     - PRD: docs/project-prd-changes/{id}/PRD-{id}-功能需求.md │   │
│  │     - SOLUTION: openspec/changes/{id}/proposal.md            │   │
│  │     - CODE: {project}/src                                    │   │
│  │     - DELIVERY: --project {project} --change-id {id}         │   │
│  │                                                               │   │
│  │  3. 调用 check_*.py 执行实际检查                              │   │
│  └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  check_*.py (质量门禁脚本)                                          │
│  执行 Python 自动化检查 + LLM 语义增强                               │
│  输出 JSON 格式结果                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## MCP 工具列表

| 工具 | 说明 | 对应阶段 |
|------|------|----------|
| `quality-gates.check_prd` | PRD 质量门禁检查 | Step 2 PRD评审 |
| `quality-gates.check_solution` | 方案质量门禁检查 | Step 4 方案评审 |
| `quality-gates.check_code` | 代码质量门禁检查 | Step 6 代码评审 |
| `quality-gates.check_delivery` | 交付质量门禁检查 | Step 8 归档 |
| `quality-gates.gate_status` | 查询当前所处阶段 | - |

## Gate 与 Step 对应关系

| Step | 阶段 | 应调用的 Gate | MCP 工具 |
|------|------|--------------|----------|
| 1 | 需求分析 | 无 | - |
| 2 | PRD评审 | Gate-PRD | `quality-gates.check_prd` |
| 3 | 技术方案 | 无 | - |
| 4 | 方案评审 | Gate-DESIGN | `quality-gates.check_solution` |
| 5 | 编码实现 | 无 | - |
| 6 | 代码评审 | Gate-CODE | `quality-gates.check_code` |
| 7 | 功能验收 | 无 | - |
| 8 | 归档 | Gate-DELIVERY | `quality-gates.check_delivery` |

## 配置

### 1. 环境变量

配置 API 密钥（使用全局配置）：

```bash
# 复制全局配置
cp /Users/billhu/agentsystem/sys-root/config/.env.example /Users/billhu/agentsystem/sys-root/config/.env

# 编辑填入 API Key
vim /Users/billhu/agentsystem/sys-root/config/.env
```

### 2. 模型配置

模型路由在 `config.yaml` 中定义，引用 `sys-root/config/models.json`：

| 任务 | 模型别名 | 说明 |
|------|---------|------|
| prd_review | heavy | 高质量模型 |
| solution_review | heavy | 高质量模型 |
| code_review | fast | 快速模型 |

可用别名：`fast`、`heavy`

### 3. 安装依赖

```bash
pip install pyyaml pytest bandit flake8 pytest-cov mcp
```

### 4. MCP 配置

在 `~/Library/Application Support/Trae CN/User/mcp.json` 中配置：

```json
{
  "mcpServers": {
    "quality-gates": {
      "command": "python",
      "args": [
        "/Users/billhu/agentsystem/sys-root/lib/scripts/quality-gates/mcp-wrappers/mcp_server.py"
      ]
    }
  }
}
```

## 使用方法

### MCP 工具调用（Trae）

Agent 在 dev-workflow-orchestration 技能中自主调用，无需传参：

```python
# 查询当前状态
quality-gates.gate_status

# PRD 门禁检查
quality-gates.check_prd

# 方案门禁检查
quality-gates.check_solution

# 代码门禁检查
quality-gates.check_code

# 交付门禁检查
quality-gates.check_delivery
```

### 单独运行各门禁（CLI）

```bash
# PRD 质量门禁
python check_prd.py <prd_file>

# 方案质量门禁
python check_solution.py <solution_file> --prd <prd_file>

# 代码质量门禁
python check_code.py <project_dir>

# 交付质量门禁
python check_delivery.py <change_id> --project <project_dir>
```

### 使用统一入口

```bash
python run_gates.py prd <prd_file>
python run_gates.py solution <solution_file> --prd <prd_file>
python run_gates.py code <project_dir>
python run_gates.py delivery <change_id> --project <project_dir> --confirm
python run_gates.py all <project_dir> --change-id <change_id>
```

## 输出示例

### MCP JSON 输出

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

检查项详情:
  ❌ [0.0] 验收 Checklist
      未找到: ...验收Checklist.md
  ❌ [60.0] 可部署/可运行
      基础交付物检查: README
  ❌ [50.0] 文档完整
      必需文档: 1/2
  ✅ [50.0] 变更记录完整
      变更记录: 项目日志
============================================================
```

## 门禁阈值与严格度

| 门禁 | 阈值 | 严格度 | 说明 |
|------|------|--------|------|
| PRD 质量 | 80 | Blocking | 不通过无法进入方案设计 |
| 方案质量 | 75 | Warning | 不通过提示警告，但可继续 |
| 代码质量 | 80 | Blocking | 不通过无法进入验收 |
| 交付质量 | 85 | Blocking | 不通过无法归档 |

## 评分权重

### PRD 质量
- 结构完整性: 30%
- 验收标准明确性: 25%
- 功能点可追踪性: 20%
- 产品逻辑完整性: 15% (LLM)
- 设计合理性: 10% (LLM)

### 方案质量
- PRD 对应性: 35%
- 接口定义清晰: 25%
- 技术选型合理: 20%
- 风险识别: 15% (LLM)
- 可实施性: 5% (LLM)

### 代码质量
- 功能实现完整: 40%
- 无明显安全漏洞: 25%
- 代码规范: 15%
- 单元测试覆盖: 15%
- 代码逻辑评审: 5% (LLM)

### 交付质量
- 验收 Checklist: 40%
- 可部署/可运行: 30%
- 文档完整: 15%
- 变更记录完整: 10%
- 人工确认: 5%

## 费用估算

| LLM 调用 | 单次成本 | 频率 | 月成本 | 年成本 |
|----------|----------|------|--------|--------|
| PRD 评审 | $0.03 | 2次/项目 | $0.06 | $0.72 |
| 方案评审 | $0.03 | 2次/项目 | $0.06 | $0.72 |
| 代码评审 | $0.02 | 可选 | - | - |
| **总计** | - | - | - | **~$1.5/年** |

## 文件结构

```
quality-gates/
├── config.yaml              # 门禁配置（阈值/权重/模型路由）
├── model_selector.py         # 模型选择器（引用 sys-root/config/models.json）
├── llm_enhancer.py          # LLM 语义增强
├── check_prd.py             # PRD 质量门禁
├── check_solution.py         # 方案质量门禁
├── check_code.py            # 代码质量门禁
├── check_delivery.py        # 交付质量门禁
├── run_gates.py             # 统一入口
├── prompts/                 # LLM Prompt 模板
│   ├── prd_review_prompt.md
│   └── solution_review_prompt.md
├── mcp-wrappers/            # MCP Server
│   ├── mcp_server.py        # MCP 服务器（自动发现 change-id）
│   ├── mcp_config.yaml      # MCP 配置
│   └── README.md            # MCP 使用说明
└── README.md                # 本文档
```

## 依赖全局配置

| 配置项 | 位置 |
|--------|------|
| API 密钥 | `sys-root/config/.env` |
| 模型配置 | `sys-root/config/models.json` |
