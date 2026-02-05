"""Performance tests for Planner agent."""

def test_planner_decomposition_performance():
    """Test Planner can decompose 1000 tasks in parallel in < 5 seconds."""
    from agents.planner.task_decomposer import Planner
    import time
    
    planner = Planner()
    
    # Large campaign
    campaign_goals = {
        "objective": "Large scale campaign",
        "budget": 100000  # Should generate 1000 tasks
    }
    
    start_time = time.time()
    tasks = planner.decompose(campaign_goals)
    end_time = time.time()
    
    elapsed = end_time - start_time
    task_count = len(tasks)
    
    print(f"Planner decomposed {task_count} tasks in {elapsed:.2f} seconds")
    
    # From spec: < 5 seconds for 1000 tasks
    assert elapsed < 5.0, f"Planner too slow: {elapsed:.2f}s for {task_count} tasks (SLA: <5s)"
    assert task_count == 1000, f"Expected 1000 tasks, got {task_count}"
