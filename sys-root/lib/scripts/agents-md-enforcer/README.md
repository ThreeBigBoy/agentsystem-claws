# agents-md-enforcer

> **定位**: Hybrid 模式中的 **enforcement（强制）层**  
> **作用**: 在执行任务前校验项目 `AGENTS.md` 是否存在且可解析；失败时抛出 `EnforcementError`，供上层（Cursor Agent / MCP / CI）阻断后续操作。

---

## 功能概览

| 能力 | 说明 |
|------|------|
| **存在性检查** | `{base_path}/{project}/claw-config/AGENTS.md` 必须存在 |
| **解析** | 支持可选 YAML frontmatter（`---` … `---`） |
| **结构化输出** | 解析为 `AgentsMdConfig`（`role` / `responsibilities` / `tools` / `constraints`） |
| **缓存** | 同一 `AgentsMdEnforcer` 实例内可记录已加载配置（`verify_loaded` / `get_config`） |
| **列举项目** | `list_projects()`：列出 `base_path` 下在 `claw-config/AGENTS.md` 存在的子目录名 |

---

## 目录与依赖

```
agents-md-enforcer/
├── README.md               # 本说明
├── __init__.py             # 包导出（若以包方式加载）
├── enforcer.py             # 核心逻辑 + 命令行入口
├── agents_md_enforcer.py   # 兼容模块名：与 enforcer 等价重导出（推荐 `from agents_md_enforcer import ...`）
├── config.yaml             # 规则与文案配置（当前版本以代码内默认值为主，可扩展接入）
└── test-enforcer.py        # 简易自测脚本
```

**Python 依赖**

- 标准库：`pathlib`、`re`、`dataclasses`、`argparse`
- 第三方：**PyYAML**（`pip install pyyaml`）

---

## 默认路径约定

| 项 | 默认值 |
|----|--------|
| **工作区根目录** `base_path` | `/Users/billhu/agentsystem/workspace` |
| **项目占位目录** | `{base_path}/{project_name}/`（workspace 下每项目一个目录） |
| **运行时配置目录** | `{base_path}/{project_name}/claw-config/`（通常为指向项目仓库内 `claw-config/` 的**软链**） |
| **AGENTS.md** | `{base_path}/{project_name}/claw-config/AGENTS.md` |

> **实际布局示例**（本机已验证）：`workspace/curiobuddy/claw-config` → `/Users/billhu/aiprojects/curiobuddy/claw-config`，其中含 `AGENTS.md`。  
> 文档中若出现 `devclaw-config/`，多指**同类「运行时配置目录」**的另一种命名；以你项目仓库内目录名为准，workspace 侧软链名需与之对应（常见为 `claw-config`）。

---

## 命令行用法

在脚本目录下执行：

```bash
cd /Users/billhu/agentsystem/sys-root/lib/scripts/agents-md-enforcer

# 检查指定项目（通过则 exit 0，失败则 exit 1）
python enforcer.py curiobuddy
```

或使用测试脚本：

```bash
python test-enforcer.py curiobuddy
# 省略参数时默认 project 为 curiobuddy
python test-enforcer.py
```

---

## 在 Python 中调用

目录名为 `agents-md-enforcer`（含连字符），**不能**作为包名 `import agents-md-enforcer`。已将兼容模块 **`agents_md_enforcer.py`** 放在本目录，加入 `PYTHONPATH` 后可按规则文档写法导入。

### 方式 A（推荐）：`agents_md_enforcer`

```python
import sys
from pathlib import Path

ROOT = Path("/Users/billhu/agentsystem/sys-root/lib/scripts/agents-md-enforcer")
sys.path.insert(0, str(ROOT))

from agents_md_enforcer import AgentsMdEnforcer, EnforcementError, quick_enforce

config = quick_enforce("curiobuddy")
print(config.role, config.responsibilities)
```

### 方式 B：直接导入 `enforcer`

与方式 A 等价，仅模块名不同。

### 方式 C：使用 `AgentsMdEnforcer` 并自定义 `base_path`

```python
from pathlib import Path
import sys
sys.path.insert(0, "/Users/billhu/agentsystem/sys-root/lib/scripts/agents-md-enforcer")

from enforcer import AgentsMdEnforcer, EnforcementError

enforcer = AgentsMdEnforcer(base_path="/Users/billhu/agentsystem/workspace")
try:
    cfg = enforcer.enforce("curiobuddy")
except EnforcementError as e:
    print(e.message)
    print(e.remediation)
```

---

## AGENTS.md 格式建议

支持 **可选** YAML frontmatter，便于结构化字段：

```markdown
---
role: "K12 教育助手"
responsibilities:
  - 帮助学生理解概念
tools:
  - content-generation
constraints:
  - 不直接给答案
---

# 正文

更多说明……
```

未包含 frontmatter 时，元数据字段为空列表/空字符串，但文件存在且可读仍可通过 `enforce()`（解析阶段不因缺 frontmatter 失败）。

---

## API 摘要

| 符号 | 说明 |
|------|------|
| `EnforcementError` | 检查失败异常；含 `message`、`remediation` |
| `AgentsMdConfig` | `role`、`responsibilities`、`tools`、`constraints`、`raw_content` |
| `AgentsMdEnforcer(base_path=...)` | 构造检查器 |
| `enforce(project_name) -> AgentsMdConfig` | 强制检查，失败抛 `EnforcementError` |
| `verify_loaded(project_name) -> bool` | 是否已在当前实例中成功加载过 |
| `get_config(project_name)` | 返回已缓存配置或 `None` |
| `list_projects() -> list[str]` | 列出在 `claw-config/AGENTS.md` 存在的项目名 |
| `quick_enforce(project_name)` | 使用默认 `base_path` 的一行封装 |

---

## 与 Cursor 规则的关系

- **`.cursor/rules/AGENT.mdc`**：提示 Agent「应先读 AGENTS.md」——属于 **提示层**。  
- **本脚本**：可被 Agent、MCP、CI 显式调用，用 **退出码 / 异常** 表达是否通过——属于 **强制层**。

两者配合即为 Hybrid 模式；仅依赖 `.mdc` 无法从技术上禁止模型改文件，**强制阻断需在调用链中执行本检查**（或等价逻辑）。

---

## 常见问题

**Q: 为什么 `from agents_md_enforcer import …` 仍报错？**  
A: 须先将本目录（`.../agents-md-enforcer`）加入 `sys.path`，或在该目录下执行 Python；仓库已提供 **`agents_md_enforcer.py`** 重导出，无需再改包名。若仍失败，检查是否误从其他工作目录 import 或未插入正确路径。

**Q: `enforcer.py` 里的 `--check-only` 有什么效果？**  
A: 当前实现中该参数已注册但未改变分支逻辑；实际行为与不带该参数一致。若需「只打印结果不退出非 0」，可在后续版本实现。

**Q: `config.yaml` 是否已接入 `enforcer.py`？**  
A: 当前以代码内默认值为主；`config.yaml` 可作为后续扩展（消息文案、`base_path` 覆盖等）的配置源。

---

## 版本

- **1.0.0**（与 `__init__.py` 中 `__version__` 对齐）

---

## 相关文档

- 系统总览：`/Users/billhu/agentsystem/README.md`
- Cursor 侧约定：`/Users/billhu/agentsystem/.cursor/rules/AGENT.mdc`
