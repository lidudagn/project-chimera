"""
Engagement Skill Package for Project Chimera
Exposes tools for audience interaction, reply generation, and sentiment analysis.
"""

# This assumes your logic file is named 'replier.py' or 'engagement_manager.py'
from .replier import EngagementManager

__all__ = ["EngagementManager"]
__version__ = "0.1.0"