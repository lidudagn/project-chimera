# MCP Tooling Strategy for Project Chimera

## Development MCP Servers

### Core Development Servers:
1. **git-mcp-server** (Stdio)
   - Purpose: Enable AI agents to perform version control operations
   - Tools: `git_commit`, `git_status`, `git_branch`, `git_diff`
   - Security: Read-only by default, write operations require explicit confirmation

2. **filesystem-mcp-server** (Stdio)
   - Purpose: File operations within project boundaries
   - Tools: `read_file`, `write_file`, `list_directory`
   - Security: Restricted to project directory only

3. **docker-mcp-server** (Custom - Stdio)
   - Purpose: Container management for testing and deployment
   - Tools: `build_image`, `run_container`, `stop_container`
   - Security: Limited to development environment

4. **test-runner-mcp-server** (Custom - Stdio)
   - Purpose: Execute and monitor test suites
   - Tools: `run_pytest`, `get_coverage`, `list_tests`
   - Security: Sandboxed execution

### Runtime MCP Servers (For Agent Swarm):
1. **social-mcp-server** - Social media integrations
2. **weaviate-mcp-server** - Vector database operations
3. **coinbase-mcp-server** - Agentic commerce
4. **news-mcp-server** - Trend monitoring

## Implementation Strategy

### Transport Configuration:
- **Development:** Stdio transport for local tooling servers
- **Production:** SSE transport for distributed runtime servers
- **Security:** Each server runs in isolated container with minimal permissions

### Directory Structure: