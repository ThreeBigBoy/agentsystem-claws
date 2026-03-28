#!/usr/bin/env python3
"""
质量门禁两层判断机制完整测试脚本 v2
===================================

架构设计：
┌─────────────────────────────────────────────────────────────────────┐
│  第一层：check_*.py（显式调用入口，由 SKILL.md 触发）              │
│                                                                      │
│  判断用户指令是否使用LLM语义评审：                                   │
│    跳过关键词（不需要LLM等）→ 自动化检查 → python_only              │
│    其他指令 → 自动化检查 + llm_enhancer.analyze_*() → 语义评审       │
│                                                                      │
│                     ↓                                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  第二层：llm_enhancer.py（内部判断）                          │  │
│  │                                                              │  │
│  │  API关键词（用API模型） → _call_api() → API 模型评审          │  │
│  │  其他 → _agent_fallback() → Agent 直接执行评审                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

用户指令场景（6个）：
  #1 请执行评审              → 第一层放行 → 第二层Agent评审
  #2 请执行评审，不要用API模型 → 第一层放行 → 第二层Agent评审
  #3 请执行评审，只需要自动化执行 → 第一层拦截 → python_only
  #4 请执行评审，不要LLM     → 第一层拦截 → python_only
  #5 请执行评审，不使用LLM，可以用API模型 → 第一层拦截 → python_only
  #6 请执行评审，用API模型   → 第一层放行 → 第二层API评审

测试场景矩阵：
| 层级 | 参数/输入 | check_*.py 行为 | llm_enhancer 行为 |
|------|-----------|-----------------|-------------------|
| 第一层 | --skip-llm | 跳过LLM | python_only |
| 第一层 | --user-input含跳过关键词 | 跳过LLM | python_only |
| 第一层 | --user-input无跳过关键词 | 调用LLM | → 第二层 |
| 第二层 | "" 或 "请执行评审" | - | Agent 评审 |
| 第二层 | "用API模型" | - | API 评审 |

测试目标：
1. 第一层判断：验证 --skip-llm 和 --user-input关键词 的行为差异
2. 第二层判断：验证 agent / api 的分支逻辑
3. 集成验证：两层判断正确协作
"""

import os
import sys
import subprocess
import json
import time

os.chdir("/Users/billhu/agentsystem")
sys.path.insert(0, "sys-root/lib/skills/dev-workflow-orchestration/references/quality-gates")

os.environ["SILICONFLOW_API_KEY"] = "sk-hykeoxdjiozbswqeyjpzrcszoeddwnfudolpaewcgdeplesl"
os.environ["MINIMAX_API_KEY"] = "sk-api-BfYM72ltHFHhz-OyiMDE7AqgHMoz-BsJdYVsQo24Nx_J7FqpcAh4q5gT-4LfX7EeYG-n768WwpfGY_nXLash0P34QC_UGLx0ZS4ga4nETE84qRTLxSc9e0A"

prd_file = "/Users/billhu/aiprojects/curiobuddy/docs/project-prd-changes/wechat-miniprogram-v0.1beta/PRD-wechat-miniprogram-v0.1beta-功能需求.md"
solution_file = "/Users/billhu/aiprojects/curiobuddy/openspec/changes/wechat-miniprogram-v0.1beta/proposal.md"
code_dir = "/Users/billhu/aiprojects/curiobuddy/src"

SAMPLE_CONTENT = """
# PRD 示例
## 背景
用户需要一个简单的待办事项管理功能
## 功能
- 添加待办
- 删除待办
- 完成待办
## 验收标准
- [ ] 可以添加待办
- [ ] 可以删除待办
"""


def extract_json(stdout: str) -> str:
    """从 stdout 提取纯 JSON（跳过警告行）"""
    lines = stdout.strip().split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('{'):
            return '\n'.join(lines[i:])
    return stdout.strip()


