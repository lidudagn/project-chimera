---
name: "Trend Perception Engine"
capabilities: ["social_media_polling", "trend_clustering", "sentiment_analysis"]
version: "1.0.0"
---
# Skill: Trends

## Description
This skill enables the Chimera Agent to "sense" the digital world. It interfaces with external MCP servers (Twitter, Google News, etc.) to identify what is currently viral or relevant to the agent's niche.

## Primary Tools
- `trend_fetcher.py`: The core logic for polling external MCP Resources and returning structured trend data.

## Usage Guidelines
- **Frequency**: Should be invoked by the Planner every 4-6 hours to maintain context.
- **Filtering**: Data must be passed through a relevance filter before being committed to the GlobalState.

## Input/Output Contract
- **Input**: None (or optional `category` string).
- **Output**: A list of dictionaries containing `topic`, `relevance_score`, and `source_url`.