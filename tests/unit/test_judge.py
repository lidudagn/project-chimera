"""Tests for Judge agent from Project Chimera test specification."""

def test_judge_exists():
    """Test Judge class can be imported and instantiated."""
    from agents.judge.evaluator import Judge
    judge = Judge()
    assert judge is not None

def test_judge_evaluates_confidence():
    """Test Judge routes tasks correctly according to confidence thresholds."""
    from agents.judge.evaluator import Judge
    
    judge = Judge()
    
    test_cases = [
        # (confidence, expected_decision)
        (0.5, "escalate"),   # < 0.7 → escalate to HITL
        (0.7, "queue"),      # 0.7–0.9 → queue for async review
        (0.85, "queue"),     # 0.7–0.9 → queue for async review
        (0.91, "approve"),   # > 0.9 → auto-approve
    ]
    
    for confidence, expected in test_cases:
        task_result = {
            "task_id": "test_task",
            "confidence": confidence,
            "output": "Test output"
        }
        
        # This will fail - evaluate() doesn't exist yet
        decision = judge.evaluate(task_result)
        
        assert decision["action"] == expected, \
            f"Confidence {confidence} should be {expected}, got {decision['action']}"
        
        # Decision should include task_id
        assert decision["task_id"] == "test_task"

def test_judge_hitl_trigger():
    """Test Judge escalates sensitive tasks to human review."""
    from agents.judge.evaluator import Judge
    
    judge = Judge()
    
    # Sensitive task: finance > $50
    sensitive_task = {
        "task_id": "finance_task",
        "confidence": 0.95,  # High confidence
        "output": "Transfer $100",
        "task_type": "finance",
        "amount": 100
    }
    
    # This will fail - evaluate() doesn't exist yet
    decision = judge.evaluate(sensitive_task)
    
    # From spec: "Sensitive task (finance > $50) → Judge escalates to human review"
    assert decision["action"] == "escalate", \
        "Finance tasks > $50 should escalate regardless of confidence"
    assert decision["reason"] == "HITL_REQUIRED"
