#!/usr/bin/env python3
"""
PRD 质量门禁检查脚本
Hybrid 模式：Python 形式检查 + LLM 语义增强

使用方法：
    python check_prd.py <prd_file_path>
    python check_prd.py <prd_file_path> --config config.yaml
    python check_prd.py <prd_file_path> --llm  # 启用 LLM 增强
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
    llm_analysis: Optional[str] = None


class PRDChecker:
    REQUIRED_SECTIONS = [
        "背景",
        "需求",
        "验收标准",
        "功能",
        "用户故事",
        "非功能需求",
        "异常情况",
        "附录",
    ]

    KEYWORDS_CHECK = {
        "验收标准": 2,
        "验收 Checklist": 1,
        "可测试": 1,
        "功能点": 1,
        "F1": 1,
        "F2": 1,
        "优先级": 1,
        "P0": 1,
        "P1": 1,
    }

    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.prd_config = self.config.get("quality_gates", {}).get("prd", {})

    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"警告: 配置文件 {config_path} 未找到，使用默认配置")
            return {}

    def check_structure(self, content: str) -> CheckResult:
        found_sections = []
        missing_sections = []

        for section in self.REQUIRED_SECTIONS:
            if section in content:
                found_sections.append(section)
            else:
                missing_sections.append(section)

        score = len(found_sections) / len(self.REQUIRED_SECTIONS) * 100
        passed = len(missing_sections) == 0

        details = f"找到 {len(found_sections)}/{len(self.REQUIRED_SECTIONS)} 个必需章节"
        if missing_sections:
            details += f"\n缺失: {', '.join(missing_sections)}"

        return CheckResult(
            item="结构完整性",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_keywords(self, content: str) -> CheckResult:
        found_keywords = {}
        for keyword, weight in self.KEYWORDS_CHECK.items():
            count = content.count(keyword)
            if count > 0:
                found_keywords[keyword] = count

        total_weight = sum(self.KEYWORDS_CHECK.values())
        matched_weight = sum(
            self.KEYWORDS_CHECK[k] for k in found_keywords.keys()
        )
        score = (matched_weight / total_weight) * 100

        passed = matched_weight >= total_weight * 0.7

        details = f"匹配 {len(found_keywords)}/{len(self.KEYWORDS_CHECK)} 个关键词"
        if found_keywords:
            details += f"\n找到: {', '.join(found_keywords.keys())}"

        return CheckResult(
            item="验收标准明确性",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_traceability(self, content: str) -> CheckResult:
        feature_pattern = re.compile(r"F\d+[:：]\s*\S+")
        features = feature_pattern.findall(content)

        score = min(len(features) * 20, 100)
        passed = len(features) >= 3

        details = f"找到 {len(features)} 个功能点编号"
        if features:
            details += f"\n例如: {', '.join(features[:5])}"

        return CheckResult(
            item="功能点可追踪性",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_prd_file(self, file_path: str, enable_llm: bool = False) -> GateResult:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PRD 文件不存在: {file_path}")

        content = path.read_text(encoding="utf-8")

        checks = [
            self.check_structure(content),
            self.check_keywords(content),
            self.check_traceability(content),
        ]

        total_score = sum(c.score for c in checks)

        threshold = self.prd_config.get("threshold", 80)
        strictness = self.prd_config.get("strictness", "blocking")
        passed = total_score >= threshold

        result = GateResult(
            gate_name="PRD 质量门禁",
            total_score=total_score,
            threshold=threshold,
            strictness=strictness,
            passed=passed,
            checks=checks
        )

        if enable_llm:
            result.llm_analysis = self._llm_analysis(content)

        return result

    def _llm_analysis(self, content: str) -> str:
        return "[LLM 增强待集成]\n产品逻辑完整性和设计合理性评估需要 LLM 接口"


def print_result(result: GateResult, verbose: bool = True):
    print(f"\n{'='*60}")
    print(f"🚪 {result.gate_name}")
    print(f"{'='*60}")

    status = "✅ 通过" if result.passed else "❌ 未通过"
    print(f"总分: {result.total_score:.1f}/100 (阈值: {result.threshold})")
    print(f"严格度: {result.strictness}")
    print(f"状态: {status}")

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
    parser = argparse.ArgumentParser(description="PRD 质量门禁检查")
    parser.add_argument("prd_file", help="PRD 文件路径")
    parser.add_argument("--config", default="config.yaml", help="配置文件路径")
    parser.add_argument("--llm", action="store_true", help="启用 LLM 增强")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--verbose", action="store_true", default=True)

    args = parser.parse_args()

    try:
        checker = PRDChecker(args.config)
        result = checker.check_prd_file(args.prd_file, args.llm)

        if args.json:
            output = {
                "gate": result.gate_name,
                "score": result.total_score,
                "threshold": result.threshold,
                "passed": result.passed,
                "checks": [
                    {
                        "item": c.item,
                        "passed": c.passed,
                        "score": c.score,
                        "details": c.details
                    }
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
