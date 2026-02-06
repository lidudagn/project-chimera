import uuid
from datetime import datetime, timedelta

class Planner:
    def __init__(self):
        pass

    def decompose(self, goals, budget=0):
        """Breaks goals into a list of executable task dictionaries."""
        task_list = []
        
        # Determine the raw goals
        if isinstance(goals, dict):
            actual_goals = [goals.get('objective', 'unknown')]
            if budget == 0:
                budget = goals.get('budget', 0)
        elif isinstance(goals, str):
            actual_goals = [goals]
        else:
            actual_goals = goals

        # Calculate how many tasks to generate
        # Logic: At least one task per goal, plus budget scaling ($100 per task)
        num_tasks = max(len(actual_goals), int(budget // 100))
        
        for i in range(num_tasks):
            goal_text = actual_goals[i % len(actual_goals)]
            task_list.append(self._create_task(goal_text, i))
            
        return task_list

    def _create_task(self, goal, index):
        """Creates the specific schema the Worker and Integration tests require."""
        return {
            "task_id": str(uuid.uuid4()),
            "action": "research",
            "spec": f"Task for: {goal}",
            "priority": "high" if index == 0 else "medium",
            "deadline": (datetime.now() + timedelta(days=7)).isoformat()
        }

    def assign_tasks(self, goals, workers):
        """
        Returns a Dictionary {worker_id: [list_of_tasks]}
        Crucial: The value MUST be a list to satisfy the tests.
        """
        assignments = {worker_id: [] for worker_id in workers}
        tasks = self.decompose(goals)
        
        for i, task in enumerate(tasks):
            # Distribute tasks to workers in a round-robin fashion
            worker_id = workers[i % len(workers)]
            assignments[worker_id].append(task)
            
        return assignments