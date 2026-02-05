import time
import random

class Worker:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries
    
    def execute(self, task_spec):
        """Execute a task with retry logic for transient errors."""
        # Validate task spec
        if not self._is_valid_task_spec(task_spec):
            return self._error_response("INVALID_SPEC", "Missing required fields")
        
        # Execute with retry logic
        for attempt in range(self.max_retries + 1):
            try:
                result = self._execute_single(task_spec)
                
                # Simulate transient errors randomly
                if self._simulate_transient_error():
                    if attempt < self.max_retries:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        return self._error_response("API_ERROR", "Max retries exceeded")
                
                return result
                
            except Exception as e:
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    return self._error_response("EXECUTION_ERROR", str(e))
    
    def _execute_single(self, task_spec):
        """Execute a single task attempt."""
        # Simulate work
        time.sleep(0.01)  # Small delay
        
        # Determine confidence based on task complexity
        complexity = len(str(task_spec)) % 10 / 10.0
        confidence = 0.7 + (random.random() * 0.25)  # 0.7-0.95
        
        return {
            "success": True,
            "output": f"Executed: {task_spec['spec']}",
            "confidence": confidence,
            "attempts": 1
        }
    
    def _simulate_transient_error(self):
        """Simulate transient errors 10% of the time."""
        return random.random() < 0.1
    
    def _is_valid_task_spec(self, task_spec):
        """Validate task specification has required fields."""
        required = ["task_id", "spec", "action"]
        return all(field in task_spec for field in required)
    
    def _error_response(self, error_code, message):
        """Create standardized error response."""
        return {
            "success": False,
            "error": message,
            "error_code": error_code,
            "confidence": 0.0
        }
