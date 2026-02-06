---
name: "Social Engagement Engine"
capabilities: ["reply_generation", "sentiment_filtering"]
---
# Skill: Engagement
This skill handles all direct interactions with the audience.

## Guardrails:
- **Safety First**: Never respond to hate speech or high-conflict political debates.
- **Tone Consistency**: All replies must match the Gen-Z/Witty persona defined in `SOUL.md`.
- **Throttling**: Maximum 50 replies per hour to avoid platform bans.

## Primary Tools:
- `replier.py`: Analyzes incoming mentions and generates context-aware responses.