"""Full integration test: Planner → Worker → Judge."""

def test_planner_worker_judge_flow():
    """Test end-to-end flow matching spec section 4.1."""
    from agents.planner.task_decomposer import Planner
    from agents.worker.executor import Worker
    from agents.judge.evaluator import Judge
    
    # Setup all agents
    planner = Planner()
    worker = Worker()
    judge = Judge()
    
    # 1. Planner creates tasks
    campaign_goals = {
        "objective": "Social media marketing campaign",
        "budget": 500  # Should generate 5 tasks (500/100 = 5)
    }
    workers_list = ["worker_alpha", "worker_beta"]
    
    assignments = planner.assign_tasks(campaign_goals, workers_list)
    
    # 2. Worker executes tasks
    task_results = []
    for worker_name, tasks in assignments.items():
        for task in tasks:
            result = worker.execute(task)
            result["task_id"] = task["task_id"]  # Preserve task_id
            task_results.append(result)
    
    # 3. Judge evaluates results
    decisions = []
    for result in task_results:
        decision = judge.evaluate(result)
        decisions.append(decision)
    
    # Verification
    expected_tasks = 5  # $500 budget / $100 per task
    assert len(task_results) == expected_tasks, \
        f"Expected {expected_tasks} tasks from ${campaign_goals['budget']} budget, got {len(task_results)}"
    
    assert len(decisions) == expected_tasks, \
        f"Expected {expected_tasks} decisions, got {len(decisions)}"
    
    # Analyze decision distribution
    approved = [d for d in decisions if d["action"] == "approve"]
    queued = [d for d in decisions if d["action"] == "queue"]
    escalated = [d for d in decisions if d["action"] == "escalate"]
    
    print(f"✓ Integration test results:")
    print(f"  Tasks executed: {len(task_results)}")
    print(f"  Approved: {len(approved)}")
    print(f"  Queued for review: {len(queued)}")
    print(f"  Escalated to HITL: {len(escalated)}")
    
    # With Worker confidence of 0.8, all should be queued (0.7-0.9 range)
    assert len(queued) == expected_tasks, \
        f"All tasks with 0.8 confidence should be queued, but got: {len(approved)} approved, {len(queued)} queued, {len(escalated)} escalated"
