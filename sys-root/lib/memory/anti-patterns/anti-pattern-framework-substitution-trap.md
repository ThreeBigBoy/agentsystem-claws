---
id: anti-pattern-framework-substitution-trap
title: 框架替代陷阱（用代码框架替代实际实现）
type: anti-pattern
description: 用代码框架和占位符替代实际功能实现，导致技术方案看似完整但实际无法直接开发
description_long: |
  一种危险的技术方案设计陷阱：用代码框架、TODO注释、空函数替代实际功能实现。
  表面上技术方案"完成"了，但实际上缺少核心调用逻辑，无法直接投入开发。
applicable_projects:
  - agentsystem
  - "*"
tags:
  - 反模式
  - 技术方案
  - 质量陷阱
  - 完成度陷阱
related:
  - pattern-systematic-technical-design-review
  - pattern-multi-round-self-review
  - anti-pattern-optimistic-evaluation-bias
created_by: 复盘-deepen-langgraph-v2-11-1-技术方案评审过程
created_date: 2026-03-18
version: 1.0
---

# 框架替代陷阱（用代码框架替代实际实现）

## 一句话定义

用代码框架和占位符替代实际功能实现，导致技术方案看似完整但实际无法直接开发的危险陷阱。

## 反模式表现

### 典型症状

```
┌─────────────────────────────────────────────────────────────┐
│                    框架替代陷阱的典型症状                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  症状 1: TODO占位符泛滥                                        │
│  ```python                                                   │
│  async def step1_request_analysis(state: AgentStateV2) -> dict:  │
│      # TODO: 调用产品经理Agent执行需求分析                     │
│      # TODO: 读取proposal.md                                    │
│      # TODO: 生成PRD                                          │
│      # TODO: 保存PRD到标准位置                                  │
│      return {"status": "completed"}                            │
│  ```                                                         │
│  → 看起来有函数，实际没有实现                                    │
│                                                              │
│  症状 2: 空函数占位                                             │
│  ```python                                                   │
│  class AgentInvoker:                                         │
│      async def invoke(self, ...):                            │
│          # 这里应该调用Agent                                    │
│          pass                                                │
│  ```                                                         │
│  → 有类有方法，实际不能调用                                     │
│                                                              │
│  症状 3: 伪实现                                                │
│  ```python                                                   │
│  async def _internal_request_analysis(...):                │
│      # 简化实现                                                │
│      return {"output": "分析完成", "artifacts_created": []}     │
│  ```                                                         │
│  → 返回假数据，没有真实逻辑                                     │
│                                                              │
│  症状 4: 框架检查替代实际执行                                    │
│  ```python                                                   │
│  async def step1_request_analysis(state: AgentStateV2) -> dict:  │
│      # 检查PRD是否存在                                         │
│      prd_exists = check_prd_exists()                         │
│      return {"status": "completed" if prd_exists else "waiting"}  │
│  ```                                                         │
│  → 只检查产出物是否存在，不执行实际生成                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 危害

| 危害 | 影响 | 后果 |
|-----|------|------|
| 开发受阻 | 无法直接投入开发 | 需要重新设计和实现 |
| 时间浪费 | 评估和补充成本高 | 项目延期 |
| 质量风险 | 实现时可能遗漏 | 系统缺陷 |
| 信任损失 | 评估不准确 | 用户失去信任 |

## 避免方法

### 识别框架替代的方法

```python
# 检查清单：如何识别框架替代

def check_framework_substitution(code_snippet: str) -> dict:
    """
    检查代码是否存在框架替代陷阱
    
    Returns:
        {"is_framework": bool, "issues": [], "suggestions": []}
    """
    issues = []
    
    # 检查1: TODO注释
    if "# TODO" in code_snippet or "TODO:" in code_snippet:
        issues.append("发现TODO注释，需要实现具体逻辑")
    
    # 检查2: 空函数（pass）
    if re.search(r'def \w+\([^)]*\):\s*\n\s*pass', code_snippet):
        issues.append("发现空函数（pass），需要实现具体逻辑")
    
    # 检查3: 伪实现（返回假数据）
    if re.search(r'return\s*\{[^}]*"output"[^}]*\}', code_snippet):
        if "analysis" not in code_snippet and "extract" not in code_snippet:
            issues.append("发现伪实现（返回假数据），需要真实逻辑")
    
    # 检查4: 只检查不执行
    if "check_" in code_snippet and "invoke" not in code_snippet:
        issues.append("发现只检查不执行模式，需要实际调用逻辑")
    
    # 检查5: 缺少核心调用
    if "AgentRole" in code_snippet and "invoke" not in code_snippet:
        issues.append("缺少Agent调用逻辑")
    
    return {
        "is_framework": len(issues) > 0,
        "issues": issues,
        "suggestions": ["实现具体逻辑", "消除TODO", "添加真实调用"]
    }
