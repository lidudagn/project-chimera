import uuid
from datetime import datetime, timedelta

class Planner:
    def __init__(self):
        pass
    
    def decompose(self, goals):
        # Determine number of tasks from budget: one task per $100, minimum 1
        budget = goals.get("budget", 0) or 0
        try:
            budget = int(budget)
        except (TypeError, ValueError):
            budget = 0

        task_count = max(1, budget // 100)

        # Choose a simple priority mapping based on budget
        if budget >= 1000:
            priority = "critical"
        elif budget >= 500:
            priority = "high"
        elif budget >= 250:
            priority = "medium"
        else:
            priority = "low"

        tasks = []
        for _ in range(task_count):
            tasks.append(
                {
                    "task_id": str(uuid.uuid4()),
                    "spec": f"Task for: {goals.get('objective', 'unknown')}",
                    "deadline": (datetime.now() + timedelta(days=7)).isoformat(),
                    "priority": priority,
                }
            )

        return tasks

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
