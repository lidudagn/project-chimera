# Project Chimera: Functional Specifications
## Version 1.0 | Date: February 5, 2026

## Purpose
Define the functional behavior of Project Chimera agents, workflows, and governance rules, based on the architecture outlined in the `_meta.md` and research report. These specifications serve as the source of truth for implementation and testing.

---

## 1. Agent Types & Responsibilities

### 1.1 Planner (Strategist)
- **Role:** Decompose high-level campaign goals into executable tasks.
- **Responsibilities:**
  - Maintain campaign goals and deadlines.
  - Assign tasks to Worker agents.
  - Re-plan dynamically based on task success/failure.
  - Communicate with Judge agents for validation of high-risk tasks.
- **Inputs:** Campaign specifications, historical performance data.
- **Outputs:** Task plans, task assignments, alerts for Judge review.

### 1.2 Worker (Executor)
- **Role:** Perform atomic tasks assigned by Planner agents.
- **Responsibilities:**
  - Execute tasks without maintaining state.
  - Report results and confidence score to Judge.
  - Store episodic memory in Redis for short-term retrieval.
- **Inputs:** Task specifications from Planner.
- **Outputs:** Task results, confidence metrics, error reports.

### 1.3 Judge (Gatekeeper)
- **Role:** Validate outputs and enforce Human-in-the-Loop (HITL) governance.
- **Responsibilities:**
  - Evaluate confidence scores and escalate tasks requiring review.
  - Maintain audit logs in PostgreSQL.
  - Trigger alerts and queue tasks for human review.
- **Inputs:** Task results from Workers, confidence thresholds, HITL rules.
- **Outputs:** Approved/blocked tasks, HITL review requests, alerts.

---

## 2. Functional Workflows

### 2.1 Task Execution Flow
1. Planner receives campaign goals.
2. Planner decomposes goals into discrete tasks.
3. Planner assigns tasks to Worker agents.
4. Worker executes task and reports result + confidence score.
5. Judge evaluates:
   - Confidence > 0.9 → Auto-approval
   - Confidence 0.7–0.9 → Async human review
   - Confidence < 0.7 → Mandatory human review
6. Results stored in PostgreSQL (audit) and Redis (real-time).

### 2.2 Agent Communication Protocol
- **Identity & Authentication:** DID + cryptographic signature.
- **Message Format:** JSON schema with required fields (`agent_id`, `task_id`, `action`, `timestamp`, `confidence`).
- **Skill Exchange:** Versioned skill packages stored in `skills/` directory, OpenClaw-compatible.
- **Error Reporting:** Standardized error codes with retry policies.

### 2.3 Data Management
- **PostgreSQL:** Transactional data, audit trails, user & agent management.
- **Weaviate:** Semantic memory, skill repository, trend analysis.
- **Redis:** Real-time caching, task queues, ephemeral agent memory.
## 2.4 Error Recovery Flow
1. Worker reports failure with error code
2. Judge analyzes error type:
   - Transient (API timeout) → Retry with exponential backoff
   - Permanent (invalid spec) → Flag for Planner re-planning
   - Security (permission denied) → Immediate HITL escalation
3. Planner receives failure notification and either:
   - Reassigns to different Worker
   - Modifies task parameters
   - Escalates to human operator

---

## 3. Social Protocols
1. **Identity & Authentication**
2. **Structured Communication**
3. **Task & Specification Exchange**
4. **Intent & Version Tracking**
5. **Knowledge Sharing**
6. **Collaboration & Coordination**
7. **Security & Permissions**
8. **Error Handling**
9. **Social Norms Enforcement**

> Immediate Focus: Implement protocols 1–3 for MVP OpenClaw integration.

---

## 4. HITL Governance Rules
- **Auto-Approval Threshold:** Confidence > 0.9
- **Async Review Threshold:** Confidence 0.7–0.9
- **Mandatory Review Threshold:** Confidence < 0.7
- **Sensitive Task Triggers:** Finance > $50, politics, health-related content.
- **Quarterly Persona Alignment:** Human review of agent personas to prevent drift.

---

## 5. Success Criteria
1. Planner can autonomously assign tasks to Worker agents.
2. Worker agents can execute tasks and generate results with confidence scores.
3. Judge agent can validate, escalate, and log tasks as per HITL rules.
4. Agents communicate using OpenClaw-compatible structured messages.
5. Real-time task tracking and semantic retrieval operate correctly across Redis + Weaviate + PostgreSQL.

---

## 6. Notes & Next Steps
- Map functional modules to folder structure: `agents/planner`, `agents/worker`, `agents/judge`.
- Start implementing Task Queue, Communication Protocol, and HITL rules as separate modules.
- Future: Expand social protocols to full 9-rule suite.

---

## 7. Performance Requirements
- **Planner Response:** < 5 seconds for task decomposition
- **Worker Execution:** < 30 seconds for atomic tasks  
- **Judge Validation:** < 3 seconds for confidence evaluation
- **HITL Response:** Human must respond within 15 minutes for mandatory reviews

---

## 8. Validation Test Cases
1. **Confidence Threshold Test:** Verify Judge correctly routes tasks based on 0.7/0.9 thresholds
2. **Protocol Compliance:** Ensure all agent messages include required JSON fields
3. **Database Integrity:** Verify PostgreSQL audit trail matches Redis ephemeral state
4. **HITL Escalation:** Test mandatory review triggers for sensitive topics
