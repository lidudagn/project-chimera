# OpenClaw Integration Specification

## 1. Status Publishing (Heartbeat)

Chimera agents SHALL publish a heartbeat to the OpenClaw relay every 5 minutes
to maintain active network status.

- **Endpoint**: `POST /relay/v1/heartbeat`

### Payload Schema
```json
{
  "agent_id": "chimera-01",
  "status": "active",
  "capabilities": [
    "trend_analysis",
    "on_chain_payment"
  ],
  "load_metric": 0.45,
  "last_action": "trend_analysis"
}
