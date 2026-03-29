# 经验沉淀：质量门禁分层设计教训

**日期**: 2026-03-29
**触发场景**: curiobuddy v0.1beta PRD/方案评审
**标签**: #经验沉淀 #分层设计 #DRY #测试设计

---

## 问题概述

在实现质量门禁两层判断机制时，犯了几个原则性错误：

1. **分层职责混淆** - 第一层判断逻辑被错误放在第二层实现
2. **DRY 违背** - 共同逻辑在3个文件重复
3. **Prompt传递错误** - Agent/API模式处理不一致
4. **测试设计错误** - 测试用例绕过架构设计

---

## 详细复盘

### 问题1：分层职责混淆

**现象**：`llm_enhancer.py` 中有 `_should_skip_llm` 死代码，从未被调用

**根因**：
- 设计意图：第一层判断（是否使用LLM）由 `check_*.py` 处理
- 错误实现：部分第一层逻辑被错误放在 `llm_enhancer.py` 中

**教训**：
```
Layer 1 (check_*.py) → Layer 2 (llm_enhancer.py)
     ↓                        ↓
  第一层判断              第二层判断
  "是否使用LLM"          "Agent还是API"
```

每层只做本层职责，不能越界。测试必须尊重架构设计，不能绕过层级。

---

### 问题2：DRY 违背

**现象**：`_should_skip_llm()` 在 `check_prd.py`, `check_solution.py`, `check_code.py` 三个文件重复

**影响**：
- 修改一个关键词需要改3个文件
- 容易遗漏
- 新增字段（如 `source`）需要改3处

**教训**：
- 共同逻辑必须抽象到共享模块
- Mixin/基类 是代码复用的正确方式

**重构方案**：
```python
# llm_helper.py
class LLMHelperMixin:
    def _should_skip_llm(self): ...
    def _llm_analysis(self, ...): ...
    def _format_json_output(self, ...): ...
    def _print_result(self, ...): ...

# check_*.py
class PRDChecker(LLMHelperMixin): ...
class SolutionChecker(LLMHelperMixin): ...
class CodeChecker(LLMHelperMixin): ...
```

---

### 问题3：Prompt传递错误

**现象**：API评审失败，返回的是Agent的prompt而非实际评审结果

**根因**：API模式下仍然传递 `file_path` 而不是 `content`

**教训**：
| 模式 | 正确做法 |
|------|---------|
| Agent模式 | 传 `file_path`，让Agent读取文件 |
| API模式 | 传 `content`，直接传内容给API |

**代码示例**：
```python
# ❌ 错误：API模式也传file_path
prompt = self._get_prompt(content, file_path)

# ✅ 正确：分开处理
if not self._should_use_api(user_input):  # Agent模式
    return self._agent_fallback(task, content, result, file_path)
else:  # API模式
    prompt = self._get_prompt(content)  # 只传content
```

---

### 问题4：测试设计错误

**现象**：测试用例期望从 `llm_enhancer` 返回 `python_only`

**根因**：混淆了第一层和第二层的边界

**教训**：
- 测试必须基于**架构设计**，而非实现便利
- 单元测试验证单元，集成测试验证协作
- 不能为了"测试通过"而破坏分层

**正确测试分层**：
```
测试第一层 → 调用 check_*.py，验证是否跳过LLM
测试第二层 → 调用 llm_enhancer，验证Agent/API分支
```

---

## 架构约束（强制）

### 5.1 分层设计原则

**强制规则**：
1. `check_*.py` 负责第一层判断（是否使用LLM）
2. `llm_enhancer.py` 负责第二层判断（Agent还是API）
3. 不得跨层调用或混合逻辑

### 5.2 DRY原则

**强制规则**：
1. 共同逻辑必须抽象到 `llm_helper.py`
2. 三个 `check_*.py` 只保留业务逻辑（检查项）
3. 修改共同逻辑只需改一处

### 5.3 Prompt传递原则

**强制规则**：
1. Agent模式：传递 `file_path`，让Agent读取文件
2. API模式：传递 `content`，直接传内容给API

### 5.4 测试设计原则

**强制规则**：
1. 测试基于架构设计，不基于实现便利
2. 分层测试：每层独立验证
3. 集成测试验证层间协作

---

## 沉淀位置

| 类型 | 位置 |
|------|------|
| 代码实现 | `references/quality-gates/llm_helper.py` |
| 测试验证 | `scripts/test_quality_gates/test_quality_gates_full.py` |

---

## 触发记忆

当遇到以下场景时，自动唤醒此记忆：
- 实现新的质量门禁脚本
- 修改两层判断逻辑
- 设计新的分层架构
- 编写涉及LLM调用的测试
