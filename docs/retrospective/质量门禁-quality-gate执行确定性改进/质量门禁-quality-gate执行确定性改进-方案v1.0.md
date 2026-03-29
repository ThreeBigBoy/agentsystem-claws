# 质量门禁执行确定性改进方案

## 修订历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-03-29 | 初始版本，定义 6 个改进点及具体实现方案 |
| v1.1 | 2026-03-29 | 补充改进点 7-8：综合判定执行保障 |

---

## 1. 背景

本方案旨在解决质量门禁执行过程中 Skill 评审环节容易被跳过的问题，确保评审类阶段严格遵循「Skill评审 → 量化评分 → 综合判定」的执行顺序。

详见：[背景复盘文档](./质量门禁-quality-gate执行确定性改进-背景复盘.md)

---

## 2. 改进点汇总

| # | 改进点 | 目标 | 涉及文件 |
|---|--------|------|---------|
| 1 | L182-183 歧义优化 | 明确每个 Step 的完整执行步骤 | SKILL.md |
| 2 | 触发机制 | 定义启动条件 + 触发关键词 | SKILL.md |
| 3 | 校验机制 | 用文件存在性替代 tasks.md | SKILL.md |
| 4 | 跳过后果 | 定义跳过场景 + 后果 + 处理 | SKILL.md |
| 5 | 异常处理 | 补充 6 种异常场景处理 | SKILL.md |
| 6 | check_*.py 警告 | 自动检测 + 强制校验警告 | llm_helper.py, check_*.py |
| 7 | 综合判定执行保障 | 执行者、产出位置、保障机制 | SKILL.md |
| 8 | 综合判定 vs Gate 确认 | 明确两者关系和顺序 | SKILL.md |

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

## 4. 改进点 2：触发机制

### 问题

SKILL.md 只说"调用 Skill"，没说怎么触发、怎么判断当前阶段。

### 方案

在 SKILL.md 中添加各 Step 启动准入条件：

```markdown
#### 各 Step 启动准入条件

**Step 2 PRD评审 - 启动条件**：
- 前置条件：PRD 文档已存在于 `docs/project-prd-changes/[change-id]/PRD-[change-id]*.md`
- 触发条件：用户输入包含「评审 PRD」「检查 PRD」「PRD 自检」等关键词
- Agent 动作：必须加载并执行 `prd-review` Skill，不得跳过

**Step 4 方案评审 - 启动条件**：
- 前置条件：PRD 评审「✓通过」+ Gate-PRD 已确认
- 触发条件：用户输入包含「评审方案」「检查设计」「方案自检」等关键词
- Agent 动作：必须加载并执行 `architecture-review` + `technical-design-review` Skill，不得跳过

**Step 6 代码评审 - 启动条件**：
- 前置条件：方案评审「✓通过」+ Gate-DESIGN 已确认
- 触发条件：用户输入包含「评审代码」「代码检查」「自检」等关键词
- Agent 动作：必须加载并执行 `code-review` Skill，不得跳过

**触发识别规则**：
- 当用户输入匹配触发关键词时，Agent 自动进入对应 Step
- Agent 执行前先确认前置条件满足
- 前置条件不满足时，Agent 应先完成前置步骤
```

### 涉及文件

- `SKILL.md` 新增章节

---

## 5. 改进点 3：校验机制（基于文件存在性）

### 问题

tasks.md 机制太重，用"文件存在性"替代。

### 方案

```markdown
#### 校验点定义

**Step 2 PRD评审 - 校验点**：

| 校验点 | 校验内容 | 校验方式 |
|--------|---------|---------|
| 校验点 1 | prd-review Skill 是否执行 | 检查 `docs/project-prd-changes/[change-id]/records/PRD-[change-id]-评审纪要.md` 是否存在 |
| 校验点 2 | check_prd.py 是否执行 | 读取量化评分输出（stdout/文件） |
| 校验点 3 | 综合判定 | Skill 评审结论 + 量化评分，两者都存在方可判定 |

**校验点判定规则**：
- 校验点 1 不满足 → **必须**先执行 prd-review Skill，**不得**跳过
- 校验点 2 不满足 → **必须**执行 check_prd.py，**不得**以 Skill 评审替代
- 校验点 1 + 2 都满足 → 可进行综合判定

**Step 4 方案评审 - 校验点**：

| 校验点 | 校验内容 | 校验方式 |
|--------|---------|---------|
| 校验点 1a | architecture-review Skill 是否执行 | 检查对应评审纪要是否存在 |
| 校验点 1b | technical-design-review Skill 是否执行 | 检查对应评审纪要是否存在 |
| 校验点 2 | check_solution.py 是否执行 | 读取量化评分输出 |
| 校验点 3 | 双 Skill 判定结论 | 两个 Skill 都必须「✓通过」 |

**Step 6 代码评审 - 校验点**：

| 校验点 | 校验内容 | 校验方式 |
|--------|---------|---------|
| 校验点 1 | code-review Skill 是否执行 | 检查 `records/code-review-[change-id]-评审纪要.md` 是否存在 |
| 校验点 2 | check_code.py 是否执行 | 读取量化评分输出 |
| 校验点 3 | 综合判定 | Skill 评审结论 + 量化评分 |
```

