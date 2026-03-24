#!/usr/bin/env python3
"""质量门禁2.0完整测试脚本"""
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
    ("默认(Agent)", "请执行评审", "prd"),
    ("不需要LLM", "不需要LLM", "prd"),
    ("不要LLM", "不要LLM", "prd"),
    ("只需要自动化", "只需要自动化", "prd"),
    ("用API模型", "用API模型", "prd"),
    ("用API", "请使用API模型", "prd"),
    ("默认(Agent)", "请执行评审", "solution"),
    ("不需要LLM", "不需要LLM", "solution"),
    ("用API模型", "用API模型", "solution"),
    ("默认(Agent)", "请执行评审", "code"),
    ("不需要LLM", "不需要LLM", "code"),
    ("用API模型", "用API模型", "code"),
]

print("=" * 80)
print("质量门禁2.0完整测试")
print("=" * 80)

for name, user_input, gate_type in test_cases:
    print(f"\n测试: {name} | Gate: {gate_type.upper()}")
    print("-" * 60)
    print(f"指令: {user_input}")

    enhancer = LLMEnhancer()

    if gate_type == "prd":
        result = enhancer.analyze_prd(sample_content, prd_file, user_input)
    elif gate_type == "solution":
        result = enhancer.analyze_solution(sample_content, solution_file, None, user_input)
    elif gate_type == "code":
        result = enhancer.analyze_code(sample_content, code_dir, user_input)

    print(f"Source: {result.get('source')}")
    print(f"Score: {result.get('score')}")
    if result.get('python_check'):
        print(f"Python Score: {result.get('python_check', {}).get('score')}")
    print()

print("=" * 80)
print("测试完成!")
print("=" * 80)
