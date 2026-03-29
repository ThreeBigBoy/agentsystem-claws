#!/usr/bin/env python3
"""
方案质量门禁检查脚本
对应 OpenSpec Step 4：方案评审（Gate 2）
Hybrid 模式：Python 形式检查 + LLM 语义增强

职责说明：
- 第一层判断（是否使用LLM）由本脚本实现
- 第二层判断（Agent评审orAPI评审）由 llm_enhancer.py 实现

使用说明：
    Step 4 执行命令：python check_solution.py <solution_file> --prd <prd_file> --llm
    Step 4 完成后命令：python check_solution.py <solution_file> --agent-score <分数>
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


class SolutionChecker(LLMHelperMixin):
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
            feature_pattern = re.compile(r"F-\d+")
            prd_features = feature_pattern.findall(prd_content)

        matched_features = []
        for feature in prd_features:
            if feature in content:
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
        quality_checks = {
            "技术需求分析": ["需求分析", "具体需求", "优先级"],
            "候选方案对比": ["方案", "对比", "候选", "方案A", "方案B", "方案C"],
            "选型决策": ["决策", "选择", "依据", "加权", "评分"],
            "风险应对": ["风险", "应对", "缓解", "措施", "等级"],
            "技术栈清单": ["技术栈", "框架", "数据库", "存储", "API"]
        }

        scores = {}
        total_score = 0

        for check_name, keywords in quality_checks.items():
            found = any(kw in content for kw in keywords)
            check_score = 20 if found else 0
            scores[check_name] = check_score
            total_score += check_score

        passed = total_score >= 60

        details = f"技术选型质量评分: {total_score}/100"
        for check_name, score in scores.items():
            status = "✅" if score > 0 else "❌"
            details += f"\n  {status} {check_name}: {'通过' if score > 0 else '缺失'}"

        return CheckResult(
            item="技术选型合理",
            passed=passed,
            score=total_score,
            max_score=100,
            details=details
        )

    def check_data_flow_design(self, content: str) -> CheckResult:
        quality_checks = {
            "数据流描述": ["数据流", "流向", "流程"],
            "模块间接口": ["接口", "调用", "交互"],
            "输入输出定义": ["输入", "输出", "参数", "返回值"],
        }

        scores = {}
        total_score = 0

        for check_name, keywords in quality_checks.items():
            found = any(kw in content for kw in keywords)
            check_score = 20 if found else 0
            scores[check_name] = check_score
            total_score += check_score

        passed = total_score >= 40

        details = f"数据流设计评分: {total_score}/100"
        for check_name, score in scores.items():
            status = "✅" if score > 0 else "❌"
            details += f"\n  {status} {check_name}: {'通过' if score > 0 else '缺失'}"

        return CheckResult(
            item="数据流设计",
            passed=passed,
            score=total_score,
            max_score=100,
            details=details
        )

    def check_storage_design(self, content: str) -> CheckResult:
        quality_checks = {
            "存储结构定义": ["存储", "数据结构", "storage"],
            "容量控制策略": ["容量", "限制", "清理", "自动清理"],
            "数据安全措施": ["安全", "加密", "隐私"],
        }

        scores = {}
        total_score = 0

        for check_name, keywords in quality_checks.items():
            found = any(kw in content for kw in keywords)
            check_score = 20 if found else 0
            scores[check_name] = check_score
            total_score += check_score

        passed = total_score >= 40

        details = f"存储设计评分: {total_score}/100"
        for check_name, score in scores.items():
            status = "✅" if score > 0 else "❌"
            details += f"\n  {status} {check_name}: {'通过' if score > 0 else '缺失'}"

        return CheckResult(
            item="存储设计",
            passed=passed,
            score=total_score,
            max_score=100,
            details=details
        )

    def check_project_structure(self, content: str) -> CheckResult:
        quality_checks = {
            "目录结构": ["目录", "结构", "文件夹"],
            "模块划分": ["模块", "pages", "components", "utils"],
            "规范遵循": ["规范", "规则", "遵循"],
        }

        scores = {}
        total_score = 0

        for check_name, keywords in quality_checks.items():
            found = any(kw in content for kw in keywords)
            check_score = 20 if found else 0
            scores[check_name] = check_score
            total_score += check_score

        passed = total_score >= 40

        details = f"项目结构评分: {total_score}/100"
        for check_name, score in scores.items():
            status = "✅" if score > 0 else "❌"
            details += f"\n  {status} {check_name}: {'通过' if score > 0 else '缺失'}"

        return CheckResult(
            item="项目结构",
            passed=passed,
            score=total_score,
            max_score=100,
            details=details
        )

    def check_solution_file(self, file_path: str, prd_path: Optional[str] = None, enable_llm: bool = False, user_input: str = "") -> GateResult:
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
            self.check_data_flow_design(content),
            self.check_storage_design(content),
            self.check_project_structure(content),
        ]

        total_score = sum(c.score for c in checks)
        warnings = []

        threshold = self.solution_config.get("threshold", 75)
        strictness = self.solution_config.get("strictness", "warning")
        passed = total_score >= threshold

        if not passed and strictness == "warning":
            warnings.append("方案质量未达标准，但设置为 warning 模式，可继续推进")

        python_score_normalized = total_score / len(checks)

        result = GateResult(
            gate_name="方案质量门禁",
            total_score=python_score_normalized,
            threshold=threshold,
            strictness=strictness,
            passed=python_score_normalized >= threshold,
            checks=checks,
            warnings=warnings
        )

        if enable_llm:
            from llm_enhancer import LLMEnhancer
            enhancer = LLMEnhancer()
            result.llm_analysis, result.llm_score, result.source = self._llm_analysis(
                enhancer.analyze_solution, content, file_path, prd_content, user_input
            )
            python_weight = 0.7
            llm_weight = 0.3
            result.total_score = python_score_normalized * python_weight + result.llm_score * llm_weight
            result.passed = result.total_score >= threshold

        return result


def _should_skip_llm(user_input: str = "") -> bool:
    """判断是否跳过LLM语义增强（第一层判断）"""
    skip_keywords = ["不使用LLM", "不要LLM", "不需要LLM", "跳过LLM", "不需要语义", "只需要自动化", "只要自动化", "不用LLM", "不要语义"]
    return any(kw in user_input for kw in skip_keywords)


def main():
    parser = argparse.ArgumentParser(description="方案质量门禁检查")
    parser.add_argument("solution_file", help="方案文件路径")
    parser.add_argument("--prd", help="PRD 文件路径（用于对应性检查）")
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
        checker = SolutionChecker(args.config)

        if not args.skip_skill_check:
            skill_warnings = checker._format_skill_review_warning("solution", args.solution_file)
            for w in skill_warnings:
                print(w)
            if not any("✅" in w for w in skill_warnings):
                print()

        use_llm = not args.skip_llm and not _should_skip_llm(args.user_input)

        if use_llm:
            result = checker.check_solution_file(args.solution_file, args.prd, enable_llm=True, user_input=args.user_input)
        else:
            result = checker.check_solution_file(args.solution_file, args.prd, enable_llm=False)

        if args.agent_score is not None:
            python_weight = 0.7
            llm_weight = 0.3
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
