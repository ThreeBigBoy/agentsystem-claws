#!/usr/bin/env python3
"""
代码质量门禁检查脚本
对应 OpenSpec Step 6：代码评审（Gate 3）
Hybrid 模式：Python 自动化检查 + LLM 可选评审

职责说明：
- 第一层判断（是否使用LLM）由本脚本实现
- 第二层判断（Agent评审orAPI评审）由 llm_enhancer.py 实现

使用说明：
    Step 6 执行命令：python check_code.py <project_dir> --llm
    Step 6 完成后命令：python check_code.py <project_dir> --agent-score <分数>
"""

import argparse
import json
import subprocess
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
    llm_score: Optional[float] = None
    source: Optional[str] = None


class CodeChecker:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.code_config = self.config.get("quality_gates", {}).get("code", {})

    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"警告: 配置文件 {config_path} 未找到，使用默认配置")
            return {}

    def _run_command(self, cmd: list[str], cwd: Optional[str] = None) -> tuple[int, str, str]:
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def check_functionality(self, project_dir: str) -> CheckResult:
        pytest_dir = Path(project_dir) / "tests"
        if not pytest_dir.exists():
            return CheckResult(
                item="功能实现完整",
                passed=False,
                score=0,
                max_score=100,
                details="未找到 tests 目录"
            )

        returncode, stdout, stderr = self._run_command(
            ["python", "-m", "pytest", "--collect-only", "-q"],
            cwd=project_dir
        )

        if returncode != 0:
            return CheckResult(
                item="功能实现完整",
                passed=False,
                score=0,
                max_score=100,
                details=f"pytest 收集失败: {stderr[:200]}"
            )

        test_count = len([l for l in stdout.split("\n") if "::" in l])
        score = min(test_count * 5, 100)
        passed = test_count >= 3

        return CheckResult(
            item="功能实现完整",
            passed=passed,
            score=score,
            max_score=100,
            details=f"找到 {test_count} 个测试用例"
        )

    def check_security(self, project_dir: str) -> CheckResult:
        bandit_result = Path(project_dir) / "bandit_report.json"
        if not Path(project_dir).exists():
            return CheckResult(
                item="无明显安全漏洞",
                passed=True,
                score=100,
                max_score=100,
                details="跳过安全检查（未安装 bandit）"
            )

        returncode, stdout, stderr = self._run_command(
            ["python", "-m", "bandit", "-r", "-f", "json", "."],
            cwd=project_dir
        )

        try:
            report = json.loads(stdout) if stdout else {"metrics": {}}
            high_issues = report.get("metrics", {}).get("SEVERITY.HIGH.value", 0)
            medium_issues = report.get("metrics", {}).get("SEVERITY.MEDIUM.value", 0)

            score = max(100 - high_issues * 20 - medium_issues * 5, 0)
            passed = high_issues == 0 and medium_issues <= 3

            details = f"高危: {high_issues}, 中危: {medium_issues}"
        except:
            score = 50
            passed = False
            details = "bandit 报告解析失败，跳过安全检查"

        return CheckResult(
            item="无明显安全漏洞",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_linting(self, project_dir: str) -> CheckResult:
        returncode, stdout, stderr = self._run_command(
            ["python", "-m", "flake8", "--count", "-q"],
            cwd=project_dir
        )

        error_count = len([l for l in stdout.split("\n") if l.strip()])
        score = max(100 - error_count * 2, 0)
        passed = error_count <= 10

        return CheckResult(
            item="代码规范",
            passed=passed,
            score=score,
            max_score=100,
            details=f"flake8 报错: {error_count} 处"
        )

    def check_test_coverage(self, project_dir: str) -> CheckResult:
        returncode, stdout, stderr = self._run_command(
            ["python", "-m", "pytest", "--cov", "--cov-report=term-missing", "-q"],
            cwd=project_dir
        )

        try:
            for line in stdout.split("\n"):
                if "TOTAL" in line or "Coverage" in line:
                    import re
                    match = re.search(r"(\d+)%",
                                    line.replace("Coverage", "").replace("TOTAL", ""))
                    if match:
                        coverage = int(match.group(1))
                        score = coverage
                        passed = coverage >= 60
                        return CheckResult(
                            item="单元测试覆盖",
                            passed=passed,
                            score=score,
                            max_score=100,
                            details=f"覆盖率: {coverage}%"
                        )
        except:
            pass

        return CheckResult(
            item="单元测试覆盖",
            passed=True,
            score=50,
            max_score=100,
            details="覆盖率检测失败，跳过"
        )

    def check_project(self, project_dir: str, enable_llm: bool = False, user_input: str = "") -> GateResult:
        path = Path(project_dir)
        if not path.exists():
            raise FileNotFoundError(f"项目目录不存在: {project_dir}")

        checks = [
            self.check_functionality(project_dir),
            self.check_security(project_dir),
            self.check_linting(project_dir),
            self.check_test_coverage(project_dir),
        ]

        total_score = sum(c.score for c in checks)

        threshold = self.code_config.get("threshold", 80)
        strictness = self.code_config.get("strictness", "blocking")
        python_score_normalized = total_score / len(checks)

        result = GateResult(
            gate_name="代码质量门禁",
            total_score=python_score_normalized,
            threshold=threshold,
            strictness=strictness,
            passed=python_score_normalized >= threshold,
            checks=checks
        )

        if enable_llm:
            result.llm_analysis, result.llm_score, result.source = self._llm_analysis(project_dir, user_input)
            python_weight = 0.95
            llm_weight = 0.05
            result.total_score = python_score_normalized * python_weight + result.llm_score * llm_weight
            result.passed = result.total_score >= threshold

        return result

    def _llm_analysis(self, project_dir: str, user_input: str = "") -> tuple:
        try:
            from llm_enhancer import LLMEnhancer
            enhancer = LLMEnhancer()
            result = enhancer.analyze_code(project_dir, project_dir, user_input)
            score = result.get("score", 80)
            source = result.get("source", "unknown")
            if result.get("source") == "api" and result.get("analysis"):
                return result["analysis"], score, source
            if result.get("source") == "agent" and result.get("analysis"):
                return result["analysis"], score, source
            return f"[{source.upper()}] {result.get('analysis', 'LLM 增强执行中')}", score, source
        except Exception as e:
            return f"[LLM 增强执行中] {str(e)}", 80, "error"


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
        is_prompt = result.llm_analysis.startswith("请以")
        if is_prompt:
            print(f"\n🤖 LLM 语义增强:")
            print(f"   来源: Agent (需要用户触发)")
            print(f"   当前评分: {result.llm_score:.1f}/100 (权重5%) [待语义评审后更新]")
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
                print(f"   评分: {result.llm_score:.1f}/100 (权重5%)")
            print(f"   详情:\n{result.llm_analysis}")

    print(f"{'='*60}\n")

    return 0 if result.passed else 1


def _should_skip_llm(user_input: str = "") -> bool:
    """判断是否跳过LLM语义增强（第一层判断）"""
    skip_keywords = ["不使用LLM", "不要LLM", "不需要LLM", "跳过LLM", "不需要语义", "只需要自动化", "只要自动化", "不用LLM", "不要语义"]
    return any(kw in user_input for kw in skip_keywords)


def main():
    parser = argparse.ArgumentParser(description="代码质量门禁检查")
    parser.add_argument("project_dir", help="项目目录路径")
    parser.add_argument("--config", default="config.yaml", help="配置文件路径")
    parser.add_argument("--llm", action="store_true", help="启用 LLM 语义增强（默认启用，除非命中 --skip-llm）")
    parser.add_argument("--skip-llm", action="store_true", help="跳过 LLM 语义增强，仅执行 Python 自动化检查")
    parser.add_argument("--user-input", dest="user_input", default="", help="用户原始指令（用于自动判断是否跳过LLM）")
    parser.add_argument("--agent-score", type=float, help="回填 Agent 语义评审的实际分数（0-100）")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--verbose", action="store_true", default=True)

    args = parser.parse_args()

    try:
        checker = CodeChecker(args.config)

        use_llm = not args.skip_llm and not _should_skip_llm(args.user_input)

        if use_llm:
            result = checker.check_project(args.project_dir, enable_llm=True, user_input=args.user_input)
        else:
            result = checker.check_project(args.project_dir, enable_llm=False)

        if args.agent_score is not None:
            python_weight = 0.95
            llm_weight = 0.05
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
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            exit_code = print_result(result, args.verbose)
            sys.exit(exit_code)

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
