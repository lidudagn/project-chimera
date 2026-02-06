"""
Skill Registry for Project Chimera
Central registry for managing all agent skills and providing a 
standardized interface for the Orchestrator.
"""
import logging
from typing import Dict, Any, Optional, List

# Setup logging for the registry
logger = logging.getLogger(__name__)

class SkillRegistry:
    """Registry for managing agent skills using a Singleton pattern."""
    
    def __init__(self):
        self._skills: Dict[str, Any] = {}
        self._initialize_default_skills()
    
    def _initialize_default_skills(self):
        """
        Dynamically imports and registers the core skills.
        This follows the 'Skill Capsule' architecture.
        """
        try:
            # Import standardized interfaces from sub-packages
            from skills.trends import fetch_trends
            from skills.commerce import execute_transaction
            from skills.content import ContentGenerator
            from skills.engagement import EngagementManager

            # Register functions or instantiated classes
            self.register("trends", fetch_trends)
            self.register("commerce", execute_transaction)
            self.register("content", ContentGenerator())
            self.register("engagement", EngagementManager())
            
            logger.info(f"Successfully registered {len(self._skills)} core skills.")
            
        except ImportError as e:
            logger.error(f"Failed to initialize core skills: {e}")
            # Non-blocking: Registry can still be used for manual registration
    
    def register(self, name: str, skill: Any) -> None:
        """Register a new skill into the inventory."""
        self._skills[name] = skill
        logger.debug(f"Skill '{name}' registered.")
    
    def get_skill(self, name: str) -> Optional[Any]:
        """Retrieve a skill by its unique name."""
        return self._skills.get(name)
    
    def list_skills(self) -> List[Dict[str, str]]:
        """List metadata for all registered skills for AI discovery."""
        return [
            {
                "name": name,
                "type": type(skill).__name__,
                "module": getattr(skill, "__module__", "unknown")
            }
            for name, skill in self._skills.items()
        ]
    
    def has_skill(self, name: str) -> bool:
        """Check if a specific skill is available in the registry."""
        return name in self._skills

# Global registry instance (Singleton)
_registry_instance: Optional[SkillRegistry] = None

def get_skill_registry() -> SkillRegistry:
    """
    Get the global skill registry instance. 
    Ensures all agents share the same tool definitions.
    """
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = SkillRegistry()
    return _registry_instance

if __name__ == "__main__":
    # Internal validation test
    registry = get_skill_registry()
    available = registry.list_skills()
    print(f"--- Chimera Skill Registry Audit ---")
    print(f"Total Skills: {len(available)}")
    for skill in available:
        print(f"  - {skill['name']} ({skill['type']})")