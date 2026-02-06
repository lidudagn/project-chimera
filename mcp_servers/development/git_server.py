"""
Git MCP Server for Project Chimera
"""
import subprocess
from typing import Any
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

server = Server("git-mcp-server")

@server.list_tools()
async def handle_list_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": "git_status",
            "description": "Get git status",
            "inputSchema": {"type": "object", "properties": {}}
        },
        {
            "name": "git_commit",
            "description": "Commit changes",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Commit message"}
                },
                "required": ["message"]
            }
        }
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
    if name == "git_status":
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        output = result.stdout or result.stderr or "Working directory clean"
        return [{"type": "text", "text": f"Git Status:\n{output}"}]
    elif name == "git_commit":
        message = arguments.get("message", "")
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )
        output = result.stdout or result.stderr or "Commit completed"
        return [{"type": "text", "text": f"Commit Result:\n{output}"}]
    return [{"type": "text", "text": f"Unknown tool: {name}"}]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="git-mcp-server",
                server_version="1.0.0"
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
