class Worker:
    """Executor-style Worker for tests.

    Provides a minimal constructor and a `process_tasks` helper used elsewhere.
    """

    def __init__(self, name: str = "worker"):
        self.name = name

    def process_tasks(self, tasks):
        if not tasks:
            return []
        return [{"task_id": t.get("task_id"), "status": "completed"} for t in tasks]
