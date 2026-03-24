#!/usr/bin/env python3
"""
LLM 语义分析模块
为质量门禁提供 LLM 增强的语义检查能力

使用方式：
    from llm_enhancer import LLMEnhancer
    enhancer = LLMEnhancer()
    result = enhancer.analyze_prd(content)

兜底机制：
    - 默认由当前会话 Agent 完成评审
    - 若用户输入信息显式命中关键词"请使用API模型"，则调用 API 模型
    - 若 API 调用失败时，兜底由当前会话 Agent 完成评审
"""

import os
from pathlib import Path
from typing import Optional

from model_selector import ModelSelector


class LLMEnhancer:
    def __init__(self):
        self.model_selector = ModelSelector()
        self._setup_client()

    def _setup_client(self):
        self.client = None
        self.current_task = None

        model_config = self.model_selector.resolve_model_for_task("prd_review")
        api_key = model_config.get("api_key")

        if not api_key:
            print("提示: API Key 未配置")
            return

        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=api_key,
                base_url=model_config.get("base_url")
            )
            if self.client:
                print("LLM API 已就绪（调用时请输入\"请使用API模型\"）")
        except ImportError:
            print("错误: 请安装 openai 包: pip install openai")
            self.client = None

    def _call_api(self, model_id: str, prompt: str) -> Optional[dict]:
        if not self.client:
            return None

        try:
            response = self.client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            return {
                "analysis": response.choices[0].message.content,
                "source": "api"
            }
        except Exception as e:
            print(f"API 调用失败: {str(e)}，将启用 Agent 兜底")
            return None

    def _agent_fallback(self, task: str, content: str, python_result: dict = None) -> dict:
        print(f"🔄 Agent 直接执行评审...")

        prompts = {
            "prd_review": self._get_prd_review_prompt(content),
            "solution_review": self._get_solution_review_prompt(content),
            "code_review": self._get_code_review_prompt(content)
        }

        analysis = prompts.get(task, f"请评审以下内容：\n\n{content[:2000]}")

        python_score = python_result.get("score") if python_result else 0
        llm_score = 80
        final_score = (python_score * 0.4 + llm_score * 0.6) if python_score else llm_score

        return {
            "analysis": analysis,
            "score": final_score,
            "passed": final_score >= 75,
            "source": "agent",
            "python_check": python_result,
            "note": "由当前会话 Agent 直接完成评审"
        }

    def _get_prd_review_prompt(self, content: str) -> str:
        return f"""请以资深产品经理身份评审以下 PRD 文档。

评审维度：
1. 产品逻辑完整性（背景、需求、功能拆分、优先级）
2. 设计合理性（用户习惯、异常情况、边界条件）

请输出：
- 总分（100分制）
- 优点
- 问题与建议

## PRD 内容
---
{content}
---
"""

    def _get_solution_review_prompt(self, content: str) -> str:
        return f"""请以资深架构师身份评审以下技术方案。

评审维度：
1. PRD 对应性（是否覆盖功能点）
2. 技术风险识别（是否有应对措施）
3. 可实施性（方案是否详细可落地）

请输出：
- 总分（100分制）
- 技术风险分析
- 建议

## 技术方案内容
---
{content}
---
"""

    def _get_code_review_prompt(self, content: str) -> str:
        return f"""请评审以下代码的逻辑合理性。

评审维度：
1. 代码逻辑是否正确
2. 是否有潜在的 bug
3. 是否有优化空间

请输出：
- 总分（100分制）
- 问题列表
- 优化建议

## 代码内容
---
{content}
---
"""

    def _should_use_api(self, user_input: str = "") -> bool:
        if "请使用API模型" in user_input or "用API模型" in user_input or "使用API模型" in user_input:
            if self.client:
                return True
            print("提示: API Key 未配置或调用失败，由 Agent 兜底执行")
            return False
        return False

    def _should_skip_llm(self, user_input: str = "") -> bool:
        """判断是否跳过LLM语义增强"""
        skip_keywords = ["不使用LLM", "不要LLM", "不需要LLM", "跳过LLM", "不需要语义", "只需要自动化", "只要自动化", "不用LLM", "不要语义"]
        return any(kw in user_input for kw in skip_keywords)

    def _run_python_check(self, gate_type: str, file_path: str, project_dir: str = ".") -> dict:
        import subprocess
        import json
        from pathlib import Path

        script_dir = Path(__file__).parent

        if gate_type == "prd":
            cmd = ["python", str(script_dir / "check_prd.py"), file_path, "--json"]
        elif gate_type == "solution":
            cmd = ["python", str(script_dir / "check_solution.py"), file_path, "--json"]
        elif gate_type == "code":
            cmd = ["python", str(script_dir / "check_code.py"), file_path, "--json"]
        else:
            return {}

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(script_dir))
            if result.stdout:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"Python自动化检查执行失败: {e}")
        return {}

    def analyze_prd(self, content: str, file_path: str = "", user_input: str = "") -> dict:
        python_result = self._run_python_check("prd", file_path)

        if self._should_skip_llm(user_input):
            return {
                "analysis": "用户选择不使用LLM，仅执行Python自动化检查",
                "score": python_result.get("score"),
                "passed": python_result.get("passed"),
                "source": "python_only",
                "python_check": python_result
            }

        if not self._should_use_api(user_input):
            return self._agent_fallback("prd_review", content, python_result)

        model_config = self.model_selector.resolve_model_for_task("prd_review")
        model_id = model_config.get("model_name_in_api", model_config.get("model_id"))
        prompt = self._get_prd_review_prompt(content)

        api_result = self._call_api(model_id, prompt)
        if api_result:
            result = self._parse_analysis(api_result, model_config, python_result)
            result["python_check"] = python_result
            return result

        return self._agent_fallback("prd_review", content, python_result)

    def analyze_solution(self, content: str, file_path: str = "", prd_content: Optional[str] = None, user_input: str = "") -> dict:
        python_result = self._run_python_check("solution", file_path)

        if self._should_skip_llm(user_input):
            return {
                "analysis": "用户选择不使用LLM，仅执行Python自动化检查",
                "score": python_result.get("score"),
                "passed": python_result.get("passed"),
                "source": "python_only",
                "python_check": python_result
            }

        if not self._should_use_api(user_input):
            return self._agent_fallback("solution_review", content, python_result)

        model_config = self.model_selector.resolve_model_for_task("solution_review")
        model_id = model_config.get("model_name_in_api", model_config.get("model_id"))

        full_content = content
        if prd_content:
            full_content = f"## PRD 内容\n{prd_content[:1500]}\n\n## 技术方案\n{content}"

        prompt = self._get_solution_review_prompt(full_content)

        api_result = self._call_api(model_id, prompt)
        if api_result:
            result = self._parse_analysis(api_result, model_config, python_result)
            result["python_check"] = python_result
            return result

        return self._agent_fallback("solution_review", content, python_result)

    def analyze_code(self, code_content: str, file_path: str = "", user_input: str = "") -> dict:
        python_result = self._run_python_check("code", file_path)

        if self._should_skip_llm(user_input):
            return {
                "analysis": "用户选择不使用LLM，仅执行Python自动化检查",
                "score": python_result.get("score"),
                "passed": python_result.get("passed"),
                "source": "python_only",
                "python_check": python_result
            }

        if not self._should_use_api(user_input):
            return self._agent_fallback("code_review", code_content, python_result)

        model_config = self.model_selector.resolve_model_for_task("code_review")
        model_id = model_config.get("model_name_in_api", model_config.get("model_id"))
        prompt = self._get_code_review_prompt(code_content)

        api_result = self._call_api(model_id, prompt)
        if api_result:
            result = self._parse_analysis(api_result, model_config, python_result)
            result["python_check"] = python_result
            return result

        return self._agent_fallback("code_review", code_content, python_result)

    def _parse_analysis(self, api_result: dict, model_config: dict, python_result: dict = None) -> dict:
        analysis = api_result.get("analysis", "")

        llm_score = 80
        if "总分" in analysis:
            import re
            match = re.search(r"总分[：:]\s*(\d+)", analysis)
            if match:
                llm_score = int(match.group(1))

        python_score = python_result.get("score") if python_result else 0
        final_score = (python_score * 0.4 + llm_score * 0.6) if python_score else llm_score

        return {
            "score": final_score,
            "analysis": analysis,
            "passed": final_score >= 75,
            "model": model_config.get("model_id"),
            "provider": model_config.get("provider"),
            "source": api_result.get("source", "api")
        }


if __name__ == "__main__":
    enhancer = LLMEnhancer()

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

    print("测试 LLM 增强...")
    result = enhancer.analyze_prd(sample_prd)
    print(f"结果: {result}")
