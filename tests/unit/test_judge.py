def test_judge_exists():
    from agents.judge.evaluator import Judge
    judge = Judge()
    assert judge is not None

def test_judge_evaluates_confidence():
    """Test Judge routes tasks correctly according to thresholds (<0.7, 0.7–0.9, >0.9)."""
    from agents.judge.evaluator import Judge
    
    judge = Judge()
    
    test_cases = [
        (0.5, "escalate"),   # < 0.7 → escalate
        (0.69, "escalate"),  # < 0.7 → escalate
        (0.7, "queue"),      # 0.7–0.9 → queue for review
        (0.85, "queue"),     # 0.7–0.9 → queue for review
        (0.9, "queue"),      # 0.7–0.9 → queue for review
        (0.91, "approve"),   # > 0.9 → auto-approve
        (0.95, "approve"),   # > 0.9 → auto-approve
    ]
    
    for confidence, expected_action in test_cases:
        task_result = {
            "task_id": f"task_{confidence}",
            "confidence": confidence,
            "output": "Test output"
        }
        
        # This will fail - evaluate() doesn't exist yet
        decision = judge.evaluate(task_result)
        
        assert decision["action"] == expected_action, \
            f"Confidence {confidence} should be {expected_action}, got {decision['action']}"

def test_judge_hitl_trigger():
    """Test Judge escalates sensitive tasks (finance > $50) to human review."""
    from agents.judge.evaluator import Judge
    
    judge = Judge()
    
    # Sensitive finance task > $50
    sensitive_task = {
        "task_id": "finance_transfer",
        "confidence": 0.95,  # High confidence
        "output": "Transfer $100 to vendor",
        "task_type": "finance",
        "amount": 100
    }
    
    # This will fail - evaluate() doesn't exist yet
    decision = judge.evaluate(sensitive_task)
    
    # From spec: "Task status = 'pending HITL'"
    assert decision["action"] == "escalate", \
        "Finance tasks > $50 should escalate to HITL"
    assert "HITL" in decision.get("reason", "").upper()
