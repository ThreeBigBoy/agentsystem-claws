# agentsystem README 方案补充（详篇）

> **文档类型**：从 **README 精简版** 迁移的 **操作与方案细节**，供实施与培训使用。  
> **权威入口**：根目录 **[README.md](../README.md)**；架构与分层以 **[agentsystem-心智模型与框架设计说明书.md](./agentsystem-心智模型与框架设计说明书.md)** 为准。  
> **路径约定**：业务项目侧 Agent 配置目录名以仓库为准（常见为 **`claw-config/`**）；下文若出现历史路径 **`devclaw-config`**，请等价替换为当前仓库实际目录名。

---

## 1. 项目简介（扩展）

Agent DevClaw System（`agentsystem`）是一套 **轻量级、可复用** 的 AI 辅助研发治理壳：在 **Cursor** 中以 **规则提示层 + Python 强制层（可选）** 组合，约束 Agent **先读规则、再改仓**。

### 1.1 核心特点（对照表）

| 特点 | 说明 |
|------|------|
| **轻量** | 无独立业务后端；依托 Cursor 与本地脚本。 |
| **可复用** | `sys-root` 技能/记忆、`usr-rules` 流程可跨多业务项目复用。 |
| **可强制** | `agents-md-enforcer` 可在业务项目场景下对「未读 AGENTS」等风险做阻断（以脚本实现为准）。 |
| **可扩展** | 业务仓 `claw-config` 内可扩展技能、工具与运行时文档。 |

---

## 2. 架构示意：Hybrid 三层（概念）

> 与《心智模型》中的 **系统层 / 用户层 / 项目层** 互补；此处强调 **IDE ↔ 检查脚本 ↔ 门禁策略** 的纵向关系。

```
┌─────────────────────────────────────────┐
│         交互层（Cursor IDE）             │
│  ├── 自然语言 / 任务                    │
│  ├── Agent 理解与工具调用               │
│  └── 规则入口（.mdc 等）                │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         检查层（Python，可选）            │
│  ├── 形式检查（结构 / 关键词等）        │
│  └── 强制验证（未通过可阻断）           │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         控制层（质量门禁 · 规划口径）      │
│  ├── Gate：PRD / 方案 / 代码 / 交付     │
│  └── 具体阈值与脚本以仓库实现为准       │
└─────────────────────────────────────────┘
```

---

## 3. 目录结构（详版示例）

> 与 **§1.4.1** 心智模型文档一致处不再重复；此处保留 **门禁脚本文件级** 展开，便于上手。

```
agentsystem/
├── .cursor/
│   └── rules/
│       └── AGENT.mdc
├── docs/
│   ├── agentsystem-心智模型与框架设计说明书.md
│   ├── AGENTS-md-职责区分说明.md
│   └── agentsystem-README-方案补充.md    # 本文
├── sys-root/
│   └── lib/
│       ├── skills/
│       ├── memory/
│       └── scripts/
│           └── agents-md-enforcer/
│               ├── agents_md_enforcer.py
│               ├── enforcer.py
│               ├── config.yaml
│               └── README.md
├── usr-devclaw/
│   ├── user.json
│   └── usr-rules/
│       ├── OpenSpec.md
│       └── PROJECT-CONFIG.md
└── workspace/
    └── <项目键> -> <业务仓库>/claw-config/
```

---

## 4. 快速开始（详版）

### 4.1 环境准备

```bash
python3 --version   # 建议 3.10+

# 门禁测试可能用到的依赖（以 enforcer 目录 README / 脚本为准）
pip install pytest pytest-cov bandit flake8 pyyaml
```

### 4.2 创建 workspace 软链

```bash
# 示例：将本机业务仓库的 claw-config 链到 agentsystem/workspace
mkdir -p /path/to/agentsystem/workspace

ln -s /path/to/your-repo/claw-config \
      /path/to/agentsystem/workspace/<项目键>

ls -la /path/to/agentsystem/workspace/<项目键>
```

`<项目键>` 须与 **`agents-md-enforcer` 配置/约定** 中的项目名一致（如 `curiobuddy`）。

### 4.3 准备 `AGENTS.md`（示例）

以下 YAML + 正文 **仅为演示结构**；实际人设与禁区以业务为准。

```bash
cat > /path/to/your-repo/claw-config/AGENTS.md << 'EOF'
---
role: "示例角色"
responsibilities:
  - 说明职责一
  - 说明职责二
tools:
  - tool-a
constraints:
  - 说明禁区或语气
---

# 项目 Agent 配置

## 角色定位
（正文）

## 操作规范
- 规范一
- 规范二
EOF
```

### 4.4 验证强制检查

**方式 A：测试脚本**

```bash
cd /path/to/agentsystem/sys-root/lib/scripts/agents-md-enforcer
python3 test-enforcer.py <项目键>   # 若仓库提供该脚本；名称以目录内为准
```

**方式 B：`quick_enforce`（需 PYTHONPATH）**

若已将 `.../agents-md-enforcer` 加入 `PYTHONPATH`：

```bash
python3 -c 'from agents_md_enforcer import quick_enforce; quick_enforce("<项目键>")'
```

单次会话可：

```bash
export PYTHONPATH="/path/to/agentsystem/sys-root/lib/scripts/agents-md-enforcer${PYTHONPATH:+:$PYTHONPATH}"
python3 -c 'from agents_md_enforcer import quick_enforce; c = quick_enforce("<项目键>"); print("OK, role=", repr(c.role))'
```

**说明**：`role` 为空字符串时，多为 **frontmatter 未配置 `role:`**，不一定表示脚本失败；详见根 README 与 enforcer 文档。

