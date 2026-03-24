#!/usr/bin/env python3
"""
方案质量门禁检查脚本
Hybrid 模式：Python 形式检查 + LLM 语义增强

使用方法：
    python check_solution.py <solution_file_path> --prd <prd_file_path>
"""

import argparse
import json
import re
import sys
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class CheckResult:
    item: str
    passed: bool
    score: float
    max_score: float
    details: str = ""


@dataclass
class GateResult:
    gate_name: str
    total_score: float
    threshold: float
    strictness: str
    passed: bool
    checks: list[CheckResult] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    llm_analysis: Optional[str] = None


class SolutionChecker:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.solution_config = self.config.get("quality_gates", {}).get("solution", {})

    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"警告: 配置文件 {config_path} 未找到，使用默认配置")
            return {}

    def check_prd_alignment(self, content: str, prd_content: Optional[str] = None) -> CheckResult:
        prd_features = []
        if prd_content:
            feature_pattern = re.compile(r"F\d+[:：]\s*\S+")
            prd_features = feature_pattern.findall(prd_content)

        matched_features = []
        for feature in prd_features:
            feature_id = feature.split(":")[0] if ":" in feature else feature.split("：")[0]
            if feature_id in content:
                matched_features.append(feature)

        score = (len(matched_features) / max(len(prd_features), 1)) * 100
        passed = len(matched_features) >= len(prd_features) * 0.7 if prd_features else True

        details = f"PRD 功能点覆盖率: {len(matched_features)}/{max(len(prd_features), 1)}"
        if prd_features and not matched_features:
            details += "\n⚠️ 未找到 PRD 功能点对应"

        return CheckResult(
            item="PRD 对应性",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_interface_clarity(self, content: str) -> CheckResult:
        has_interface_def = any(kw in content for kw in ["接口", "API", "endpoint", "/api/"])
        has_params = any(kw in content for kw in ["参数", "params", "request", "response"])
        has_field_def = "字段" in content or "field" in content.lower()

        score = 0
        if has_interface_def:
            score += 40
        if has_params:
            score += 30
        if has_field_def:
            score += 30

        passed = score >= 60

        details = f"接口定义得分: {score}/100"
        found = []
        if has_interface_def:
            found.append("接口定义")
        if has_params:
            found.append("参数定义")
        if has_field_def:
            found.append("字段定义")
        if found:
            details += f"\n找到: {', '.join(found)}"

        return CheckResult(
            item="接口定义清晰",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_tech_stack(self, content: str) -> CheckResult:
        tech_keywords = ["Python", "JavaScript", "TypeScript", "Java", "Go", "Rust",
                        "React", "Vue", "Angular", "Node.js", "FastAPI", "Django",
                        "Spring", "PostgreSQL", "MySQL", "MongoDB", "Redis"]
        found_tech = [tech for tech in tech_keywords if tech in content]

        score = min(len(found_tech) * 15, 100)
        passed = len(found_tech) >= 2

        details = f"技术栈提及: {len(found_tech)} 个"
        if found_tech:
            details += f"\n找到: {', '.join(found_tech[:5])}"

        return CheckResult(
            item="技术选型合理",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_solution_file(self, file_path: str, prd_path: Optional[str] = None, enable_llm: bool = False) -> GateResult:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"方案文件不存在: {file_path}")

        content = path.read_text(encoding="utf-8")

        prd_content = None
        if prd_path and Path(prd_path).exists():
            prd_content = Path(prd_path).read_text(encoding="utf-8")

        checks = [
            self.check_prd_alignment(content, prd_content),
            self.check_interface_clarity(content),
            self.check_tech_stack(content),
        ]

        total_score = sum(c.score for c in checks)
        warnings = []

        threshold = self.solution_config.get("threshold", 75)
        strictness = self.solution_config.get("strictness", "warning")
        passed = total_score >= threshold

        if not passed and strictness == "warning":
            warnings.append("方案质量未达标准，但设置为 warning 模式，可继续推进")

        result = GateResult(
            gate_name="方案质量门禁",
            total_score=total_score,
            threshold=threshold,
            strictness=strictness,
            passed=passed,
            checks=checks,
            warnings=warnings
        )

        if enable_llm:
            result.llm_analysis = self._llm_analysis(content, prd_content)

        return result

    def _llm_analysis(self, content: str, prd_content: Optional[str] = None) -> str:
        return "[LLM 增强待集成]\n风险识别和可实施性评估需要 LLM 接口"


def print_result(result: GateResult, verbose: bool = True):
    print(f"\n{'='*60}")
    print(f"🚪 {result.gate_name}")
    print(f"{'='*60}")

    status = "✅ 通过" if result.passed else "⚠️ 未通过（warning 模式）"
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
        print(f"\n🤖 LLM 分析:\n{result.llm_analysis}")

    print(f"{'='*60}\n")

    return 0 if result.passed else 1


def main():
    parser = argparse.ArgumentParser(description="方案质量门禁检查")
    parser.add_argument("solution_file", help="方案文件路径")
    parser.add_argument("--prd", help="PRD 文件路径（用于对应性检查）")
    parser.add_argument("--config", default="config.yaml", help="配置文件路径")
    parser.add_argument("--llm", action="store_true", help="启用 LLM 增强")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--verbose", action="store_true", default=True)

    args = parser.parse_args()

    try:
        checker = SolutionChecker(args.config)
        result = checker.check_solution_file(args.solution_file, args.prd, args.llm)

        if args.json:
            output = {
                "gate": result.gate_name,
                "score": result.total_score,
                "threshold": result.threshold,
                "passed": result.passed,
                "warnings": result.warnings,
                "checks": [
                    {"item": c.item, "passed": c.passed, "score": c.score, "details": c.details}
                    for c in result.checks
                ]
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            exit_code = print_result(result, args.verbose)
            sys.exit(exit_code)

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
