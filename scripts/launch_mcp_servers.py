#!/usr/bin/env python3
"""
Launch MCP servers for Project Chimera development environment.

This script starts all MCP servers needed for development:
1. git-mcp-server: Git operations
2. filesystem-mcp-server: Secure file operations
3. test-runner-mcp-server: Test execution (mock)
4. docker-mcp-server: Container operations (mock)

Usage:
    python scripts/launch_mcp_servers.py
    OR
    ./scripts/launch_mcp_servers.py
"""

import asyncio
import sys
import os
from pathlib import Path
import subprocess
import signal
import time

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

async def launch_mcp_server(script_path: Path, server_name: str):
    """
    Launch an MCP server as a subprocess.
    
    Args:
        script_path: Path to the MCP server Python script
        server_name: Human-readable name for logging
    
    Returns:
        (process, task) tuple
    """
    print(f"🚀 Starting {server_name} from {script_path.name}...")
    
    try:
        # Launch the MCP server
        process = await asyncio.create_subprocess_exec(
            sys.executable, 
            str(script_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=PROJECT_ROOT
        )
        
        # Create a task to monitor the process output
        async def monitor_output(proc, name):
            """Monitor and log server output"""
            try:
                while True:
                    line = await proc.stdout.readline()
                    if not line:
                        break
                    print(f"[{name}] {line.decode().strip()}")
                    
                # Check for errors after process ends
                stderr_data = await proc.stderr.read()
                if stderr_data:
                    print(f"[{name}-ERROR] {stderr_data.decode().strip()}")
            except Exception as e:
                print(f"[{name}-MONITOR] Error: {e}")
        
        monitor_task = asyncio.create_task(monitor_output(process, server_name))
        
        # Wait a bit to see if server starts successfully
        await asyncio.sleep(1)
        
        # Check if process is still running
        if process.returncode is not None:
            print(f"❌ {server_name} failed to start (exit code: {process.returncode})")
            return None, None
        else:
            print(f"✅ {server_name} started successfully (PID: {process.pid})")
            return process, monitor_task
            
    except FileNotFoundError:
        print(f"❌ Script not found: {script_path}")
        return None, None
    except Exception as e:
        print(f"❌ Failed to start {server_name}: {e}")
        return None, None

async def launch_all_servers():
    """
    Launch all MCP servers concurrently.
    """
    print("=" * 60)
    print("🚀 Project Chimera - MCP Server Launcher")
    print("=" * 60)
    
    # Define servers to launch
    servers_to_launch = []
    
    # Check which servers exist
    possible_servers = [
        {
            "script": PROJECT_ROOT / "mcp_servers" / "development" / "git_server.py",
            "name": "Git MCP Server"
        },
        {
            "script": PROJECT_ROOT / "mcp_servers" / "development" / "filesystem_server.py", 
            "name": "Filesystem MCP Server"
        },
        {
            "script": PROJECT_ROOT / "mcp_servers" / "development" / "test_runner_server.py",
            "name": "Test Runner MCP Server"
        },
        {
            "script": PROJECT_ROOT / "mcp_servers" / "development" / "docker_server.py",
            "name": "Docker MCP Server"
        }
    ]
    
    for server_info in possible_servers:
        if server_info["script"].exists():
            servers_to_launch.append(server_info)
            print(f"✅ Found: {server_info['name']}")
        else:
            print(f"⚠️  Missing: {server_info['name']}")
    
    if not servers_to_launch:
        print("❌ No MCP servers found to launch")
        print("\n📝 Create server scripts in mcp_servers/development/")
        return
    
    print(f"\n📋 Found {len(servers_to_launch)} MCP server(s) to launch")
    
    print("\n" + "=" * 60)
    
    # Launch all servers
    processes = []
    tasks = []
    
    for server_info in servers_to_launch:
        process, monitor_task = await launch_mcp_server(server_info["script"], server_info["name"])
        if process and monitor_task:
            processes.append((process, server_info["name"]))
            tasks.append(monitor_task)
    
    if not processes:
        print("❌ No MCP servers started successfully")
        return
    
    print("\n" + "=" * 60)
    print("✅ All MCP servers started!")
    print("\n📡 Servers are now running and listening for connections.")
    print("📝 They communicate via stdio transport with your IDE/agent.")
    print("\n🛑 Press Ctrl+C to stop all servers.")
    print("=" * 60)
    
    # Set up signal handling
    stop_event = asyncio.Event()
    
    def signal_handler():
        print("\n\n🛑 Received shutdown signal...")
        stop_event.set()
    
    # Add signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        # Keep servers running until stop event
        await stop_event.wait()
        
    except asyncio.CancelledError:
        print("\n⚠️  Task cancelled")
    finally:
        print("\n🔄 Stopping all MCP servers...")
        
        # Terminate all processes
        for process, name in processes:
            if process.returncode is None:  # Still running
                print(f"  Stopping {name}...")
                try:
                    process.terminate()
                    await process.wait()
                    print(f"  ✅ {name} stopped")
                except Exception as e:
                    print(f"  ❌ Error stopping {name}: {e}")
        
        # Cancel monitor tasks
        for task in tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)
        
        print("\n✅ All MCP servers stopped successfully.")
        print("=" * 60)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required = ["mcp"]
    missing = []
    
    for package in required:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install mcp")
        return False
    
    print("✅ All dependencies available")
    return True

