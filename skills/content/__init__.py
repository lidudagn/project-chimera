"""
Content Skill Package for Project Chimera
Exposes tools for multimodal content generation (Text, Image, Video).
"""

# This assumes your logic file is named generator.py
# and it contains a function or class to handle creative tasks.
from .generator import ContentGenerator 

__all__ = ["ContentGenerator"]
__version__ = "0.1.0"