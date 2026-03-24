#!/usr/bin/env python3
"""
MCP Server: Quality Gates
使用 MCP SDK 实现质量门禁服务

调用链路：
  Trae (MCP Client)
       │
       ▼
  mcp_server.py (自动检测 change-id 和当前阶段)
       │
       ▼
  check_*.py (执行实际门禁检查)
"""

import json
import subprocess
import sys
import yaml
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

MCP_CONFIG = "/Users/billhu/agentsystem/sys-root/lib/scripts/quality-gates/mcp-wrappers/mcp_config.yaml"
CHECK_SCRIPTS = "/Users/billhu/agentsystem/sys-root/lib/scripts/quality-gates"

server = Server("quality-gates")


def load_mcp_config():
    with open(MCP_CONFIG, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_openspec_dir():
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        openspec = parent / "openspec"
        if openspec.exists() and openspec.is_dir():
            return openspec
    return None


def discover_change_id():
    openspec = find_openspec_dir()
    if not openspec:
        return None, None

    changes_dir = openspec / "changes"
    if not changes_dir.exists():
        return None, None

    change_ids = [d.name for d in changes_dir.iterdir() if d.is_dir()]
    if not change_ids:
        return None, None

    active_change_id = change_ids[0]
    project_dir = openspec.parent

    return active_change_id, project_dir


def read_current_phase(change_id, project_dir):
    tasks_file = project_dir / "openspec" / "changes" / change_id / "tasks.md"
    if not tasks_file.exists():
        return None

    content = tasks_file.read_text(encoding="utf-8")
    for line in content.split("\n"):
        if "**Step" in line and "启动准入检查" in line:
            parts = line.split("**Step")[1].split("**")[0]
            return parts.strip()

    return None


def determine_next_gate(current_phase):
    gate_mapping = {
        "1": "prd",
        "2": "solution",
        "3": "code",
        "4": "delivery",
    }
    return gate_mapping.get(current_phase, "prd")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="check_prd",
            description="PRD质量门禁检查",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="check_solution",
            description="方案质量门禁检查",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="check_code",
            description="代码质量门禁检查",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="check_delivery",
            description="交付质量门禁检查",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="gate_status",
            description="查询当前项目所处阶段和待执行的门禁",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    change_id, project_dir = discover_change_id()

    if not change_id:
        return [TextContent(type="text", text=json.dumps({
            "error": "无法发现 change-id，请确认当前目录是否为业务项目根目录",
            "cwd": str(Path.cwd())
        }, ensure_ascii=False))]

    config = load_mcp_config()

    if name == "gate_status":
        current_phase = read_current_phase(change_id, project_dir)
        next_gate = determine_next_gate(current_phase) if current_phase else "prd"

        return [TextContent(type="text", text=json.dumps({
            "change_id": change_id,
            "project_dir": str(project_dir),
            "current_phase": current_phase,
            "next_gate": next_gate,
            "cwd": str(Path.cwd())
        }, ensure_ascii=False))]

    gate_name = name.replace("check_", "")
    gate_config = config.get("quality_gates", {}).get(gate_name, {})

    if not gate_config:
        return [TextContent(type="text", text=json.dumps({
            "error": f"未找到 {name} 的配置"
        }, ensure_ascii=False))]

    if name == "check_prd":
        prd_file = str(
            project_dir / "docs" / "project-prd-changes" / change_id /
            f"PRD-{change_id}-功能需求.md"
        )
        cmd = [
            sys.executable,
            f"{CHECK_SCRIPTS}/check_prd.py",
            prd_file,
            "--config", gate_config["config"],
            "--json"
        ]
    elif name == "check_solution":
        solution_file = str(
            project_dir / "openspec" / "changes" / change_id / "proposal.md"
        )
        cmd = [
            sys.executable,
            f"{CHECK_SCRIPTS}/check_solution.py",
            solution_file,
            "--config", gate_config["config"],
            "--json"
        ]
    elif name == "check_code":
        project_src = str(project_dir / "src")
        cmd = [
            sys.executable,
            f"{CHECK_SCRIPTS}/check_code.py",
            project_src,
            "--config", gate_config["config"],
            "--json"
        ]
    elif name == "check_delivery":
        cmd = [
            sys.executable,
            f"{CHECK_SCRIPTS}/check_delivery.py",
            change_id,
            "--project", str(project_dir),
            "--config", gate_config["config"],
            "--json"
        ]
    else:
        return [TextContent(type="text", text=json.dumps({
            "error": f"Unknown tool: {name}"
        }, ensure_ascii=False))]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return [TextContent(type="text", text=result.stdout)]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
