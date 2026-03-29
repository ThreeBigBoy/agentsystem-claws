# 质量门禁执行确定性改进方案（精简版）

## 修订历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-03-29 | 精简版，仅保留改进点 1, 6, 7 |

---

## 1. 背景

在执行 curiobuddy v0.1beta 的 PRD 评审和技术方案评审时，Agent 只执行了 `check_*.py` 脚本，跳过了 Skill 评审环节。

**根因**：SKILL.md 定义了"强制"执行顺序，但没有检测机制来确保执行。

### 1.1 为什么需要精简版

**完整版改进点（共 8 个）**：

| # | 改进点 | 有效性 |
|---|--------|--------|
| 1 | L182-183 歧义优化 | 低 |
| 2 | 触发机制 | 低 |
| 3 | 校验机制 | 中 |
| 4 | 跳过后果 | 中 |
| 5 | 异常处理 | 低 |
| 6 | check_*.py 警告 | **高** |
| 7 | 综合判定执行保障 | **高** |
| 8 | 综合判定 vs Gate 确认 | 低 |

**ROI 评估结论**：

| 类型 | 改进点 | 问题 |
|------|--------|------|
| **文档定义** | 改进点 1-5, 8 | 描述"应该怎么做"，但 Agent 可以不遵守 |
| **检测机制** | 改进点 6 | 能检测"是否跳过了"，有效 |
| **执行保障** | 改进点 7 | 能确保"关键步骤执行"，有效 |

**精简原则**：只实施真正有效的改进点，文档优化暂缓。

### 1.2 精简版保留的改进点

| # | 改进点 | 保留理由 |
|---|--------|---------|
| 1 | L182-183 歧义优化 | 中优先级，描述优化 |
| 6 | check_*.py 警告 | **高优先级，直接解决 Skill 跳过问题** |
| 7 | 综合判定执行保障 | **高优先级，确保关键步骤执行** |

---

## 2. 改进点汇总

| # | 改进点 | 有效性 | 说明 |
|---|--------|--------|------|
| **1** | **L182-183 歧义优化** | 中 | 明确三步执行顺序 |
| **6** | **check_*.py 警告** | **高** | **检测 Skill 跳过问题** |
| **7** | **综合判定执行保障** | **高** | **确保关键步骤执行** |

---

## 3. 改进点 1：L182-183 歧义优化

### 问题

```markdown
**⚠️ 关键约束：评审类阶段必须严格遵循「先Agent评审后量化检查」的执行顺序**
```

- 只描述了 2 个步骤（Agent评审 + 量化检查）
- 遗漏了"综合判定"环节
- Step 4 的双 Skill 结构与描述不符

### 方案

替换为：

```markdown
**⚠️ 关键约束：评审类阶段必须严格遵循「Skill评审 → 量化评分 → 综合判定」的执行顺序**

**各阶段完整执行步骤**：
- Step 2（PRD评审）：prd-review Skill → check_prd.py → 综合判定 → Gate-PRD确认
- Step 4（方案评审）：architecture-review + technical-design-review Skill（双 Skill） → check_solution.py → 综合判定 → Gate-DESIGN确认
- Step 6（代码评审）：code-review Skill → check_code.py → 综合判定 → Gate-代码确认
```

### 涉及文件

- `SKILL.md` L182-183

---

## 4. 改进点 6：check_*.py 强制校验警告

### 问题

Agent 可能直接调用 check_*.py 绕过 Skill 评审，且无检测机制。

### 方案

在 `check_*.py` 执行时，自动检测 Skill 评审纪要是否存在：

| 情况 | 处理 |
|------|------|
| 评审纪要存在 | 输出 ✅ 已找到，继续执行 |
| 评审纪要不存在 | 输出 ⚠️ 警告，但不阻止执行 |

### 4.1 llm_helper.py 新增代码

