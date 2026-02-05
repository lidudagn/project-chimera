"""Performance tests for Planner agent."""

import time
import pytest

def test_planner_decomposition_performance():
    """Test Planner decomposes 1000 tasks in < 5 seconds (SLA from spec)."""
    from agents.planner.task_decomposer import Planner
    
    planner = Planner()
    
    # Large campaign that should generate ~1000 tasks
    campaign_goals = {
        "objective": "Large scale marketing campaign",
        "budget": 100000  # 1000 tasks (100000/100 = 1000)
    }
    
    start_time = time.time()
    tasks = planner.decompose(campaign_goals)
    end_time = time.time()
    
    elapsed = end_time - start_time
    task_count = len(tasks)
    
    print(f"⏱️  Planner Performance:")
    print(f"   Tasks generated: {task_count}")
    print(f"   Time elapsed: {elapsed:.3f} seconds")
    print(f"   SLA: < 5.0 seconds")
    
    # Assertions from spec
    assert task_count == 1000, f"Expected 1000 tasks, got {task_count}"
    assert elapsed < 5.0, f"Planner too slow: {elapsed:.3f}s (SLA: <5s)"
    
    print(f"✅ PASS: Decomposed {task_count} tasks in {elapsed:.3f}s (< 5.0s SLA)")
