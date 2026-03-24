#!/usr/bin/env python3
"""
AGENTS.md 强制检查器测试脚本

使用方法：
    python test-enforcer.py [project_name]

示例：
    python test-enforcer.py curiobuddy
"""

import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from enforcer import quick_enforce, EnforcementError


def test_enforcer(project_name: str = "curiobuddy"):
    """测试强制检查器"""
    
    print(f"🧪 测试 AGENTS.md 强制检查器")
    print(f"   Project: {project_name}")
    print(f"   路径: /Users/billhu/agentsystem/workspace/{project_name}/claw-config/AGENTS.md")
    print()
    
    try:
        config = quick_enforce(project_name)
        
        print(f"✅ 检查通过！")
        print(f"   角色: {config.role}")
        print(f"   职责数: {len(config.responsibilities)}")
        print(f"   工具数: {len(config.tools)}")
        
        if config.responsibilities:
            print(f"\n   主要职责:")
            for i, resp in enumerate(config.responsibilities[:3], 1):
                print(f"   {i}. {resp}")
        
        return 0
        
    except EnforcementError as e:
        print(f"❌ 检查失败")
        print(f"   错误: {e.message}")
        if e.remediation:
            print(f"\n   💡 修复建议:")
            print(f"   {e.remediation}")
        return 1
    
    except Exception as e:
        print(f"💥 意外错误: {str(e)}")
        return 2


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="测试 AGENTS.md 强制检查器")
    parser.add_argument("project", nargs="?", default="curiobuddy", help="项目名称")
    args = parser.parse_args()
    
    sys.exit(test_enforcer(args.project))
