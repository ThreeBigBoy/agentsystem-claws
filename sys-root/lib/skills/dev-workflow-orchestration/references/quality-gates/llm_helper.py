#!/usr/bin/env python3
"""
LLM Helper Mixin - 统一的LLM处理逻辑
被 check_prd.py, check_solution.py, check_code.py 共同使用
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class GateResult:
    gate_name: str
    total_score: float
    threshold: float
    strictness: str
    passed: bool
    checks: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    llm_analysis: Optional[str] = None
    llm_score: Optional[float] = None
    source: Optional[str] = None


class LLMHelperMixin:
    """LLM处理Mixin - 被各Checker类继承"""

    SKIP_KEYWORDS = [
        "不使用LLM", "不要LLM", "不需要LLM", "跳过LLM",
        "不需要语义", "只需要自动化", "只要自动化", "不用LLM", "不要语义"
    ]

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

    def _should_skip_llm(self, user_input: str = "") -> bool:
        """判断是否跳过LLM语义增强（第一层判断）"""
        return any(kw in user_input for kw in self.SKIP_KEYWORDS)

    def _llm_analysis(self, enhancer_method, content: str = "", file_path: str = "",
                       prd_content: Optional[str] = None, user_input: str = "",
                       task_name: str = "review") -> tuple:
        """
        统一的LLM分析处理

        Args:
            enhancer_method: llm_enhancer的analyze_*方法
            content: 待评审内容
            file_path: 文件路径
            prd_content: PRD内容（可选）
            user_input: 用户输入
            task_name: 任务名称

        Returns:
            (llm_analysis, llm_score, source)
        """
        try:
            result = enhancer_method(content, file_path, prd_content, user_input) if prd_content else \
                     enhancer_method(content, file_path, user_input)
            score = result.get("score", 80)
            source = result.get("source", "unknown")

            if result.get("source") == "api" and result.get("analysis"):
                return result["analysis"], score, source
            if result.get("source") == "agent" and result.get("analysis"):
                return result["analysis"], score, source

            return f"[{source.upper()}] {result.get('analysis', 'LLM 增强执行中')}", score, source
        except Exception as e:
            return f"[LLM 增强执行中] {str(e)}", 80, "error"

    def _format_json_output(self, result: GateResult) -> dict:
        """统一的JSON输出格式化"""
        output = {
            "gate": result.gate_name,
            "score": result.total_score,
            "threshold": result.threshold,
            "passed": result.passed,
            "source": result.source,
            "llm_analysis": result.llm_analysis,
            "llm_score": result.llm_score,
            "checks": [
                {"item": c.item, "passed": c.passed, "score": c.score, "details": c.details}
                for c in result.checks
            ]
        }
        if result.warnings:
            output["warnings"] = result.warnings
        return output

    def _print_result(self, result: GateResult, verbose: bool = True) -> int:
        """统一的打印输出"""
        print(f"\n{'='*60}")
        print(f"🚪 {result.gate_name}")
        print(f"{'='*60}")

        status = "✅ 通过" if result.passed else "❌ 未通过"
        print(f"总分: {result.total_score:.1f}/100 (阈值: {result.threshold})")
        print(f"严格度: {result.strictness}")
        print(f"状态: {status}")

        if result.warnings:
            print(f"\n⚠️ 警告:")
            for warning in result.warnings:
                print(f"  - {warning}")

        if verbose:
            print(f"\n检查项详情:")
            for check in result.checks:
                icon = "✅" if check.passed else "❌"
                print(f"  {icon} [{check.score:.1f}] {check.item}")
                if check.details:
                    for line in check.details.split("\n"):
                        print(f"      {line}")

        if result.llm_analysis:
            is_prompt = result.llm_analysis.startswith("请以")
            if is_prompt:
                print(f"\n🤖 LLM 语义增强:")
                print(f"   来源: Agent (需要用户触发)")
                print(f"   当前评分: {result.llm_score:.1f}/100 [待语义评审后更新]")
                print(f"\n{'='*60}")
                print(f"📋 请复制以下 Prompt 发送给会话 Agent 执行语义评审:")
                print(f"{'='*60}")
                print(result.llm_analysis)
                print(f"{'='*60}")
                print(f"\n💡 Agent 评审完成后，请将结果回填以更新综合评分")
            else:
                print(f"\n🤖 LLM 语义增强:")
                print(f"   来源: API")
                if result.llm_score is not None:
                    print(f"   评分: {result.llm_score:.1f}/100")
                print(f"   详情:\n{result.llm_analysis}")

        print(f"{'='*60}\n")

        return 0 if result.passed else 1
