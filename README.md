# 🧬 Project Chimera: The Agentic Infrastructure
> **Mission**: Architecting the "Factory" for the Autonomous AI Influencer.

Project Chimera is an engineering-first repository designed to support a swarm of AI agents capable of trend research, content generation, and autonomous engagement. Built on the **Planner-Worker-Judge** pattern, this repo serves as the "Governor" to ensure the AI Influencer operates within specified guardrails and security protocols.



---

## 🏗️ Architectural Strategy (Task 1.2)
Chimera follows a **Hierarchical Swarm Pattern**. 
- **The Brain**: Guided by `.cursor/rules` and `specs/`, ensuring zero "hallucination" by making Specifications the absolute source of truth.
- **The Social Protocol**: Aligned with the **OpenClaw** network for inter-agent communication and availability broadcasting.
- **Safety Layer**: A Human-in-the-Loop (HITL) trigger is integrated into the "Judge" logic for high-stakes content and financial transactions.

---

## 🛠️ The "Golden" Tooling (Task 2.3)

| Category | Implementation | Role |
| :--- | :--- | :--- |
| **Developer Tools (MCP)** | `git-mcp`, `filesystem-mcp` | Assists the FDE in rapid, governed development. |
| **Agent Skills (Runtime)** | `commerce`, `trends`, `content` | Isolated Python capsules with strict I/O contracts. |
| **Memory & State** | PostgreSQL & SQLAlchemy | High-velocity metadata storage for video/engagement. |
| **Traceability** | Tenx MCP Sense | The "Black Box" flight recorder for all agent thinking. |

---

## 🚦 Governance & Reliability (Task 3)

This repository functions as a **Spec-Driven Development (SDD)** environment. Implementation code does not exist until the **Governor** verifies the failing tests.

### 1. True TDD Framework (Task 3.1)
We define the "goal posts" for the AI Swarm through failing tests:
* `make test`: Executes the test suite within a **Dockerized** environment to ensure "it works on every machine."
* **Status**: 20/23 Passing (3 Intentional TDD Failures in Skill Interfaces to guide future Agent work).

### 2. Automated CI/CD Pipeline (Task 3.3)
Our `.github/workflows/main.yml` enforces:
* **Linting**: Black and Flake8 for style consistency.
* **Security**: Bandit scans for cryptographic vulnerabilities (CWE-330).
* **AI Review**: Simulated via CodeRabbit config to verify Spec Alignment.



---

## 📂 Project Mapping (The FDE Blueprint)

| Directory | Task | Purpose |
| :--- | :--- | :--- |
| `specs/` | **2.1** | Functional/Technical blueprints and OpenClaw integration plans. |
| `agents/` | **2.2** | `SOUL.md` defining the Influencer's persona and guardrails. |
| `research/` | **1.2/2.3** | Domain strategy for the Agent Social Network and Tooling. |
| `skills/` | **2.3B** | The "Hands" of the agent—reusable runtime capabilities. |
| `tests/` | **3.1** | The TDD "Empty Slots" defining the AI's implementation goals. |

---

## 🚀 The FDE Command Center
- **Setup Environment**: `make setup`
- **Run Governor Audit**: `make lint`
- **Verify TDD Progress**: `make test`
- **Spec Consistency Check**: `make spec-check`

---
*Forward Deployed Engineering Submission - February 6, 2026*