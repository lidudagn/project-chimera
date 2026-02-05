import time

def test_planner_decomposition_performance():
    from agents.planner.task_decomposer import Planner
    
    planner = Planner()
    campaign_goals = {"objective": "Test", "budget": 100000}
    
    start = time.time()
    tasks = planner.decompose(campaign_goals)
    elapsed = time.time() - start
    
    print(f"Planner: {len(tasks)} tasks in {elapsed:.3f}s")
    assert len(tasks) == 1000
    assert elapsed < 5.0
