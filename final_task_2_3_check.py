#!/usr/bin/env python3
"""
Final check for Task 2.3 completion
"""
import os
import sys
from pathlib import Path

print("🎯 TASK 2.3 FINAL STATUS")
print("=" * 60)

# List all checks
checks = []

# 1. Virtual environment
venv = os.environ.get('VIRTUAL_ENV')
checks.append(("Virtual Environment", venv is not None))
print(f"{'✅' if venv else '❌'} Virtual Environment: {'Active' if venv else 'Not active'}")

# 2. MCP installation
try:
    import mcp
    checks.append(("MCP Library", True))
    print("✅ MCP Library: Installed")
except ImportError:
    checks.append(("MCP Library", False))
    print("❌ MCP Library: Not installed")

# 3. MCP servers
mcp_dir = Path("mcp_servers/development")
if mcp_dir.exists():
    servers = list(mcp_dir.glob("*.py"))
    has_servers = len(servers) >= 2
    checks.append(("MCP Servers", has_servers))
    print(f"{'✅' if has_servers else '❌'} MCP Servers: {len(servers)} files")
    for s in servers:
        print(f"    • {s.name} ({s.stat().st_size} bytes)")
else:
    checks.append(("MCP Servers", False))
    print("❌ MCP Servers: Directory missing")

# 4. Launcher script
launcher = Path("scripts/launch_mcp_servers.py")
checks.append(("Launcher Script", launcher.exists()))
if launcher.exists():
    print(f"✅ Launcher: {launcher} ({launcher.stat().st_size} bytes)")
else:
    print("❌ Launcher: Missing")

# 5. Skills structure
skills_dir = Path("skills")
if skills_dir.exists():
    subdirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    has_skills = len(subdirs) >= 4
    checks.append(("Skills Structure", has_skills))
    print(f"{'✅' if has_skills else '❌'} Skills: {len(subdirs)} packages")
    for d in subdirs:
        print(f"    • {d.name}/")
else:
    checks.append(("Skills Structure", False))
    print("❌ Skills: Directory missing")

print("\n" + "=" * 60)
print("📊 TASK 2.3 COMPLETION SUMMARY")

passed = sum(1 for _, status in checks if status)
total = len(checks)

print(f"✅ {passed}/{total} requirements met")

if passed == total:
    print("\n🎉 TASK 2.3 COMPLETED SUCCESSFULLY!")
    print("\n📋 Ready for Task 3.1: Test-Driven Development")
    print("   Create failing tests in tests/ directory")
else:
    print(f"\n⚠️  {total - passed} requirement(s) missing")

print("=" * 60)

# Test MCP servers can run
if passed >= 3:  # At least basic setup
    print("\n🔧 Testing MCP server functionality...")
    try:
        import subprocess
        import time
        
        # Test git server briefly
        proc = subprocess.Popen(
            ["python", "mcp_servers/development/git_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(0.5)
        if proc.poll() is None:
            print("✅ Git server: Can start")
            proc.terminate()
            proc.wait()
        else:
            stdout, stderr = proc.communicate()
            print(f"⚠️  Git server: {stderr[:100]}")
        
        # Test filesystem server briefly
        proc = subprocess.Popen(
            ["python", "mcp_servers/development/filesystem_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(0.5)
        if proc.poll() is None:
            print("✅ Filesystem server: Can start")
            proc.terminate()
            proc.wait()
        else:
            stdout, stderr = proc.communicate()
            print(f"⚠️  Filesystem server: {stderr[:100]}")
    except Exception as e:
        print(f"⚠️  Server test error: {e}")

print("=" * 60)
