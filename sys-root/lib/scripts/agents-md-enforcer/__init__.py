"""
AGENTS.md 强制检查模块

确保 Agent 在执行任务前必须读取项目的 AGENTS.md 配置。
Hybrid 模式的 enforcement 层。
"""

from .enforcer import AgentsMdEnforcer, EnforcementError, quick_enforce

__version__ = "1.0.0"
__all__ = ["AgentsMdEnforcer", "EnforcementError", "quick_enforce"]