def create_missing_servers():
    """Create template MCP servers if they don't exist"""
    server_templates = {
        "test_runner_server.py": '''"""
Test Runner MCP Server - Execute and monitor tests
"""
from typing import Any
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

server = Server("test-runner-mcp-server")

@server.list_tools()
async def handle_list_tools() -> list[dict[str, Any]]:
    """List available test tools"""
    return [
        {
            "name": "run_pytest",
            "description": "Run pytest tests",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "test_path": {
                        "type": "string",
                        "description": "Path to test file or directory"
                    }
                }
            }
        }
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
    """Handle tool execution"""
    if name == "run_pytest":
        return [{
            "type": "text",
            "text": "Test runner server is running in mock mode"
        }]
    
    return [{"type": "text", "text": f"Unknown tool: {name}"}]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="test-runner-mcp-server",
                server_version="0.1.0"
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
''',
        "docker_server.py": '''"""
Docker MCP Server - Container management
"""
from typing import Any
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

server = Server("docker-mcp-server")

@server.list_tools()
async def handle_list_tools() -> list[dict[str, Any]]:
    """List available docker tools"""
    return [
        {
            "name": "docker_info",
            "description": "Get Docker system information",
            "inputSchema": {"type": "object", "properties": {}}
        }
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
    """Handle tool execution"""
    if name == "docker_info":
        return [{
            "type": "text", 
            "text": "Docker server is running in mock mode\\nRun 'docker --version' to verify Docker installation"
        }]
    
    return [{"type": "text", "text": f"Unknown tool: {name}"}]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="docker-mcp-server",
                server_version="0.1.0"
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
'''
    }
    
    created = []
    for filename, content in server_templates.items():
        filepath = PROJECT_ROOT / "mcp_servers" / "development" / filename
        if not filepath.exists():
            filepath.parent.mkdir(exist_ok=True, parents=True)
            filepath.write_text(content)
            created.append(filename)
            print(f"  📝 Created: {filename}")
    
    if created:
        print(f"\n📁 Created {len(created)} template MCP server(s)")
        print("📋 Note: Some servers are running in mock mode.")
        print("   Implement full functionality as needed.")
    return len(created)

async def main():
    """Main entry point"""
    print("🔧 Project Chimera MCP Server Launcher")
    print("Version: 1.0.0")
    print()
    
    # Check if we're in the project root
    if not (PROJECT_ROOT / "pyproject.toml").exists():
        print("❌ Error: Must run from project root directory")
        print(f"   Current directory: {Path.cwd()}")
        print(f"   Expected to find: pyproject.toml in {PROJECT_ROOT}")
        return 1
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Create missing template servers
    created = create_missing_servers()
    
    print()
    
    try:
        await launch_all_servers()
        return 0
    except KeyboardInterrupt:
        print("\n\n👋 Exiting by user request")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    # Make script executable
    if sys.platform != "win32" and not Path(__file__).stat().st_mode & 0o111:
        os.chmod(__file__, 0o755)
        print(f"🔧 Made script executable: {__file__}")
    
    # Run the launcher
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