def run_check(script_name: str, file_path: str, extra_args: list = None, user_input: str = "") -> dict:
    """执行 check_*.py 并返回解析后的结果"""
    script_dir = "sys-root/lib/skills/dev-workflow-orchestration/references/quality-gates"
    cmd = ["python", f"{script_dir}/{script_name}", file_path, "--skip-llm", "--json"]

    if extra_args:
        cmd = ["python", f"{script_dir}/{script_name}", file_path] + extra_args + ["--json"]

    if user_input:
        cmd = ["python", f"{script_dir}/{script_name}", file_path] + extra_args + ["--json", "--user-input", user_input] if extra_args else ["python", f"{script_dir}/{script_name}", file_path, "--json", "--user-input", user_input]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd="/Users/billhu/agentsystem")
        if proc.stdout:
            json_str = extract_json(proc.stdout)
            return json.loads(json_str)
    except subprocess.TimeoutExpired:
        print(f"    ⏱️ 超时（60秒）")
    except json.JSONDecodeError as e:
        print(f"    ❌ JSON解析失败: {e}")
    except Exception as e:
        print(f"    ❌ 执行失败: {e}")
    return {}


class TestRunner:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.results = []

    def add(self, name: str, passed: bool, detail: str = ""):
        self.total += 1
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        self.results.append((name, passed, detail))

    def summary(self):
        print("\n" + "=" * 70)
        print(f"【测试结果】{self.passed}/{self.total} 通过")
        if self.failed > 0:
            for name, _, detail in self.results:
                if detail:
                    print(f"  ❌ {name}: {detail}")
        print("=" * 70)
        return self.failed == 0


def test_first_layer_skip():
    """测试第一层：--skip-llm 跳过 LLM"""
    print("\n" + "=" * 70)
    print("【第一层测试】--skip-llm 跳过 LLM")
    print("=" * 70)

    runner = TestRunner()

    # PRD
    print("\n1. check_prd.py --skip-llm")
    result = run_check("check_prd.py", prd_file, ["--skip-llm"])
    if result:
        no_llm = result.get("llm_analysis") is None and result.get("llm_score") is None
        runner.add("PRD --skip-llm 无LLM分析", no_llm)
        print(f"   {'✅' if no_llm else '❌'} llm_analysis={'无' if no_llm else '有'}")
        print(f"   score={result.get('score')}")
    else:
        runner.add("PRD --skip-llm 执行", False, "执行失败")

    return runner.summary()


def test_first_layer_keywords():
    """测试第一层：用户指令中的关键词自动判断跳过LLM"""
    print("\n" + "=" * 70)
    print("【第一层测试】用户指令关键词 → 自动 --skip-llm")
    print("说明：用户说'不需要LLM'时，check_*.py应自动识别并跳过LLM")
    print("=" * 70)

    runner = TestRunner()

    skip_keywords = [
        "不需要LLM",
        "不要LLM",
        "不需要语义",
        "跳过LLM",
        "只需要自动化",
        "只要自动化",
        "不用LLM",
        "不要语义",
        "不使用LLM",
    ]

    for keyword in skip_keywords:
        print(f"\n  指令含'{keyword}' → 应跳过LLM")
        result = run_check("check_prd.py", prd_file, user_input=keyword)
        if result:
            no_llm = result.get("llm_analysis") is None and result.get("llm_score") is None
            runner.add(f"关键词'{keyword}'跳过LLM", no_llm)
            print(f"     {'✅' if no_llm else '❌'} llm_analysis={'无' if no_llm else '有'}")
        else:
            runner.add(f"关键词'{keyword}'执行", False, "执行失败")

    enable_cases = [
        ("请执行评审", "指令1-放行"),
        ("请执行评审，不要用API模型", "指令2-放行"),
        ("请执行评审，用API模型", "指令6-放行"),
    ]

    print("\n--- 放行场景（应使用LLM）---")
    for user_input, desc in enable_cases:
        print(f"\n  {desc}: '{user_input}' → 应放行使用LLM")
        result = run_check("check_prd.py", prd_file, user_input=user_input)
        if result:
            has_llm = result.get("llm_analysis") is not None
            runner.add(f"{desc}使用LLM", has_llm)
            print(f"     {'✅' if has_llm else '❌'} llm_analysis={'有' if has_llm else '无'}")
        else:
            runner.add(f"{desc}执行", False, "执行失败")

    return runner.summary()


