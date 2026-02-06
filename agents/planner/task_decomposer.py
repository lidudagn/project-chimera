import uuid
import math
from dataclasses import dataclass

@dataclass
class Task:
    task_id: str
    action: str
    budget: float

class TaskDecomposer:  # <--- Ensure this matches exactly
    def __init__(self, cost_per_task=100.0):
        self.cost_per_task = cost_per_task

    def decompose_goal(self, goal: str, total_budget: float):
        num_tasks = math.floor(total_budget / self.cost_per_task)
        assignments = {"worker_alpha": [], "worker_beta": []}
        
        for i in range(num_tasks):
            task = Task(
                task_id=str(uuid.uuid4()),
                action="research" if i % 2 == 0 else "analyze",
                budget=self.cost_per_task
            )
            # Alternate assignments
            worker = "worker_alpha" if i % 2 == 0 else "worker_beta"
            assignments[worker].append(task)
            
        return assignments