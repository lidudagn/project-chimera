def test_hitl_mandatory_review():
    from agents.judge.evaluator import Judge
    judge = Judge()
    
    # Finance > $50 should escalate
    task = {"task_type": "finance", "amount": 100, "confidence": 0.95}
    decision = judge.evaluate(task)
    assert decision["action"] == "escalate"
    print("✓ HITL: Finance > $50 escalated")
