def test_planner_worker_judge_flow():
    from agents.planner.task_decomposer import Planner
    from agents.worker.executor import Worker
    from agents.judge.evaluator import Judge
    
    planner = Planner()
    worker = Worker()
    judge = Judge()
    
    campaign_goals = {"objective": "Test", "budget": 200}
    workers = ["w1", "w2"]
    
    assignments = planner.assign_tasks(campaign_goals, workers)
    
    results = []
    for tasks in assignments.values():
        for task in tasks:
            result = worker.execute(task)
            result["task_id"] = task["task_id"]
            results.append(result)
    
    decisions = []
    for result in results:
        decisions.append(judge.evaluate(result))
    
    assert len(results) == 2
    assert len(decisions) == 2
    print("✓ Integration test passed")
