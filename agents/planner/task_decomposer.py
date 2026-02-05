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

    def assign_tasks(self, goals, workers):
        """Distribute tasks evenly among workers."""
        # First decompose goals into tasks
        tasks = self.decompose(goals)

        # Initialize assignments dictionary
        assignments = {worker: [] for worker in workers}

        # Simple round-robin distribution
        for i, task in enumerate(tasks):
            worker_idx = i % len(workers)
            worker = workers[worker_idx]
            assignments[worker].append(task)

        return assignments
