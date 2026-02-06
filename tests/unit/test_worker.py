from models.database import init_db, Task
import uuid

class Planner:
    def __init__(self):
        self.db_session = init_db()

    def decompose(self, goals):
        """Breaks high-level goals into executable tasks."""
        tasks = []
        for i, goal in enumerate(goals):
            # The test specifically looks for this method
            task = self._create_task(goal, i)
            tasks.append(task)
        return tasks

    def _create_task(self, goal, index):
        """Helper to format task structure for the Worker."""
        return {
            "task_id": str(uuid.uuid4()),
            "type": "research" if "find" in goal.lower() else "execution",
            "description": goal,
            "priority": "high" if index == 0 else "medium"
        }

    def assign_tasks(self, goals, workers):
        """Assigns goals to specific worker IDs."""
        assignments = {}
        tasks = self.decompose(goals)
        for i, task in enumerate(tasks):
            worker_id = workers[i % len(workers)]
            assignments[worker_id] = task
        return assignments