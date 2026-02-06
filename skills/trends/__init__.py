"""
Trends Skill Package for Project Chimera
Exposes tools for market perception and social trend analysis.
"""

# Import the actual logic from your script
from .trend_fetcher import fetch_trends 

__all__ = ["fetch_trends"]
__version__ = "0.1.0"