**方式 C：CLI**

```bash
python3 /path/to/agentsystem/sys-root/lib/scripts/agents-md-enforcer/enforcer.py <项目键>
```

---

## 5. 使用方式（场景）

### 5.1 在 Cursor 中结合门禁表述

在对话中可显式带项目名与任务，便于 Agent 对齐 `workspace` 与 `AGENTS.md`（具体触发词以实现为准）。

### 5.2 命令行直接检查

```bash
python3 /path/to/agentsystem/sys-root/lib/scripts/agents-md-enforcer/enforcer.py <项目键>
# 若支持列表：
# python3 .../enforcer.py --list
```

### 5.3 在 Python 中调用

```python
import sys
from pathlib import Path

ROOT = Path("/path/to/agentsystem/sys-root/lib/scripts/agents-md-enforcer")
sys.path.insert(0, str(ROOT))

from agents_md_enforcer import quick_enforce, EnforcementError

try:
    config = quick_enforce("<项目键>")
    print("角色:", config.role)
except EnforcementError as e:
    print("检查失败:", e)
```

---

## 6. 质量门禁（规划口径 · 须与实现对齐）

> 下表为 **早期 README 中的目标化描述**，用于产品沟通；**实际阈值、是否 Blocking、是否已接入 LangGraph/OpenSpec**，以 **`agents-md-enforcer/config.yaml`**、**业务 openspec** 与 **当前脚本** 为准。

| 门禁 | 严格度（示意） | 检查侧重（示意） |
|------|------------------|------------------|
| PRD 质量 | Blocking | 结构 / 完整性等 |
| 方案质量 | Warning | 与 PRD 对齐等 |
| 代码质量 | Blocking | 测试 / 安全 / 规范等 |
| 交付质量 | Blocking | Checklist / 可部署验证等 |

### 6.1 触发关键词（治理内核常见约定 · 摘录）

- **对象类**：如 `提案`、`需求`、`change-id`、`迭代` 等（以 OpenSpec 为准）。  
- **执行类**：如 `推进`、`落实`、`执行`、`完成`、`验收`、`测试`、`归档`、`发布` 等。  

具体是否自动触发运行后端或门禁，见业务项目 **`openspec/AGENTS.md`** 与 **`usr-devclaw/usr-rules/OpenSpec.md`**。

---

## 7. 核心概念（补充）

### 7.1 `AGENTS.md` 职责分层

| 文件 | 层级 | 用途 |
|------|------|------|
| `openspec/AGENTS.md` | 治理层 | 变更流程、质量标准、与 usr-rules 的指针关系 |
| `claw-config/AGENTS.md` | 运行时层 | 人设、禁区、沟通方式（项目身份） |

**原则**：治理标准 ≠ 运行时配置，二者互补、避免全文重复。

### 7.2 软链接设计

- 业务仓库内 **`claw-config/`** 与代码 **同库版本管理**。  
- **`agentsystem/workspace/<项目键>`** 指向该目录，供宿主与脚本 **统一发现** 配置。  
- 新成员 clone 业务仓即拥有配置；CI 可按同一约定挂载 `agentsystem` 后做检查。

### 7.3 Hybrid：提示 vs 强制

```
.cursor/rules/AGENT.mdc     → 提示「应先读什么」
agents-md-enforcer          → 可选强制「是否已满足最低约定」
```

---

## 8. 自定义扩展（摘要）

### 8.1 业务侧技能目录

在业务仓库 `claw-config/`（或约定路径）下增加技能包与 `SKILL.md`，并在 `AGENTS.md` 中引用（细节见项目自身约定）。

### 8.2 门禁配置示例

编辑 `sys-root/lib/scripts/agents-md-enforcer/config.yaml`（字段以文件为准），例如：

```yaml
enforcement:
  require_agents_md: true
  require_role: true
  min_responsibilities: 1

messages:
  agents_md_not_found: "必须读取 AGENTS.md 才能执行任务"
```

---

## 9. 常见问题（FAQ）

**Q：为什么需要强制检查 AGENTS.md？**  
A：降低 Agent 在未建立项目上下文与禁区的情况下改仓的风险。

**Q：软链与复制一份配置有何区别？**  
A：软链指向 **唯一真相**；复制易漂移。

**Q：多项目能否共用同一份 claw-config？**  
A：一般 **不建议**；每项目应有独立人设与禁区。多项目可 **共用** `agentsystem` 内核与 `usr-devclaw`（独立开发者角色），见《心智模型》。

**Q：门禁失败怎么办？**  
A：按报错与 `openspec`/任务清单修正确认项后重试；Blocking 未通过则不应进入下一阶段。

---

## 10. 相关文档

- [README.md](../README.md)（精简入口）  
- [agentsystem-心智模型与框架设计说明书.md](./agentsystem-心智模型与框架设计说明书.md)  
- [AGENTS-md-职责区分说明.md](./AGENTS-md-职责区分说明.md)  
- [usr-devclaw/usr-rules/OpenSpec.md](../usr-devclaw/usr-rules/OpenSpec.md)  
- 框架级演进与复盘：以 **`usr-devclaw/usr-rules`**、`sys-root/lib/memory/` 下 pattern 为准。

---

## 11. 维护说明

- **来源**：本文自 **2026-03-22 前** 根 `README.md` 详版整理迁移，后续 **以根 README + 心智模型文档** 为纲增量更新。  
- **冲突处理**：若与 `README.md`、`user.json`、`usr-rules` 冲突，以后者及 OpenSpec 权威层为准修订本文。

---

*文档版本：1.0 | 2026-03-22*
