# Project Chimera: Technical Specifications

**Version:** 1.0  
**Date:** February 5, 2026

## 1. Purpose

Translate functional specifications into implementation-ready technical details: folder structure, modules, APIs, databases, task queues, and dependencies.  
Serves as the blueprint for developers and automation agents.

## 2. Folder & Module Structure

project-chimera/
├── agents/
│   ├── planner/
│   │   ├── init.py
│   │   ├── task_decomposer.py
│   │   └── scheduler.py
│   ├── worker/
│   │   ├── init.py
│   │   ├── executor.py
│   │   └── task_reporter.py
│   └── judge/
│       ├── init.py
│       ├── validator.py
│       └── hitl_handler.py
├── skills/
│   ├── skill1.json
│   └── skill2.json
├── specs/
│   ├── _meta.md
│   ├── functional.md
│   ├── technical.md
│   └── test.md
├── research/
│   ├── architecture_strategy.md
│   └── research_summary.md
├── scripts/
│   ├── run_agent.py
│   └── deploy.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── performance/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci_cd.yml
├── .vscode/
│   └── mcp.json
└── README.m

## 3. Programming Stack

- **Language:** Python 3.11+
- **Frameworks / Libraries:**
  - FastAPI – For agent APIs and microservices
  - asyncio – Concurrency in Planner/Worker pools
  - pydantic – Data validation for task specifications
  - pytest – Unit & integration testing
  - docker – Containerization
  - redis-py – Redis cache management
  - sqlalchemy – PostgreSQL ORM
  - weaviate-client – Vector database interaction
- **Task Queue:** Celery with Redis backend

## 4. Database Schemas

### 4.1 PostgreSQL (Transactional)

**Tables:**

- `agents`: id, type, credentials, status, last_seen
- `tasks`: id, planner_id, worker_id, spec_id, status, confidence, created_at, updated_at
- `audit_logs`: task_id, action, agent_id, timestamp, review_status
- `transactions`: id, type, amount, currency, status, timestamp

### 4.2 Weaviate (Vector / Semantic)

**Classes:**

- `AgentMemory` – Stores embeddings of past interactions
- `Skills` – Embeddings of skill modules for semantic search
- `ContentTrend` – Temporal vector representations of content trends

### 4.3 Redis (Cache / Task Queue)

**Keys:**

- `task_queue:<planner_id>` – Pending tasks
- `ephemeral_memory:<agent_id>` – Last hour interactions
- `rate_limit:<agent_id>` – API usage tracking

## 5. APIs & Interfaces

### 5.1 Planner → Worker

- **Endpoint:** `/assign_task`
- **Method:** POST
- **Payload:** `{ task_id, spec, priority, deadline }`
- **Response:** `{ status, assigned_worker_id }`

### 5.2 Worker → Judge

- **Endpoint:** `/report_result`
- **Method:** POST
- **Payload:** `{ task_id, result, confidence, error_code }`
- **Response:** `{ status, hitl_required }`

### 5.3 Judge → Planner / HITL Dashboard

- **Endpoint:** `/evaluate_task`
- **Method:** POST
- **Payload:** `{ task_id, confidence, error_code }`
- **Response:** `{ approved, escalation, notes }`

### 5.4 MCP Server

Standardized agent interface for all external platform interactions (Twitter, Coinbase, OpenClaw, etc.)

## 6. Task Queue & Workflow

1. Planner receives campaign goals → decomposes into tasks → pushes to Celery queue
2. Worker consumes tasks asynchronously → executes → stores ephemeral data in Redis → reports to Judge
3. Judge evaluates confidence → triggers HITL if needed → logs approved tasks in PostgreSQL → updates Redis for real-time dashboards

## 7. Error Handling & Recovery

- Transient Errors: Retry with exponential backoff
- Permanent Errors: Notify Planner → reassign task or modify spec
- Security Violations: Immediate HITL escalation
- Queue Failures: Fallback to Redis backup queue

## 8. Performance & SLA

| Module       | Expected Performance            |
|--------------|---------------------------------|
| Planner      | Task decomposition < 5 sec      |
| Worker       | Atomic task < 30 sec            |
| Judge        | Confidence evaluation < 3 sec   |
| HITL         | Human response < 15 min         |
| Redis Ops    | < 1 ms / operation              |
| PostgreSQL   | 50k TPS read/write              |

## 9. Deployment

- Containers: Docker for agents, databases, MCP servers
- Orchestration: Docker Compose / Kubernetes for scaling Worker swarms
- CI/CD: GitHub Actions for linting, testing, and deployment
- Logging: Centralized via ELK Stack or Prometheus

## 10. Next Steps

1. Start module implementation: Planner, Worker, Judge
2. Connect task queue, Redis cache, and PostgreSQL
3. Implement MCP server interface
4. Run initial unit tests
5. Deploy minimal agents in local Docker environment