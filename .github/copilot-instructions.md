# Copilot Instructions – Project Chimera

This repository belongs to **Project Chimera**, an autonomous influencer system built using
spec-driven development, agent orchestration, and MCP-based integrations.

Your role as an AI coding assistant is to support implementation **without bypassing design,
specification, or governance steps**.

This is a long-lived, multi-agent codebase. Treat it accordingly.

---

## Working Model

Project Chimera is designed around:
- Explicit specifications as the source of truth
- Clear separation between agent roles (Planner, Worker, Judge)
- Strict boundaries between internal logic and external systems
- Test-first development

Assume that other AI agents and human engineers will interact with this codebase after you.
Optimise for clarity, traceability, and safety over speed.

---

## Specification First

Before writing or modifying any code, you must:

1. Identify the relevant specification in the `specs/` directory  
2. Confirm that the requested behavior is explicitly defined  
3. If applicable, reference the exact section that authorizes the change  

If the specification is missing, ambiguous, or outdated:
- Do not infer intent
- Propose a specification change instead of writing code

Implementation without an approved spec is considered an error.

---

## How to Respond to Requests

When asked to implement or modify functionality, follow this order:

1. **Confirm scope**
   - What spec governs this?
   - Which component or agent role is affected?

2. **Explain approach**
   - High-level design
   - Relevant agent role (Planner / Worker / Judge)
   - Skills or MCP tools involved

3. **Surface risks**
   - Safety concerns
   - HITL implications
   - Cost, security, or consistency risks

4. **Proceed with implementation only if allowed by spec**

If any step cannot be completed confidently, stop and ask for clarification.

---

## Architectural Constraints

### Agent Roles
- Planner, Worker, and Judge are separate responsibilities
- Workers are stateless and task-focused
- Judges are allowed to reject, retry, or escalate
- Human-in-the-Loop paths must remain intact

Do not collapse roles or shortcut validation logic.

### External Access
- All external systems are accessed through MCP
- Direct API calls from core logic are not permitted
- External behavior must remain swappable without changing agent code

If something interacts with the outside world, it belongs behind MCP.

---

## Skills vs Integrations

**Skills** (in `skills/`) represent internal capabilities:
- Clearly defined inputs and outputs
- No knowledge of API details
- Reusable across agents

**MCP servers** handle external systems:
- APIs, databases, blockchains, platforms
- Volatile by nature
- Treated as replaceable infrastructure

Do not mix these responsibilities.

---

## Testing Expectations

This project uses test-driven development.

- Tests define expected behavior
- Failing tests are acceptable and often intentional
- Do not modify tests to fit an implementation
- Tests must reflect specifications, not assumptions

If behavior changes, update specs first, then tests, then code.

---

## Security & Configuration

- No secrets in code, tests, or logs
- Configuration is environment-driven
- Financial or identity-related operations must be treated as sensitive by default

If an action has security or cost implications, call it out explicitly.

---

## Change Discipline

This repository is designed for parallel development by humans and AI agents.

Therefore:
- Make small, focused changes
- Avoid unrelated refactors
- Do not rename or remove files casually
- Preserve backwards compatibility unless a spec says otherwise

Every change should be easy to understand in isolation.

---

## When in Doubt

Pause.
Check the specs.
Explain your reasoning.
Ask before acting.

That is always preferable to guessing.
