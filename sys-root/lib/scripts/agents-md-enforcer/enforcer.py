#!/usr/bin/env python3
"""
AGENTS.md 强制检查器

功能：
1. 强制检查是否已读取 AGENTS.md
2. 验证 AGENTS.md 内容完整性
3. 提供清晰的错误信息
4. 支持多种 project 识别方式

使用方式：
    from agents_md_enforcer import AgentsMdEnforcer
    
    enforcer = AgentsMdEnforcer()
    enforcer.enforce("curiobuddy")  # 强制检查，未通过则抛出异常
"""

import os
import re
import yaml
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass


class EnforcementError(Exception):
    """强制检查失败异常"""
    
    def __init__(self, message: str, remediation: str = ""):
        self.message = message
        self.remediation = remediation
        super().__init__(f"{message}\n\n修复建议：{remediation}" if remediation else message)


@dataclass
class AgentsMdConfig:
    """AGENTS.md 配置结构"""
    role: str = ""
    responsibilities: List[str] = None
    tools: List[str] = None
    constraints: List[str] = None
    raw_content: str = ""
    
    def __post_init__(self):
        if self.responsibilities is None:
            self.responsibilities = []
        if self.tools is None:
            self.tools = []
        if self.constraints is None:
            self.constraints = []


class AgentsMdEnforcer:
    """
    AGENTS.md 强制检查器
    
    确保 Agent 在执行任务前已读取并理解项目的 AGENTS.md 配置。
    """
    
    def __init__(self, base_path: str = "/Users/billhu/agentsystem/workspace"):
        """
        初始化检查器
        
        Args:
            base_path: project workspace 根目录
        """
        self.base_path = Path(base_path)
        self._loaded_configs: Dict[str, AgentsMdConfig] = {}
        # workspace/{project}/ 下通过 claw-config 软链指向仓库内 claw-config/；AGENTS.md 在该目录内
        self.claw_config_dirname = "claw-config"

    def _agents_md_path(self, project_path: Path) -> Path:
        """项目运行时 AGENTS.md：{project}/claw-config/AGENTS.md"""
        return project_path / self.claw_config_dirname / "AGENTS.md"

    def enforce(self, project_name: str) -> AgentsMdConfig:
        """
        强制检查：必须已读取 AGENTS.md
        
        Args:
            project_name: 项目名称（如 "curiobuddy"）
            
        Returns:
            AgentsMdConfig: 解析后的配置
            
        Raises:
            EnforcementError: 如果 AGENTS.md 不存在或无效
        """
        # 1. 检查 project 目录是否存在
        project_path = self.base_path / project_name
        if not project_path.exists():
            raise EnforcementError(
                message=f"Project '{project_name}' 不存在",
                remediation=f"请确认 project 名称正确，或创建目录：{project_path}"
            )
        
        # 2. 检查 AGENTS.md 是否存在（位于 claw-config/，与 workspace 软链约定一致）
        agents_md_path = self._agents_md_path(project_path)
        if not agents_md_path.exists():
            raise EnforcementError(
                message=f"必须读取 AGENTS.md 才能执行任务",
                remediation=(
                    f"请在项目中创建或链接 claw-config，并放置 AGENTS.md：{agents_md_path}\n"
                    f"（workspace 侧一般为 workspace/{project_name}/claw-config -> 项目仓库内 claw-config/）"
                ),
            )
        
        # 3. 读取并解析 AGENTS.md
        try:
            config = self._parse_agents_md(agents_md_path)
            self._loaded_configs[project_name] = config
            return config
        except Exception as e:
            raise EnforcementError(
                message=f"AGENTS.md 解析失败: {str(e)}",
                remediation="请检查 AGENTS.md 格式是否正确（YAML frontmatter + Markdown）"
            )
    
    def _parse_agents_md(self, file_path: Path) -> AgentsMdConfig:
        """
        解析 AGENTS.md 文件
        
        支持格式：
        ---
        role: "教育助手"
        responsibilities:
          - 帮助学生理解概念
          - 生成练习题
        ---
        
        # 详细说明...
        """
        content = file_path.read_text(encoding='utf-8')
        
        # 提取 YAML frontmatter
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if yaml_match:
            try:
                yaml_content = yaml_match.group(1)
                metadata = yaml.safe_load(yaml_content) or {}
            except yaml.YAMLError:
                metadata = {}
        else:
            metadata = {}
        
        return AgentsMdConfig(
            role=metadata.get('role', ''),
            responsibilities=metadata.get('responsibilities', []),
            tools=metadata.get('tools', []),
            constraints=metadata.get('constraints', []),
            raw_content=content
        )
    
    def verify_loaded(self, project_name: str) -> bool:
        """
        验证是否已加载 AGENTS.md
        
        Args:
            project_name: 项目名称
            
        Returns:
            bool: 是否已加载
        """
        return project_name in self._loaded_configs
    
    def get_config(self, project_name: str) -> Optional[AgentsMdConfig]:
        """
        获取已加载的配置
        
        Args:
            project_name: 项目名称
            
        Returns:
            AgentsMdConfig or None: 配置对象，未加载则返回 None
        """
        return self._loaded_configs.get(project_name)
    
    def list_projects(self) -> List[str]:
        """
        列出所有可用的 project
        
        Returns:
            List[str]: project 名称列表
        """
        if not self.base_path.exists():
            return []
        
        projects = []
        for item in self.base_path.iterdir():
            if item.is_dir() and self._agents_md_path(item).exists():
                projects.append(item.name)
        return sorted(projects)


def quick_enforce(project_name: str) -> AgentsMdConfig:
    """
    快速强制检查函数
    
    便捷函数，一行代码完成检查。
    
    Args:
        project_name: 项目名称
        
    Returns:
        AgentsMdConfig: 配置对象
        
    Raises:
        EnforcementError: 检查失败
        
    Example:
        >>> config = quick_enforce("curiobuddy")
        >>> print(config.role)
        'K12 教育助手'
    """
    enforcer = AgentsMdEnforcer()
    return enforcer.enforce(project_name)


# 命令行接口
if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="AGENTS.md 强制检查")
    parser.add_argument("project", help="项目名称")
    parser.add_argument("--check-only", action="store_true", help="仅检查，不抛出异常")
    
    args = parser.parse_args()
    
    try:
        config = quick_enforce(args.project)
        print(f"✅ AGENTS.md 检查通过")
        print(f"   项目: {args.project}")
        print(f"   角色: {config.role}")
        print(f"   职责: {len(config.responsibilities)} 项")
        sys.exit(0)
    except EnforcementError as e:
        print(f"❌ AGENTS.md 检查失败")
        print(f"   错误: {e.message}")
        if e.remediation:
            print(f"   建议: {e.remediation}")
        sys.exit(1)
