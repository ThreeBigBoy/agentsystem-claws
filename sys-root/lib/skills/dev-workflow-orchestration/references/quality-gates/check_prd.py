#!/usr/bin/env python3
"""
PRD 质量门禁检查脚本
对应 OpenSpec Step 2：PRD评审（Gate 1）
Hybrid 模式：Python 形式检查 + LLM 语义增强

职责说明：
- 第一层判断（是否使用LLM）由本脚本实现
- 第二层判断（Agent评审orAPI评审）由 llm_enhancer.py 实现

使用说明：
    Step 2 执行命令：python check_prd.py <prd_file> --llm
    Step 2 完成后命令：python check_prd.py <prd_file> --agent-score <分数>
"""

import argparse
import json
import re
import sys
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from llm_helper import LLMHelperMixin, GateResult as BaseGateResult


@dataclass
class CheckResult:
    item: str
    passed: bool
    score: float
    max_score: float
    details: str = ""


class GateResult(BaseGateResult):
    checks: list[CheckResult] = field(default_factory=list)


class PRDChecker(LLMHelperMixin):
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
        feature_pattern = re.compile(r"F-\d+")
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

    def check_prd_file(self, file_path: str, enable_llm: bool = False, user_input: str = "") -> GateResult:
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
        python_score_normalized = total_score / len(checks)

        threshold = self.prd_config.get("threshold", 80)
        strictness = self.prd_config.get("strictness", "blocking")

        result = GateResult(
            gate_name="PRD 质量门禁",
            total_score=python_score_normalized,
            threshold=threshold,
            strictness=strictness,
            passed=python_score_normalized >= threshold,
            checks=checks
        )

        if enable_llm:
            from llm_enhancer import LLMEnhancer
            enhancer = LLMEnhancer()
            result.llm_analysis, result.llm_score, result.source = self._llm_analysis(
                enhancer.analyze_prd, content, file_path, user_input=user_input
            )
            python_weight = 0.4
            llm_weight = 0.6
            result.total_score = python_score_normalized * python_weight + result.llm_score * llm_weight
            result.passed = result.total_score >= threshold

        return result


def _should_skip_llm(user_input: str = "") -> bool:
    """判断是否跳过LLM语义增强（第一层判断）"""
    skip_keywords = ["不使用LLM", "不要LLM", "不需要LLM", "跳过LLM", "不需要语义", "只需要自动化", "只要自动化", "不用LLM", "不要语义"]
    return any(kw in user_input for kw in skip_keywords)


def main():
    parser = argparse.ArgumentParser(description="PRD 质量门禁检查")
    parser.add_argument("prd_file", help="PRD 文件路径")
    parser.add_argument("--config", default="config.yaml", help="配置文件路径")
    parser.add_argument("--llm", action="store_true", help="启用 LLM 语义增强（默认启用，除非命中 --skip-llm）")
    parser.add_argument("--skip-llm", action="store_true", help="跳过 LLM 语义增强，仅执行 Python 自动化检查")
    parser.add_argument("--skip-skill-check", action="store_true", help="跳过 Skill 评审纪要检查（已确认跳过 Skill 评审）")
    parser.add_argument("--user-input", dest="user_input", default="", help="用户原始指令（用于自动判断是否跳过LLM）")
    parser.add_argument("--agent-score", type=float, help="回填 Agent 语义评审的实际分数（0-100）")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--verbose", action="store_true", default=True)

    args = parser.parse_args()

    try:
        checker = PRDChecker(args.config)

        if not args.skip_skill_check:
            skill_warnings = checker._format_skill_review_warning("prd", args.prd_file)
            for w in skill_warnings:
                print(w)
            if not any("✅" in w for w in skill_warnings):
                print()

        use_llm = not args.skip_llm and not _should_skip_llm(args.user_input)

        if use_llm:
            result = checker.check_prd_file(args.prd_file, enable_llm=True, user_input=args.user_input)
        else:
            result = checker.check_prd_file(args.prd_file, enable_llm=False)

        if args.agent_score is not None:
            python_weight = 0.4
            llm_weight = 0.6
            result.llm_score = args.agent_score
            python_score = sum(c.score for c in result.checks)
            result.total_score = python_score * python_weight + args.agent_score * llm_weight
            result.passed = result.total_score >= result.threshold
            print(f"\n✅ 分数已更新:")
            print(f"   Python 自动化分数: {python_score:.1f} × {python_weight} = {python_score * python_weight:.1f}")
            print(f"   Agent 语义评审分数: {args.agent_score:.1f} × {llm_weight} = {args.agent_score * llm_weight:.1f}")
            print(f"   综合评分: {result.total_score:.1f}/100")
            print(f"   状态: {'✅ 通过' if result.passed else '❌ 未通过'}")
            sys.exit(0 if result.passed else 1)

        if args.json:
            output = checker._format_json_output(result)
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            exit_code = checker._print_result(result, args.verbose)
            sys.exit(exit_code)

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