### 涉及文件

- `SKILL.md` 新增章节

---

## 6. 改进点 4：跳过后果

### 问题

说"强制"但无后果描述。

### 方案

```markdown
#### 跳过规则与后果

**【强制】以下步骤不得跳过**：
1. prd-review / architecture-review / technical-design-review / code-review Skill 评审
2. check_prd.py / check_solution.py / check_code.py 量化评分
3. 综合判定结论

**跳过后果定义**：

| 跳过场景 | 后果 | 处理方式 |
|---------|------|---------|
| 跳过 Skill 评审（步骤 1） | check_*.py 会输出 ⚠️ 强制校验警告 | Agent **必须**补充执行 Skill 评审，量化评分结果**不得**作为最终判定依据 |
| 跳过 check_*.py（步骤 2） | **不允许** | Skill 评审结论**不得**替代量化评分，必须补充 |
| 跳过综合判定（步骤 3） | **不允许** | 必须产出综合判定结论才能进入下一阶段 |

**用户主动要求跳过的处理**：
- 用户必须显式说明跳过原因并记录
- Agent 在评审纪要中追加记录：「[日期] 用户要求跳过 [步骤]，原因：[用户说明]」
- 跳过后的结果**降级处理**：仅作参考，不作为正式通过依据
- **注意**：即使降级处理，Gate 仍需用户人工确认才能进入下一阶段
```

### 涉及文件

- `SKILL.md` 新增章节

---

## 7. 改进点 5：异常处理

### 问题

无异常场景说明。

### 方案

```markdown
#### 异常处理

**场景 1：Skill 评审执行失败**
- 处理：定位失败原因，修复后重新执行 Skill
- **禁止**：不得跳过 Skill 进入下一步

**场景 2：check_*.py 执行失败（如脚本错误）**
- 处理：修复脚本错误，重新执行
- **禁止**：不得以 Skill 评审结论作为替代

**场景 3：Skill 评审结论为「△有条件通过」**
- 处理：进入 Review-Fix-Loop
  1. 识别问题清单
  2. 修复问题
  3. 重新执行 Skill 评审
  4. 直至结论转为「✓通过」
- **禁止**：有条件通过时进入下一阶段

**场景 4：Skill 评审结论为「✗不通过」**
- 处理：必须修复 → 重新评审
- **禁止**：不通过时进入下一阶段

**场景 5：量化评分低于阈值**
- 处理：
  1. 分析低分原因
  2. 修复内容（PRD/方案/代码）
  3. 重新执行 check_*.py
  4. 直至评分 ≥ 阈值
- **注意**：低分不代表 Skill 评审结论，但综合判定需要两者都达标

**场景 6：Skill 评审与量化评分结论矛盾**
- 如：Skill 评审「✓通过」但量化评分 < 阈值
- 处理：以更严格的结论为准，需修复直至两者都达标
```

### 涉及文件

- `SKILL.md` 新增章节

---

## 8. 改进点 6：check_*.py 强制校验警告

### 问题

Agent 可能直接调用 check_*.py 绕过 Skill 评审。

### 方案

#### 8.1 llm_helper.py 新增代码

```python
class LLMHelperMixin:
    # 新增：Skill 评审纪要检测
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
        """从文件路径向上查找项目根目录"""
        path = Path(file_path).resolve()
        for parent in [path] + list(path.parents):
            if (parent / "openspec").exists() or (parent / "docs").exists():
                return parent
        return None

    def _check_skill_review_record(self, gate_type: str, file_path: str) -> tuple[bool, list[str]]:
        """
        检测 Skill 评审纪要是否存在

        Args:
            gate_type: 门禁类型 (prd/solution/code)
            file_path: 当前评审文件的路径

        Returns:
            (is_found, found_records): 是否找到纪要, 找到的纪要路径列表
        """
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
        """
        格式化 Skill 评审缺失警告
        """
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

#### 8.2 check_*.py 修改

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
        print()  # 空行分隔
```

#### 8.3 执行流程

```
用户执行：python check_prd.py PRD-xxx.md
    ↓
check_prd.py main() 入口
    ↓
解析命令行参数（包括 --skip-skill-check）
    ↓
PRDChecker 实例化
    ↓
判断 if not args.skip_skill_check:
    ↓ (为 True 时执行检测)
_format_skill_review_warning("prd", "PRD-xxx.md")
    ↓
1. _find_project_root() → 找到项目根目录
2. _check_skill_review_record("prd", path) → 搜索评审纪要
3. 判断是否找到 → 输出警告或找到记录
    ↓
输出警告信息（如果未找到）
    ↓
继续原有执行逻辑...
```