```python
class LLMHelperMixin:
    REVIEW_RECORD_PATTERNS = {
        "prd": [
            r"records?/PRD-.*评审纪要.*\.md",
            r"records?/PRD评审纪要\.md",
        ],
        "solution": [
            r"records?/architecture-review.*评审纪要.*\.md",
            r"records?/technical-design-review.*评审纪要.*\.md",
        ],
        "code": [
            r"records?/code-review.*评审纪要.*\.md",
        ]
    }

    def _find_project_root(self, file_path: str) -> Optional[Path]:
        path = Path(file_path).resolve()
        for parent in [path] + list(path.parents):
            if (parent / "openspec").exists() or (parent / "docs").exists():
                return parent
        return None

    def _check_skill_review_record(self, gate_type: str, file_path: str) -> tuple[bool, list[str]]:
        project_root = self._find_project_root(file_path)
        if not project_root:
            return False, []

        found_records = []
        search_patterns = self.REVIEW_RECORD_PATTERNS.get(gate_type, [])

        for pattern in search_patterns:
            regex = re.compile(pattern.replace("/", r"[/\\]"))
            for md_file in project_root.glob("**/*.md"):
                if regex.search(str(md_file)):
                    found_records.append(str(md_file))

        return len(found_records) > 0, found_records

    def _format_skill_review_warning(self, gate_type: str, file_path: str) -> list[str]:
        warnings = []
        is_found, found_records = self._check_skill_review_record(gate_type, file_path)

        if not is_found:
            warnings.append("⚠️ [强制校验] 未找到 Skill 评审纪要！")
            warnings.append("   根据 SKILL.md 规定，评审类阶段必须先执行 Skill 评审")
            warnings.append("   当前仅执行了 check_*.py 量化评分，跳过了深度语义评审环节")
            warnings.append("")
            warnings.append("   【正确的执行顺序应为】:")
            warnings.append("   Step 2: prd-review Skill → check_prd.py")
            warnings.append("   Step 4: architecture-review + technical-design-review Skill → check_solution.py")
            warnings.append("   Step 6: code-review Skill → check_code.py")
            warnings.append("")
            warnings.append("   【风险提示】:")
            warnings.append("   - check_*.py 只能做量化评分，无法替代 Skill 的深度语义评审")
            warnings.append("   - 缺少 Skill 评审可能导致：阻塞项遗漏、修改建议不完整")
            warnings.append("")
            warnings.append("   【建议操作】:")
            warnings.append("   1. 如果已执行 Skill 评审但纪要路径不在默认位置，请忽略此警告")
            warnings.append("   2. 如果确实跳过了 Skill 评审，建议补充执行以确保评审完整性")
            warnings.append("   3. 如确认要跳过 Skill 评审继续执行，请使用 --skip-skill-check 参数")
        else:
            warnings.append(f"✅ 已找到 {len(found_records)} 个 Skill 评审纪要:")
            for record in found_records[:3]:
                warnings.append(f"   - {record}")

        return warnings
```

### 4.2 check_*.py 修改

**新增参数**：
```python
parser.add_argument("--skip-skill-check", action="store_true",
                   help="跳过 Skill 评审纪要检查（已确认跳过 Skill 评审）")
```

**新增调用**：
```python
if not args.skip_skill_check:
    skill_warnings = checker._format_skill_review_warning("prd", args.prd_file)
    for w in skill_warnings:
        print(w)
    if not any("✅" in w for w in skill_warnings):
        print()
```

### 4.3 警告输出示例

**未找到评审纪要时**：
```
⚠️ [强制校验] 未找到 Skill 评审纪要！
   根据 SKILL.md 规定，评审类阶段必须先执行 Skill 评审
   当前仅执行了 check_*.py 量化评分，跳过了深度语义评审环节

   【正确的执行顺序应为】:
   Step 2: prd-review Skill → check_prd.py
   ...

   【风险提示】:
   - check_*.py 只能做量化评分，无法替代 Skill 的深度语义评审

   【建议操作】:
   1. ...
```

