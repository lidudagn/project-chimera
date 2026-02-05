import uuid
from datetime import datetime, timedelta

class Planner:
    def __init__(self):
        pass
    
    def decompose(self, goals):
        # MINIMAL implementation - just enough to make test pass
        return [
            {
                "task_id": str(uuid.uuid4()),
                "spec": f"Task for: {goals.get('objective', 'unknown')}",
                "deadline": (datetime.now() + timedelta(days=7)).isoformat(),
                "priority": "medium"
            }
        ]
