import uuid
from datetime import datetime, timedelta
from models.database import init_db, Task

class Planner:
    def __init__(self, agent_id="planner_01"):
        self.agent_id = agent_id
        self.db_session = init_db()
    
    def decompose(self, goals):
        budget = goals.get("budget", 0)
        task_count = max(1, budget // 100)
        
        tasks = []
        for i in range(task_count):
            task = self._create_task(goals, i, budget)
            
            # Log to database
            db_task = Task(
                task_id=task["task_id"],
                agent_id=self.agent_id,
                action="create",
                status="pending",
                spec=task,
                created_at=datetime.utcnow()
            )
            self.db_session.add(db_task)
            
            tasks.append(task)
        
        self.db_session.commit()
        return tasks
    
    # ... rest of existing code ...
