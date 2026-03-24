#!/usr/bin/env python3
"""质量门禁2.0测试脚本"""
import os, sys, json

os.chdir("/Users/billhu/agentsystem/sys-root/lib/skills/dev-workflow-orchestration/references/quality-gates")
sys.path.insert(0, ".")

os.environ["SILICONFLOW_API_KEY"] = "sk-hykeoxdjiozbswqeyjpzrcszoeddwnfudolpaewcgdeplesl"
os.environ["MINIMAX_API_KEY"] = "sk-api-BfYM72ltHFHhz-OyiMDE7AqgHMoz-BsJdYVsQo24Nx_J7FqpcAh4q5gT-4LfX7EeYG-n768WwpfGY_nXLash0P34QC_UGLx0ZS4ga4nETE84qRTLxSc9e0A"

from llm_enhancer import LLMEnhancer

sample_prd = """
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

prd_file = "/Users/billhu/aiprojects/curiobuddy/docs/project-prd-changes/wechat-miniprogram-v0.1beta/PRD-wechat-miniprogram-v0.1beta-功能需求.md"

print("=" * 60)
print("测试1: 默认场景（无关键词）")
print("=" * 60)
enhancer = LLMEnhancer()
result = enhancer.analyze_prd(sample_prd, prd_file, "请执行评审")
print(f"Source: {result.get('source')}")
print(f"Has Python Check: {'python_check' in result}")
print(f"Score: {result.get('score')}")
print()

print("=" * 60)
print("测试2: 只需要自动化（跳过LLM）")
print("=" * 60)
result = enhancer.analyze_prd(sample_prd, prd_file, "请执行评审，不需要LLM")
print(f"Source: {result.get('source')}")
print(f"Has Python Check: {'python_check' in result}")
print(f"Score: {result.get('score')}")
print()

print("=" * 60)
print("测试3: 用API模型")
print("=" * 60)
result = enhancer.analyze_prd(sample_prd, prd_file, "请执行评审，用API模型")
print(f"Source: {result.get('source')}")
print(f"Has Python Check: {'python_check' in result}")
print(f"Score: {result.get('score')}")
print(f"Model: {result.get('model', 'N/A')}")
print()

print("=" * 60)
print("测试4: 不要LLM（只做Python检查）")
print("=" * 60)
result = enhancer.analyze_prd(sample_prd, prd_file, "不要LLM")
print(f"Source: {result.get('source')}")
print(f"Has Python Check: {'python_check' in result}")
print(f"Score: {result.get('score')}")
print()

print("=" * 60)
print("测试完成！")
print("=" * 60)