def test_first_layer_enable():
    """测试第一层：--llm 启用 LLM"""
    print("\n" + "=" * 70)
    print("【第一层测试】--llm 启用 LLM（调用 llm_enhancer）")
    print("=" * 70)

    runner = TestRunner()

    print("\n1. check_prd.py --llm")
    result = run_check("check_prd.py", prd_file, ["--llm"])
    if result:
        has_llm = result.get("llm_analysis") is not None
        runner.add("PRD --llm 有LLM分析", has_llm)
        print(f"   {'✅' if has_llm else '❌'} llm_analysis={'有' if has_llm else '无'}")
        print(f"   llm_score={result.get('llm_score')}")
        print(f"   score={result.get('score')}")
    else:
        runner.add("PRD --llm 执行", False, "执行失败")

    return runner.summary()


def test_multi_user_instructions():
    """测试多用户指令模板：验证不同 user_input 触发的不同行为"""
    print("\n" + "=" * 70)
    print("【多用户指令模板测试】验证不同指令触发的场景")
    print("=" * 70)

    from llm_enhancer import LLMEnhancer
    runner = TestRunner()

    test_cases = [
        # 第二层：Agent评审 or API评审（前提：已通过第一层判断，使用LLM）
        # 注意：第一层判断（是否使用LLM）由 check_*.py --skip-llm 独立测试

        # PRD 环节 - 第二层
        ("PRD-Agent默认", "请执行评审", "prd", "agent", True, True),
        ("PRD-Agent不要API模型", "请执行评审，不要用API模型", "prd", "agent", True, True),
        ("PRD-API用API模型", "用API模型", "prd", "api", True, False),
        ("PRD-API请使用API模型", "请使用API模型", "prd", "api", True, False),

        # 方案环节 - 第二层
        ("方案-Agent默认", "请执行评审", "solution", "agent", True, True),
        ("方案-Agent不要API模型", "请执行评审，不要用API模型", "solution", "agent", True, True),
        ("方案-API用API模型", "用API模型", "solution", "api", True, False),

        # 代码环节 - 第二层
        ("代码-Agent默认", "请执行评审", "code", "agent", True, True),
        ("代码-Agent不要API模型", "请执行评审，不要用API模型", "code", "agent", True, True),
        ("代码-API用API模型", "用API模型", "code", "api", True, False),
    ]

    for name, user_input, gate_type, expected_source, expect_llm, expect_feedback in test_cases:
        print(f"\n{name}: user_input='{user_input}'")

        enhancer = LLMEnhancer()

        if gate_type == "prd":
            res = enhancer.analyze_prd(SAMPLE_CONTENT, prd_file, user_input)
        elif gate_type == "solution":
            res = enhancer.analyze_solution(SAMPLE_CONTENT, solution_file, None, user_input)
        elif gate_type == "code":
            res = enhancer.analyze_code(SAMPLE_CONTENT, code_dir, user_input)

        actual_source = res.get("source")

        # API调用可能失败回退到Agent，这是正常行为
        api_fallback = False
        if expected_source == "api" and actual_source == "agent":
            if "Agent 直接执行评审" in res.get("analysis", "") or "🔄" in res.get("analysis", ""):
                api_fallback = True
                print(f"   ⚠️ API调用失败，回退到Agent（正常行为）")

        passed = actual_source == expected_source or api_fallback
        runner.add(f"多指令-{name}", passed)
        print(f"   {'✅' if passed else '❌'} source={actual_source} (期望={expected_source})")

        if not passed:
            continue

        # 验证prompt内容
        analysis = res.get("analysis", "")

        if expected_source == "agent" and actual_source == "agent":
            has_path = gate_type in analysis or "路径" in analysis or "path" in analysis.lower()
            has_feedback_cmd = "--agent-score" in analysis
            runner.add(f"Agent-{name}-含文件路径", has_path)
            runner.add(f"Agent-{name}-含回填命令", has_feedback_cmd)
            print(f"   {'✅' if has_path else '❌'} 含文件路径")
            print(f"   {'✅' if has_feedback_cmd else '❌'} 含回填命令")
        elif expected_source == "api" and actual_source == "api":
            has_content = "PRD" in analysis or "##" in analysis
            no_feedback = "--agent-score" not in analysis
            runner.add(f"API-{name}-含内容", has_content)
            runner.add(f"API-{name}-无回填命令", no_feedback)
            print(f"   {'✅' if has_content else '❌'} 含内容")
            print(f"   {'✅' if no_feedback else '❌'} 无回填命令")

    return runner.summary()


