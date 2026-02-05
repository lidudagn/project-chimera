"""Test Worker retry logic for transient errors."""

import random

def test_worker_handles_transient_errors():
    """Test Worker automatically retries on transient errors."""
    from agents.worker.executor import Worker
    
    # Monkey-patch to control error simulation
    original_simulate = Worker._simulate_transient_error
    
    # Make it fail 100% of times for first 2 attempts
    call_count = 0
    def always_fail_first_two(self):
        nonlocal call_count
        call_count += 1
        return call_count <= 2  # Fail first two, succeed on third
    
    Worker._simulate_transient_error = always_fail_first_two
    
    try:
        worker = Worker(max_retries=3)
        
        task = {
            "task_id": "retry_test",
            "spec": "Test retry logic",
            "action": "test"
        }
        
        result = worker.execute(task)
        
        # Should succeed after retries
        assert result["success"] == True
        assert "attempts" in result
        print(f"✓ Worker succeeded after retries")
        
    finally:
        # Restore original method
        Worker._simulate_transient_error = original_simulate

def test_worker_fails_after_max_retries():
    """Test Worker fails when max retries exceeded."""
    from agents.worker.executor import Worker
    
    # Make it always fail
    def always_fail(self):
        return True
    
    original = Worker._simulate_transient_error
    Worker._simulate_transient_error = always_fail
    
    try:
        worker = Worker(max_retries=2)
        
        task = {
            "task_id": "max_retry_test",
            "spec": "Test max retries",
            "action": "test"
        }
        
        result = worker.execute(task)
        
        # Should fail after max retries
        assert result["success"] == False
        assert result["error_code"] == "API_ERROR"
        print(f"✓ Worker correctly failed after max retries")
        
    finally:
        Worker._simulate_transient_error = original