```

### 正确的实现标准

```python
# ✅ 正确的实现：实际调用Agent生成PRD

async def step1_request_analysis(state: AgentStateV2) -> dict:
    """
    Step 1: 需求分析 - 产出 PRD
    """
    change_id = state["change_id"]
    workspace_root = Path(state.get("workspace_root", "."))
    
    # 1. 读取提案
    proposal_path = workspace_root / "openspec" / "changes" / change_id / "proposal.md"
    proposal_content = await CommonUtils.async_read_file(proposal_path)
    
    # 2. 调用Agent执行需求分析（实际调用，不是检查）
    agent_invoker = get_agent_invoker(mode="auto")
    invocation_result = await retry_policy.execute(
        lambda: agent_invoker.invoke(
            agent_role=AgentRole.PRODUCT_MANAGER,
            skill=SkillType.REQUEST_ANALYSIS,
            change_id=change_id,
            inputs={"proposal_content": proposal_content},
            workspace_root=str(workspace_root),
            timeout=600
        )
    )
    
    # 3. 验证PRD生成（实际产出物）
    prd_path = workspace_root / "design" / "documents" / "changes" / change_id / f"PRD-{change_id}.md"
    prd_generated = prd_path.exists()
    
    # 4. 返回实际执行结果
    return {
        "current_step": "step1_request_analysis",
        "status": "completed" if invocation_result["success"] and prd_generated else "failed",
        "agent_invocation": invocation_result,
        "outputs": {
            "prd_path": str(prd_path) if prd_generated else None,
            "prd_generated": prd_generated
        }
    }
```

### 验证检查清单

```markdown
## 框架替代陷阱检查清单

### 代码实现检查
- [ ] 没有TODO注释
- [ ] 没有空函数（pass）
- [ ] 没有伪实现（返回假数据）
- [ ] 有实际的调用逻辑
- [ ] 有实际的产出物生成

### 逻辑完整性检查
- [ ] 输入处理逻辑完整
- [ ] 核心处理逻辑完整
- [ ] 输出生成逻辑完整
- [ ] 错误处理逻辑完整
- [ ] 边界条件处理完整

### 可执行性检查
- [ ] 代码可以直接运行
- [ ] 有实际产出物
- [ ] 可以验证执行结果
- [ ] 异常时能够定位问题
```

## 真实案例

### 案例: deepen-langgraph-v2-11-1技术方案评审

**问题发现过程**:

| 轮次 | 用户问题 | 发现的问题 | 实际情况 |
|-----|---------|-----------|---------|
| 首轮 | "技术方案是否还有错漏？" | 自评95% | 实际85% |
| 深挖 | "为什么不是100%？" | TODO替代 | 有框架无实现 |
| 改进 | "请补充完整" | 发现框架陷阱 | 补充实际调用 |

**框架陷阱实例**:

```python
# ❌ 框架替代（首轮）
async def step1_request_analysis(state: AgentStateV2) -> dict:
    # TODO: 调用产品经理Agent执行需求分析
    # TODO: 读取proposal.md获取变更基本信息
    # TODO: 产出PRD
    hook_result = await pre_step_hook(state, "step1_request_analysis")
    return {
        "status": "completed",  # 伪完成状态
        "hook_result": hook_result
    }

# ✅ 实际实现（改进后）
async def step1_request_analysis(state: AgentStateV2) -> dict:
    # 实际读取提案
    proposal_content = await CommonUtils.async_read_file(proposal_path)
    
    # 实际调用Agent
    agent_invoker = get_agent_invoker(mode="auto")
    invocation_result = await retry_policy.execute(
        lambda: agent_invoker.invoke(...)
    )
    
    # 实际验证产出物
    prd_generated = prd_file_path.exists()
    
    return {
        "status": "completed" if invocation_result["success"] and prd_generated else "failed",
        "agent_invocation": invocation_result,
        "outputs": {"prd_path": str(prd_file_path) if prd_generated else None}
    }
```

**改进成果**:
- 从框架占位到实际实现
- 从伪完成到真实完成
- 从85%到100%

---

**反模式版本**: v1.0  
**创建日期**: 2026-03-18  
**来源复盘**: deepen-langgraph-v2-11-1技术方案评审过程  
**维护者**: agentsystem架构组
