#!/usr/bin/env python3
"""
质量门禁主入口
统一调用 4 个质量门禁脚本

使用方法：
    python run_gates.py <gate_name> [options]
    python run_gates.py prd <prd_file>
    python run_gates.py solution <solution_file> --prd <prd_file>
    python run_gates.py code <project_dir>
    python run_gates.py delivery <change_id> --project <project_dir>
    python run_gates.py all <project_dir> --change-id <change_id>

可用门禁：
    prd        - PRD 质量门禁
    solution   - 方案质量门禁
    code       - 代码质量门禁
    delivery   - 交付质量门禁
    all        - 运行所有门禁
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional


SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.yaml"


def run_prd_gate(prd_file: str, enable_llm: bool = False) -> dict:
    cmd = ["python", str(SCRIPT_DIR / "check_prd.py"), prd_file, "--config", str(CONFIG_FILE)]
    if enable_llm:
        cmd.append("--llm")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "gate": "prd",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


def run_solution_gate(solution_file: str, prd_file: Optional[str] = None, enable_llm: bool = False) -> dict:
    cmd = ["python", str(SCRIPT_DIR / "check_solution.py"), solution_file, "--config", str(CONFIG_FILE)]
    if prd_file:
        cmd.extend(["--prd", prd_file])
    if enable_llm:
        cmd.append("--llm")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "gate": "solution",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


def run_code_gate(project_dir: str, enable_llm: bool = False) -> dict:
    cmd = ["python", str(SCRIPT_DIR / "check_code.py"), project_dir, "--config", str(CONFIG_FILE)]
    if enable_llm:
        cmd.append("--llm")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "gate": "code",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


def run_delivery_gate(change_id: str, project_dir: str, confirm: bool = False) -> dict:
    cmd = ["python", str(SCRIPT_DIR / "check_delivery.py"), change_id, "--project", project_dir, "--config", str(CONFIG_FILE)]
    if confirm:
        cmd.append("--confirm")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "gate": "delivery",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


def run_all_gates(project_dir: str, change_id: str, enable_llm: bool = False, confirm: bool = False) -> list[dict]:
    results = []

    prd_file = Path(project_dir) / "docs" / "project-prd-changes" / change_id
    prd_candidates = list(prd_file.glob("PRD-*.md")) + list(prd_file.glob("功能需求*.md"))
    if prd_candidates:
        results.append(run_prd_gate(str(prd_candidates[0]), enable_llm))

    solution_file = Path(project_dir) / "openspec" / "changes" / change_id / "design.md"
    if solution_file.exists():
        prd_path = str(prd_candidates[0]) if prd_candidates else None
        results.append(run_solution_gate(str(solution_file), prd_path, enable_llm))

    results.append(run_code_gate(project_dir, enable_llm))
    results.append(run_delivery_gate(change_id, project_dir, confirm))

    return results


def print_summary(results: list[dict]):
    print(f"\n{'='*60}")
    print(f"📊 质量门禁汇总")
    print(f"{'='*60}")

    gate_names = {
        "prd": "PRD 质量",
        "solution": "方案质量",
        "code": "代码质量",
        "delivery": "交付质量"
    }

    all_passed = True
    for r in results:
        gate_name = gate_names.get(r["gate"], r["gate"])
        status = "✅ 通过" if r["returncode"] == 0 else "❌ 未通过"
        if r["returncode"] != 0:
            all_passed = False
        print(f"{gate_name}: {status}")

    print(f"{'='*60}")
    if all_passed:
        print("🎉 所有门禁通过！")
    else:
        print("⚠️ 部分门禁未通过，请检查上方详情")

    return 0 if all_passed else 1


def main():
    parser = argparse.ArgumentParser(description="质量门禁主入口")
    parser.add_argument("gate", choices=["prd", "solution", "code", "delivery", "all"], help="门禁类型")
    parser.add_argument("path", help="文件路径或项目目录")
    parser.add_argument("--prd", help="PRD 文件路径（用于方案门禁）")
    parser.add_argument("--project", help="项目目录路径")
    parser.add_argument("--change-id", help="Change ID（用于交付门禁和全量检查）")
    parser.add_argument("--llm", action="store_true", help="启用 LLM 增强")
    parser.add_argument("--confirm", action="store_true", help="人工确认通过（用于交付门禁）")
    parser.add_argument("--json", action="store_true", help="JSON 输出")

    args = parser.parse_args()

    try:
        if args.gate == "prd":
            result = run_prd_gate(args.path, args.llm)
            print(result["stdout"])
            if result["stderr"]:
                print(result["stderr"], file=sys.stderr)
            sys.exit(result["returncode"])

        elif args.gate == "solution":
            result = run_solution_gate(args.path, args.prd, args.llm)
            print(result["stdout"])
            if result["stderr"]:
                print(result["stderr"], file=sys.stderr)
            sys.exit(result["returncode"])

        elif args.gate == "code":
            result = run_code_gate(args.path, args.llm)
            print(result["stdout"])
            if result["stderr"]:
                print(result["stderr"], file=sys.stderr)
            sys.exit(result["returncode"])

        elif args.gate == "delivery":
            if not args.project or not args.change_id:
                print("错误: 交付门禁需要 --project 和 --change-id 参数", file=sys.stderr)
                sys.exit(1)
            result = run_delivery_gate(args.change_id, args.project, args.confirm)
            print(result["stdout"])
            if result["stderr"]:
                print(result["stderr"], file=sys.stderr)
            sys.exit(result["returncode"])

        elif args.gate == "all":
            if not args.project or not args.change_id:
                print("错误: 全量检查需要 --project 和 --change-id 参数", file=sys.stderr)
                sys.exit(1)
            results = run_all_gates(args.project, args.change_id, args.llm, args.confirm)
            if args.json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                exit_code = print_summary(results)
                sys.exit(exit_code)

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
