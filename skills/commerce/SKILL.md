---
name: "Commerce Toolset"
capabilities: ["wallet_management", "transaction_execution"]
---
# Commerce Skill
This folder contains the logic for interacting with the **Coinbase AgentKit**.

## Primary Tools:
- `wallet_management.py`: Handles creation and loading of non-custodial wallets.
- `skill_commerce.py`: Main entry point for financial transactions.

## Guardrails:
- No transaction should exceed 100 USD without Human-in-the-Loop approval.