def test_second_layer_llm_enhancer():
    """测试第二层：llm_enhancer 的 agent/api 分支"""
    print("\n" + "=" * 70)
    print("【第二层测试】llm_enhancer agent/api 分支")
    print("=" * 70)

    from llm_enhancer import LLMEnhancer
    runner = TestRunner()

    test_cases = [
        ("", "agent", "默认Agent"),
        ("请执行评审", "agent", "显式Agent"),
        ("请使用API模型", "api", "显式API"),
    ]

    for user_input, expected_source, desc in test_cases:
        print(f"\n{desc}: user_input='{user_input}'")
        enhancer = LLMEnhancer()
        res = enhancer.analyze_prd(SAMPLE_CONTENT, prd_file, user_input)
        actual = res.get("source")

        passed = actual == expected_source
        runner.add(f"llm_enhancer: {desc}", passed)
        print(f"   {'✅' if passed else '❌'} source={actual} (期望={expected_source})")

        if actual == "agent" and expected_source == "agent":
            has_prompt = "--agent-score" in res.get("analysis", "")
            runner.add("Agent分支含回填命令", has_prompt)
            print(f"   {'✅' if has_prompt else '❌'} 含 --agent-score")

    return runner.summary()


def test_integration():
    """集成测试：验证两层判断正确协作"""
    print("\n" + "=" * 70)
    print("【集成测试】两层判断机制协作")
    print("=" * 70)

    runner = TestRunner()

    scenarios = [
        ("--skip-llm", "第一层拦截 → python_only"),
        ("--llm", "第一层放行 → llm_enhancer 第二层判断"),
    ]

    for arg, desc in scenarios:
        print(f"\n{arg}: {desc}")
        result = run_check("check_prd.py", prd_file, [arg])
        if result:
            if arg == "--skip-llm":
                no_llm = result.get("llm_analysis") is None
                runner.add(f"集成-{arg}无LLM", no_llm)
                print(f"   {'✅' if no_llm else '❌'} 无LLM分析")
            else:
                has_llm = result.get("llm_analysis") is not None
                runner.add(f"集成-{arg}有LLM", has_llm)
                print(f"   {'✅' if has_llm else '❌'} 有LLM分析")
                print(f"   score={result.get('score')}")
        else:
            runner.add(f"集成-{arg}执行", False, "执行失败")

    return runner.summary()


