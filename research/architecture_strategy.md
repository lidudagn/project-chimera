# Project Chimera Architecture Strategy

## Agent Pattern
- Hierarchical FastRender Swarm (Planner → Worker → Judge)
- Planner decomposes tasks
- Worker executes atomic tasks
- Judge validates and escalates to HITL if needed

## Human-in-the-Loop
- Auto-approval (>0.9 confidence)
- Async review (0.7–0.9 confidence)
- Mandatory review (<0.7 confidence)

## Database Strategy
- Hybrid SQL + NoSQL + Vector
- PostgreSQL: transactional video metadata
- Weaviate: vector search, content memory
- Redis: high-velocity ephemeral storage
