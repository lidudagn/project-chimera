class Worker:
    def __init__(self):
        pass
    
    def execute(self, task_spec):
        """Execute a task and return result with confidence score."""
        # Validate task spec has required fields
        if not self._is_valid_task_spec(task_spec):
            return {
                "success": False,
                "error": "Invalid task specification",
                "error_code": "INVALID_SPEC",
                "message": "Missing required fields: task_id, spec, action",
                "confidence": 0.0
            }
        
        # Successful execution (simulated for now)
        return {
            "success": True,
            "output": f"Executed: {task_spec['spec']}",
            "confidence": 0.8
        }
    
    def _is_valid_task_spec(self, task_spec):
        """Validate task specification has required fields."""
        required = ["task_id", "spec", "action"]
        return all(field in task_spec for field in required)