def test_prompt_structure():
    """测试：验证 prompt 结构正确性"""
    print("\n" + "=" * 70)
    print("【Prompt结构测试】验证 agent/api 分支 prompt 差异")
    print("=" * 70)

    from llm_enhancer import LLMEnhancer
    runner = TestRunner()
    enhancer = LLMEnhancer()

    # Agent 分支（有 file_path）
    agent_prompt = enhancer._get_prd_review_prompt(SAMPLE_CONTENT, prd_file)
    print("\n1. Agent分支（有 file_path）:")
    has_path = prd_file in agent_prompt or "文件路径" in agent_prompt
    no_content = "PRD 示例" not in agent_prompt
    has_score_cmd = "--agent-score" in agent_prompt
    print(f"   {'✅' if has_path else '❌'} 包含文件路径")
    print(f"   {'✅' if no_content else '❌'} 不含PRD内容")
    print(f"   {'✅' if has_score_cmd else '❌'} 包含回填命令")
    runner.add("Agent分支结构", has_path and no_content and has_score_cmd)

    # API 分支（无 file_path）
    api_prompt = enhancer._get_prd_review_prompt(SAMPLE_CONTENT)
    print("\n2. API分支（无 file_path）:")
    has_content = "PRD 示例" in api_prompt
    no_path = "--agent-score" not in api_prompt
    print(f"   {'✅' if has_content else '❌'} 包含PRD内容")
    print(f"   {'✅' if no_path else '❌'} 不含回填命令")
    runner.add("API分支结构", has_content and no_path)

    return runner.summary()


def test_all_gates():
    """测试所有门禁脚本：4环节 × 多种场景"""
    print("\n" + "=" * 70)
    print("【全门禁测试】PRD/方案/代码/交付 × 多场景")
    print("=" * 70)

    runner = TestRunner()
    error_count = [0]

    gate_configs = [
        ("check_prd.py", prd_file, ["--skip-llm", "--llm"]),
        ("check_solution.py", solution_file, ["--skip-llm", "--llm"]),
        ("check_code.py", code_dir, ["--skip-llm", "--llm"]),
    ]

    for script, path, flags in gate_configs:
        if not os.path.exists(path):
            print(f"\n⚠️ {script}: 文件不存在 {path}，跳过")
            runner.add(f"{script}文件存在", False, "文件不存在")
            continue

        print(f"\n{'='*60}")
        print(f"📋 {script}")
        print(f"{'='*60}")

        for flag in flags:
            desc = "跳过LLM" if flag == "--skip-llm" else "启用LLM"
            print(f"\n  [{desc}] {flag}")
            result = run_check(script, path, [flag])

            if result is None or result == {}:
                print(f"     ❌ 执行失败")
                runner.add(f"{script} {flag}", False, "执行失败")
                error_count[0] += 1
                continue

            total = result.get("score", 0)
            llm_analysis = result.get("llm_analysis")
            llm_score = result.get("llm_score")
            checks = result.get("checks", [])
            python_score = sum(c.get("score", 0) for c in checks)

            print(f"     综合得分: {total}")
            print(f"     Python自动化(原始): {python_score}")

            if flag == "--skip-llm":
                has_llm = llm_analysis is not None
                runner.add(f"{script} {desc}无LLM", not has_llm)
                print(f"     LLM语义评审: {'有' if has_llm else '无'} (期望: 无)")
                print(f"     状态: {'✅' if not has_llm else '❌'}")
            else:
                has_llm = llm_analysis is not None
                runner.add(f"{script} {desc}有LLM", has_llm)
                print(f"     LLM语义评审: {'有' if has_llm else '无'} (期望: 有)")
                print(f"     LLM得分: {llm_score}")
                print(f"     状态: {'✅' if has_llm else '❌'}")

    print(f"\n{'='*60}")
    print(f"📊 测试统计：执行失败次数 = {error_count[0]}")
    print(f"{'='*60}")

    return runner.summary()


def main():
    print("=" * 70)
    print("质量门禁两层判断机制完整测试 v3")
    print("=" * 70)

    all_passed = True

    # 按测试维度分组
    all_passed &= test_first_layer_skip()
    all_passed &= test_first_layer_enable()
    all_passed &= test_multi_user_instructions()
    all_passed &= test_second_layer_llm_enhancer()
    all_passed &= test_prompt_structure()
    all_passed &= test_all_gates()
    all_passed &= test_integration()

    print("\n" + "=" * 70)
    print("【最终结果】")
    print("=" * 70)
    if all_passed:
        print("✅ 所有测试通过！两层判断机制工作正常。")
    else:
        print("❌ 存在失败测试，请检查上述输出。")
    print("=" * 70)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
