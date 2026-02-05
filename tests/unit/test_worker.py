"""Tests for Worker agent from Project Chimera test specification."""

def test_worker_exists():
    """Test Worker class can be imported and instantiated."""
    from agents.worker.executor import Worker
    worker = Worker()
    assert worker is not None

def test_worker_executes_task():
    """Test Worker executes task correctly and produces a confidence score."""
    from agents.worker.executor import Worker
    
    worker = Worker()
    task_spec = {
        "task_id": "test_task_1",
        "spec": "Create social media post about Project Chimera",
        "action": "create_post",
        "platform": "twitter"
    }
    
    # This will fail - execute() doesn't exist yet
    result = worker.execute(task_spec)
    
    # From spec: "Worker executes task correctly"
    assert "success" in result
    assert "output" in result
    
    # From spec: "Produces a confidence score between 0.0–1.0"
    assert "confidence" in result
    confidence = result["confidence"]
    assert 0.0 <= confidence <= 1.0, f"Confidence {confidence} not in range 0.0-1.0"

def test_worker_error_reporting():
    """Test Worker returns correct error code for failures."""
    from agents.worker.executor import Worker
    
    worker = Worker()
    
    # Test with invalid task spec
    invalid_task = {"invalid": "spec"}
    
    # This will fail - execute() needed
    result = worker.execute(invalid_task)
    
    # From spec: "Correct error code is returned"
    assert "error" in result
    assert "error_code" in result
    assert "message" in result
    
    # Error codes should be standardized
    valid_error_codes = ["INVALID_SPEC", "API_ERROR", "NETWORK_ERROR", "TIMEOUT"]
    assert result["error_code"] in valid_error_codes
