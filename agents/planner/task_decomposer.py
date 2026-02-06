import uuid
import math
from dataclasses import dataclass

@dataclass
class Task:
    task_id: str
    spec: str  # Renamed from 'action' to match the test requirements
    budget: float
    priority: str = "medium"
    deadline: str = "2026-12-31T00:00:00Z"

class Planner:
    def __init__(self, cost_per_task=100.0):
        self.cost_per_task = cost_per_task

    def decompose(self, goals: dict):
        """Standard method for Task 1.2 and Unit Tests"""
        total_budget = goals.get("budget", 0)
        num_tasks = max(1, math.floor(total_budget / self.cost_per_task))
        
        tasks = []
        for i in range(num_tasks):
            tasks.append({
                "task_id": str(uuid.uuid4()),
                "spec": f"Execute {goals.get('objective', 'task')} - Part {i+1}",
                "budget": self.cost_per_task,
                "priority": "medium",
                "deadline": "2026-12-31T00:00:00Z"
            })
        return tasks

    def assign_tasks(self, goals: dict, workers: list):
        """The specific method the Integration Test is looking for"""
        tasks = self.decompose(goals)
        assignments = {worker: [] for worker in workers}
        
        for i, task in enumerate(tasks):
            worker = workers[i % len(workers)]
            assignments[worker].append(task)
            
        return assignments