"""
Filesystem MCP Server for Project Chimera
"""
import asyncio
from pathlib import Path
from typing import Any

try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP not available. Running in mock mode.")

if MCP_AVAILABLE:
    server = Server("filesystem-mcp-server")
    
    @server.list_tools()
    async def handle_list_tools() -> list[dict[str, Any]]:
        return [
            {
                "name": "list_files",
                "description": "List files in directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path",
                            "default": "."
                        }
                    }
                }
            }
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
        if name == "list_files":
            path = Path(arguments.get("path", "."))
            try:
                if not path.exists():
                    return [{"type": "text", "text": f"Error: Path {path} does not exist."}]
                files = [str(f.name) for f in path.iterdir()]
                return [{"type": "text", "text": "\n".join(files)}]
            except Exception as e:
                return [{"type": "text", "text": f"Error: {str(e)}"}]
        return [{"type": "text", "text": f"Unknown tool: {name}"}]

    async def main():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="filesystem-mcp-server",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities()
                )
            )

if __name__ == "__main__":
    if MCP_AVAILABLE:
        asyncio.run(main())
    else:
        print("Cannot start server: MCP library missing.")
