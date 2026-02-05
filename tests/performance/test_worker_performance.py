"""Performance tests for Worker agent."""

import time
import concurrent.futures

def test_worker_concurrent_execution():
    """Test Worker executes 500 tasks concurrently in < 30 seconds (SLA from spec)."""
    from agents.worker.executor import Worker
    
    worker = Worker()
    
    # Create 500 test tasks
    test_tasks = []
    for i in range(500):
        task = {
            "task_id": f"perf_task_{i}",
            "spec": f"Performance test task {i}",
            "action": "test_action"
        }
        test_tasks.append(task)
    
    # Execute concurrently
    start_time = time.time()
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_task = {
            executor.submit(worker.execute, task): task 
            for task in test_tasks
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_task):
            results.append(future.result())
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"⏱️  Worker Performance:")
    print(f"   Tasks executed: {len(results)}")
    print(f"   Time elapsed: {elapsed:.3f} seconds")
    print(f"   SLA: < 30.0 seconds")
    print(f"   Throughput: {len(results)/elapsed:.1f} tasks/second")
    
    # Assertions from spec
    assert len(results) == 500, f"Expected 500 results, got {len(results)}"
    assert elapsed < 30.0, f"Worker too slow: {elapsed:.3f}s (SLA: <30s)"
    
    # Verify all tasks succeeded
    success_count = sum(1 for r in results if r.get("success") == True)
    assert success_count == 500, f"Expected 500 successful executions, got {success_count}"
    
    print(f"✅ PASS: Executed {len(results)} tasks in {elapsed:.3f}s (< 30.0s SLA)")
