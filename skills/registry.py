"""
Skill Registry for Project Chimera

Central registry for managing all agent skills.
"""
from typing import Dict, Any, Optional

class SkillRegistry:
    """Registry for managing agent skills"""
    
    def __init__(self):
        self._skills: Dict[str, Any] = {}
        self._initialize_default_skills()
    
    def _initialize_default_skills(self):
        """Initialize default skills"""
        # Placeholder - will be populated in Task 3
        pass
    
    def register(self, name: str, skill: Any) -> None:
        """Register a new skill"""
        self._skills[name] = skill
    
    def get_skill(self, name: str) -> Optional[Any]:
        """Get a skill by name"""
        return self._skills.get(name)
    
    def list_skills(self) -> list:
        """List all registered skills"""
        return [
            {
                "name": name,
                "module": skill.__class__.__module__,
                "class": skill.__class__.__name__
            }
            for name, skill in self._skills.items()
        ]
    
    def has_skill(self, name: str) -> bool:
        """Check if skill exists"""
        return name in self._skills

# Global registry instance
_registry_instance: Optional[SkillRegistry] = None

def get_skill_registry() -> SkillRegistry:
    """Get the global skill registry instance"""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = SkillRegistry()
    return _registry_instance

if __name__ == "__main__":
    # Test the registry
    registry = get_skill_registry()
    print(f"Skill Registry initialized: {registry}")
    print(f"Skills available: {registry.list_skills()}")
