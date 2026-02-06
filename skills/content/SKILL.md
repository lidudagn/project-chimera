---
name: "Creative Engine"
capabilities: ["text_generation", "image_synthesis"]
---
# Skill: Content
This skill allows the agent to produce high-fidelity multimodal assets while maintaining **Character Consistency** as defined in `SOUL.md`.

## Tools:
- `generator.py`: Main engine for asset creation.

## Directives:
- Always include the character's unique style LoRA in image prompts.
- Tone must align with the 'Voice' section of the agent's persona.