### 涉及文件

- `llm_helper.py` - 新增检测方法
- `check_prd.py` - 新增参数和调用
- `check_solution.py` - 新增参数和调用
- `check_code.py` - 新增参数和调用

---

## 5. 改进点 7：综合判定执行保障

### 问题

| 问题 | 缺失 |
|------|------|
| **谁来执行综合判定？** | Agent？check_*.py？ |
| **综合判定产出位置？** | 评审纪要？check_*.py 输出？ |

### 综合判定规则

| Skill 评审 | 量化评分 | 综合判定 | 行动 |
|------------|---------|---------|------|
| ✓通过 | ≥ 阈值 | **✓通过** | 可进入下一阶段 |
| ✓通过 | < 阈值 | **△需修复** | 修复内容 → 重新量化评分 |
| △有条件通过 | 任意 | **△需修复** | 修复问题 → 重新 Skill 评审 |
| ✗不通过 | 任意 | **✗需修复** | 修复问题 → 重新 Skill 评审 |

### 方案

#### 7.1 执行者

**执行者**：Agent（人工判定）

**执行时机**：check_*.py 量化评分完成后

**执行过程**：
1. Agent 读取 Skill 评审纪要，提取评审结论
2. Agent 读取 check_*.py 量化评分
3. Agent 根据判定规则输出综合判定
4. Agent 将综合判定追加到评审纪要文件末尾

#### 7.2 产出位置

**方案**：追加到 Skill 评审纪要末尾

```markdown
## 综合判定

**判定日期**：YYYY-MM-DD
**判定人**：Agent

| 项目 | 值 |
|------|-----|
| Skill 评审结论 | ✓通过 / △有条件通过 / ✗不通过 |
| 量化评分 | XX/100 (阈值: YY) |
| **综合判定** | **✓通过 / △需修复 / ✗需修复** |

**判定理由**：
[Agent 根据 Skill 评审结论和量化评分，给出判定理由]

**后续行动**：
- 如果 ✓通过：可进入下一阶段，等待 Gate 确认
- 如果 △需修复：列出需要修复的问题
- 如果 ✗需修复：列出必须修复的问题
```

#### 7.3 保障机制

```markdown
#### 综合判定保障

**【强制】综合判定必须执行**：
- 执行时机：check_*.py 量化评分完成后
- 执行者：Agent（不得跳过）
- 产出物：综合判定章节，追加到 Skill 评审纪要末尾

**【强制】综合判定内容**：
- Skill 评审结论
- 量化评分
- 综合判定结论
- 判定理由
- 后续行动

**跳过后果**：
- 未执行综合判定，不得进入下一阶段
- 未产出综合判定章节，Gate 确认无效
```

### 涉及文件

- `SKILL.md` 新增章节

---

## 6. 涉及文件清单

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `SKILL.md` | 修改 | 改进点 1（L182-183）、改进点 7（综合判定保障） |
| `llm_helper.py` | 新增代码 | 改进点 6：Skill 评审纪要检测方法 |
| `check_prd.py` | 新增代码 | 改进点 6：警告调用 |
| `check_solution.py` | 新增代码 | 改进点 6：警告调用 |
| `check_code.py` | 新增代码 | 改进点 6：警告调用 |

---

## 7. 实施顺序

1. **第一阶段**：实施改进点 6（check_*.py 警告机制）
2. **第二阶段**：实施改进点 1（L182-183 歧义优化）
3. **第三阶段**：实施改进点 7（综合判定执行保障）

---

## 8. 验收标准

- [ ] check_*.py 执行时能检测 Skill 评审纪要
- [ ] 未找到纪要时输出明确警告
- [ ] 警告信息包含正确的执行顺序、风险提示、建议操作
- [ ] SKILL.md 中 L182-183 已替换为明确的三步执行顺序描述
- [ ] 综合判定执行者已明确（Agent）
- [ ] 综合判定产出位置已明确（评审纪要末尾）
