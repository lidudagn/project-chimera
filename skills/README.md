# Project Chimera: Skill Registry
This directory defines the "hands" of the agents. No agent may perform an external action without using a registered skill.

## Design Pattern: The Skill Contract
Every skill must implement:
1. `manifest.json`: Defines the input/output schema for AI discovery.
2. `logic.py`: The executable code.
3. `test_skill.py`: Individual skill validation.

## Current Skills
| Skill | Status | Description |
| :--- | :--- | :--- |
| `trend_fetcher` | Draft | Fetches data via MCP Google Search/Twitter servers. |
| `commerce_engine` | Draft | Manages transactions via Coinbase AgentKit. |
| `content_generator` | Draft | Bridges to Stable Diffusion / GPT-4o media tools. |
