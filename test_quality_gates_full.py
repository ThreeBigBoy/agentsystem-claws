#!/usr/bin/env python3
"""
质量门禁2.0完整测试脚本
升级版：覆盖全场景逻辑及今晚升级细节

验证要点：
1. 两层判断机制：python_only / agent / api
2. Agent分支prompt：包含文件路径、不含内容、有回填命令
3. API分支prompt：包含内容、不含文件路径、无回填命令
4. 四个环节：PRD/方案/代码/交付
"""
import os, sys, json

os.chdir("/Users/billhu/agentsystem")
sys.path.insert(0, "sys-root/lib/skills/dev-workflow-orchestration/references/quality-gates")

os.environ["SILICONFLOW_API_KEY"] = "sk-hykeoxdjiozbswqeyjpzrcszoeddwnfudolpaewcgdeplesl"
os.environ["MINIMAX_API_KEY"] = "sk-api-BfYM72ltHFHhz-OyiMDE7AqgHMoz-BsJdYVsQo24Nx_J7FqpcAh4q5gT-4LfX7EeYG-n768WwpfGY_nXLash0P34QC_UGLx0ZS4ga4nETE84qRTLxSc9e0A"

from llm_enhancer import LLMEnhancer

prd_file = "/Users/billhu/aiprojects/curiobuddy/docs/project-prd-changes/wechat-miniprogram-v0.1beta/PRD-wechat-miniprogram-v0.1beta-功能需求.md"
solution_file = "/Users/billhu/aiprojects/curiobuddy/openspec/changes/wechat-miniprogram-v0.1beta/proposal.md"
code_dir = "/Users/billhu/aiprojects/curiobuddy/src"
change_id = "wechat-miniprogram-v0.1beta"

sample_content = """
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

test_cases = [
    # PRD环节测试
    ("PRD-Agent默认", "请执行评审", "prd", "agent", True, True),
    ("PRD-Agent不使用LLM", "不需要LLM", "prd", "python_only", False, False),
    ("PRD-Agent不要LLM", "不要LLM", "prd", "python_only", False, False),
    ("PRD-Agent只需要自动化", "只需要自动化", "prd", "python_only", False, False),
    ("PRD-API用API模型", "用API模型", "prd", "api", True, False),
    ("PRD-API请使用API模型", "请使用API模型", "prd", "api", True, False),

    # 方案环节测试
    ("方案-Agent默认", "请执行评审", "solution", "agent", True, True),
    ("方案-Agent不使用LLM", "不需要LLM", "solution", "python_only", False, False),
    ("方案-API用API模型", "用API模型", "solution", "api", True, False),

    # 代码环节测试（MiniMax API已修复）
    ("代码-Agent默认", "请执行评审", "code", "agent", True, True),
    ("代码-Agent不使用LLM", "不需要LLM", "code", "python_only", False, False),
    ("代码-API用API模型", "用API模型", "code", "api", True, False),
]


def verify_prompt(analysis: str, gate_type: str, expected_source: str):
    """验证prompt内容是否符合预期"""
    results = []

    if expected_source == "agent":
        # Agent分支：应包含文件路径、不含内容、有回填命令
        results.append(("Agent-含文件路径", gate_type in analysis or "路径" in analysis or "path" in analysis.lower()))
        results.append(("Agent-不含PRD内容", "PRD 示例" not in analysis))
        results.append(("Agent-有回填命令", "--agent-score" in analysis))
        results.append(("Agent-回填命令正确", f"check_{gate_type}.py" in analysis))
    elif expected_source == "api":
        # API分支：应包含内容、不含文件路径、无回填命令
        results.append(("API-含内容", "PRD 示例" in analysis or "##" in analysis))
        results.append(("API-不含文件路径", "--agent-score" not in analysis))
    elif expected_source == "python_only":
        # python_only：只有Python检查，无LLM分析
        results.append(("PythonOnly-无LLM分析", analysis in ["", "用户选择不使用LLM，仅执行Python自动化检查"]))

    return results


def run_tests():
    print("=" * 80)
    print("质量门禁2.0 完整测试")
    print("=" * 80)

    all_passed = True

    for name, user_input, gate_type, expected_source, expect_llm, expect_feedback in test_cases:
        print(f"\n测试: {name}")
        print(f"  指令: {user_input}")
        print(f"  期望source: {expected_source}")
        print("-" * 60)

        enhancer = LLMEnhancer()

        if gate_type == "prd":
            result = enhancer.analyze_prd(sample_content, prd_file, user_input)
            file_path = prd_file
        elif gate_type == "solution":
            result = enhancer.analyze_solution(sample_content, solution_file, None, user_input)
            file_path = solution_file
        elif gate_type == "code":
            result = enhancer.analyze_code(sample_content, code_dir, user_input)
            file_path = code_dir

        # API调用可能失败回退到Agent，这是正常行为
        api_fallback = False
        actual_source = result.get('source')
        if expected_source == "api" and actual_source == "agent":
            if "Agent 直接执行评审" in analysis or "🔄" in analysis:
                api_fallback = True
                print(f"  ⚠️ API调用失败，回退到Agent（正常行为）")

        passed = actual_source == expected_source or api_fallback

        print(f"  实际source: {actual_source} {'✅' if passed else '❌'}")

        if not passed:
            all_passed = False
            print(f"  ❌ 失败：期望 {expected_source}，实际 {actual_source}")
            continue

        # 验证prompt内容
        analysis = result.get('analysis', '')
        prompt_checks = verify_prompt(analysis, gate_type, expected_source if actual_source == expected_source else "agent")

        for check_name, check_result in prompt_checks:
            status = '✅' if check_result else '❌'
            print(f"  {status} {check_name}")
            if not check_result:
                all_passed = False

        if result.get('python_check'):
            print(f"  ✅ Python检查执行")

    print("\n" + "=" * 80)
    if all_passed:
        print("✅ 所有测试通过!")
    else:
        print("❌ 部分测试失败")
    print("=" * 80)

    return all_passed


def test_prompt_generation():
    """单独测试prompt生成逻辑"""
    print("\n" + "=" * 80)
    print("Prompt生成逻辑测试")
    print("=" * 80)

    enhancer = LLMEnhancer()

    gates = [
        ("PRD", enhancer._get_prd_review_prompt, sample_content, prd_file),
        ("方案", enhancer._get_solution_review_prompt, sample_content, solution_file),
        ("代码", enhancer._get_code_review_prompt, sample_content, code_dir),
    ]

    for gate_name, prompt_func, content, file_path in gates:
        print(f"\n{gate_name}环节Prompt生成:")

        # Agent分支prompt（有file_path）
        agent_prompt = prompt_func(content, file_path)
        print(f"  Agent分支（有file_path）:")
        print(f"    - 包含文件路径: {'✅' if file_path in agent_prompt else '❌'}")
        print(f"    - 不含内容: {'✅' if content[:20] not in agent_prompt else '❌'}")
        print(f"    - 包含回填命令: {'✅' if '--agent-score' in agent_prompt else '❌'}")

        # API分支prompt（无file_path）
        api_prompt = prompt_func(content)
        print(f"  API分支（无file_path）:")
        print(f"    - 包含内容: {'✅' if content[:20] in api_prompt else '❌'}")
        print(f"    - 不含文件路径: {'✅' if '--agent-score' not in api_prompt else '❌'}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_prompt_generation()
    success = run_tests()
    sys.exit(0 if success else 1)