"""
兼容模块名 `agents_md_enforcer`（目录名为 agents-md-enforcer，不能直接作为 Python 包名）。

用法：将本目录加入 PYTHONPATH 后：
    from agents_md_enforcer import quick_enforce, AgentsMdEnforcer, EnforcementError

与 `enforcer.py` 为同一实现的重导出，便于规则文档与脚本中的 import 一致。
"""

from enforcer import AgentsMdEnforcer, EnforcementError, quick_enforce

__all__ = ["AgentsMdEnforcer", "EnforcementError", "quick_enforce"]