#### 8.4 警告输出示例

**未找到评审纪要时**：
```
⚠️ [强制校验] 未找到 Skill 评审纪要！
   根据 SKILL.md 规定，评审类阶段必须先执行 Skill 评审
   当前仅执行了 check_*.py 量化评分，跳过了深度语义评审环节

   【正确的执行顺序应为】:
   Step 2: prd-review Skill → check_prd.py
   Step 4: architecture-review + technical-design-review Skill → check_solution.py
   Step 6: code-review Skill → check_code.py

   【风险提示】:
   - check_*.py 只能做量化评分，无法替代 Skill 的深度语义评审
   - 缺少 Skill 评审可能导致：阻塞项遗漏、修改建议不完整

   【建议操作】:
   1. 如果已执行 Skill 评审但纪要路径不在默认位置，请忽略此警告
   2. 如果确实跳过了 Skill 评审，建议补充执行以确保评审完整性
   3. 如确认要跳过 Skill 评审继续执行，请使用 --skip-skill-check 参数

============================================================
🚪 PRD 质量门禁
============================================================
总分: 84.27/100 (阈值: 80)
...
```

**找到评审纪要时**：
```
✅ 已找到 1 个 Skill 评审纪要:
   - docs/project-prd-changes/curiobuddy/records/PRD-curiobuddy-评审纪要.md

============================================================
🚪 PRD 质量门禁
============================================================
...
```

### 涉及文件

- `llm_helper.py` - 新增检测方法
- `check_prd.py` - 新增参数和调用
- `check_solution.py` - 新增参数和调用
- `check_code.py` - 新增参数和调用

---

## 9. 改进点 7：综合判定执行保障

### 问题

| 问题 | 缺失 |
|------|------|
| **谁来执行综合判定？** | Agent？check_*.py？ |
| **综合判定产出位置？** | 评审纪要？check_*.py 输出？ |
| **如何确保执行？** | 无保障机制 |

### 综合判定的输入

| 输入 | 来源 | 状态 |
|------|------|------|
| Skill 评审结论 | 评审纪要 | ✓通过 / △有条件通过 / ✗不通过 |
| 量化评分 | check_*.py | 0-100 分 |

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

## 10. 改进点 8：综合判定 vs Gate 确认的关系

### 问题

| 问题 | 混淆点 |
|------|--------|
| **综合判定 ≠ Gate 确认** | 综合判定是 Agent 执行的技术判定，Gate 确认是用户的人工确认 |
| **顺序** | 综合判定 → Gate 确认 → 进入下一阶段 |

### 方案

```markdown
#### Step 2 PRD评审 - 完整流程

```
prd-review Skill 执行
    ↓
check_prd.py 量化评分
    ↓
【步骤 3】Agent 综合判定 → 产出综合判定章节
    ↓
Gate-PRD 用户人工确认
    ↓
进入 Step 3
```

**注意**：
- 综合判定是技术判定（Agent 执行）
- Gate 确认是人工确认（用户执行）
- 两者缺一不可
- 顺序不能颠倒
```

### 涉及文件

- `SKILL.md` 新增章节

---

## 11. 涉及文件清单

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `SKILL.md` | 修改 | 改进点 1-5, 7-8：歧义优化、触发机制、校验机制、跳过后果、异常处理、综合判定保障 |
| `llm_helper.py` | 新增代码 | 改进点 6：Skill 评审纪要检测方法 |
| `check_prd.py` | 新增代码 | 改进点 6：警告调用 |
| `check_solution.py` | 新增代码 | 改进点 6：警告调用 |
| `check_code.py` | 新增代码 | 改进点 6：警告调用 |

---

## 12. 实施顺序建议

1. **第一阶段**：实施改进点 1（L182-183 歧义优化）
2. **第二阶段**：实施改进点 2-5（触发机制、校验机制、跳过后果、异常处理）
3. **第三阶段**：实施改进点 6（check_*.py 警告机制）
4. **第四阶段**：实施改进点 7-8（综合判定执行保障）

---

## 13. 验收标准

- [ ] SKILL.md 中 L182-183 已替换为明确的三步执行顺序描述
- [ ] 各 Step 启动准入条件已定义
- [ ] 校验点定义清晰，基于文件存在性
- [ ] 跳过后果明确
- [ ] 6 种异常场景处理已定义
- [ ] check_*.py 执行时能检测 Skill 评审纪要
- [ ] 未找到纪要时输出明确警告
- [ ] 警告信息包含正确的执行顺序、风险提示、建议操作
- [ ] 综合判定执行者已明确（Agent）
- [ ] 综合判定产出位置已明确（评审纪要末尾）
- [ ] 综合判定 vs Gate 确认的关系和顺序已明确
