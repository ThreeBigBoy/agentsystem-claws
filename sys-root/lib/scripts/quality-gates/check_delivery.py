#!/usr/bin/env python3
"""
交付质量门禁检查脚本
Hybrid 模式：Python 自动化检查 + 人工确认

使用方法：
    python check_delivery.py <change_id> --project <project_dir>
"""

import argparse
import json
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
    requires_human_confirmation: bool = True
    human_confirmation_received: bool = False


class DeliveryChecker:
    CHECKLIST_FILE = "验收Checklist.md"

    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.delivery_config = self.config.get("quality_gates", {}).get("delivery", {})

    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"警告: 配置文件 {config_path} 未找到，使用默认配置")
            return {}

    def check_deliverable(self, project_dir: str) -> CheckResult:
        path = Path(project_dir)
        has_code = any(path.glob("*.py")) or any(path.glob("*.js")) or any(path.glob("*.ts"))
        has_readme = (path / "README.md").exists()

        score = 0
        found = []
        if has_code:
            score += 40
            found.append("代码")
        if has_readme:
            score += 20
            found.append("README")
        score += 40

        passed = has_code and has_readme

        details = f"基础交付物检查: {', '.join(found) if found else '部分缺失'}"
        if not has_readme:
            details += "\n⚠️ 建议添加 README.md"

        return CheckResult(
            item="可部署/可运行",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_documentation(self, project_dir: str) -> CheckResult:
        path = Path(project_dir)
        required_docs = [
            "README.md",
            "验收Checklist.md",
        ]
        optional_docs = [
            "CHANGELOG.md",
            "docs/",
        ]

        found_required = [d for d in required_docs if (path / d).exists()]
        found_optional = [d for d in optional_docs if (path / d).exists()]

        score = len(found_required) / len(required_docs) * 100
        passed = len(found_required) == len(required_docs)

        details = f"必需文档: {len(found_required)}/{len(required_docs)}"
        if found_optional:
            details += f"\n可选文档: {', '.join(found_optional)}"

        return CheckResult(
            item="文档完整",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_changelog(self, project_dir: str) -> CheckResult:
        path = Path(project_dir)
        changelog = path / "CHANGELOG.md"
        project_log = path / "docs" / "项目事件日志.md"

        has_changelog = changelog.exists()
        has_project_log = project_log.exists()

        score = 0
        found = []
        if has_changelog:
            score += 50
            found.append("CHANGELOG")
        if has_project_log:
            score += 50
            found.append("项目日志")

        passed = has_changelog or has_project_log

        details = f"变更记录: {', '.join(found) if found else '未找到'}"

        return CheckResult(
            item="变更记录完整",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_checklist(self, change_id: str, project_dir: str) -> CheckResult:
        path = Path(project_dir) / "docs" / "project-prd-changes" / change_id
        checklist_file = path / "验收Checklist.md"

        if not checklist_file.exists():
            return CheckResult(
                item="验收 Checklist",
                passed=False,
                score=0,
                max_score=100,
                details=f"未找到: {checklist_file}"
            )

        content = checklist_file.read_text(encoding="utf-8")
        checked_items = content.count("[x]") + content.count("[X]")
        total_items = content.count("[ ]") + checked_items

        if total_items == 0:
            return CheckResult(
                item="验收 Checklist",
                passed=False,
                score=0,
                max_score=100,
                details="Checklist 为空"
            )

        completion_rate = (checked_items / total_items) * 100 if total_items > 0 else 0
        score = completion_rate
        passed = completion_rate == 100

        details = f"完成度: {checked_items}/{total_items} ({completion_rate:.0f}%)"

        return CheckResult(
            item="验收 Checklist 通过",
            passed=passed,
            score=score,
            max_score=100,
            details=details
        )

    def check_delivery(self, change_id: str, project_dir: str, human_confirmed: bool = False) -> GateResult:
        path = Path(project_dir)
        if not path.exists():
            raise FileNotFoundError(f"项目目录不存在: {project_dir}")

        checks = [
            self.check_checklist(change_id, project_dir),
            self.check_deliverable(project_dir),
            self.check_documentation(project_dir),
            self.check_changelog(project_dir),
        ]

        total_score = sum(c.score for c in checks)

        threshold = self.delivery_config.get("threshold", 85)
        strictness = self.delivery_config.get("strictness", "blocking")

        all_python_passed = all(c.passed for c in checks)
        passed = all_python_passed and human_confirmed

        result = GateResult(
            gate_name="交付质量门禁",
            total_score=total_score,
            threshold=threshold,
            strictness=strictness,
            passed=passed,
            checks=checks,
            requires_human_confirmation=True,
            human_confirmation_received=human_confirmed
        )

        return result


def print_result(result: GateResult, verbose: bool = True):
    print(f"\n{'='*60}")
    print(f"🚪 {result.gate_name}")
    print(f"{'='*60}")

    if result.requires_human_confirmation and not result.human_confirmation_received:
        status = "⏳ 待人工确认"
        print(f"总分: {result.total_score:.1f}/100 (阈值: {result.threshold})")
        print(f"严格度: {result.strictness}")
        print(f"状态: {status}")
        print(f"\n📋 请确认以下检查项全部通过后，输入 'confirm' 完成人工确认")
    else:
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

    print(f"{'='*60}\n")

    return 0 if result.passed else 1


def main():
    parser = argparse.ArgumentParser(description="交付质量门禁检查")
    parser.add_argument("change_id", help="Change ID")
    parser.add_argument("--project", required=True, help="项目目录路径")
    parser.add_argument("--config", default="config.yaml", help="配置文件路径")
    parser.add_argument("--confirm", action="store_true", help="人工确认通过")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--verbose", action="store_true", default=True)

    args = parser.parse_args()

    try:
        checker = DeliveryChecker(args.config)
        result = checker.check_delivery(args.change_id, args.project, args.confirm)

        if args.json:
            output = {
                "gate": result.gate_name,
                "score": result.total_score,
                "threshold": result.threshold,
                "passed": result.passed,
                "requires_human_confirmation": result.requires_human_confirmation,
                "human_confirmation_received": result.human_confirmation_received,
                "checks": [
                    {"item": c.item, "passed": c.passed, "score": c.score, "details": c.details}
                    for c in result.checks
                ]
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            exit_code = print_result(result, args.verbose)
            if result.requires_human_confirmation and not result.human_confirmation_received:
                print("提示: 使用 --confirm 参数确认人工通过")
            sys.exit(exit_code)

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
