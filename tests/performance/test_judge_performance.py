"""Performance tests for Judge agent."""

import time
import concurrent.futures

def test_judge_concurrent_evaluation():
    """Test Judge evaluates 500 task results concurrently in < 3 seconds (SLA from spec)."""
    from agents.judge.evaluator import Judge
    
    judge = Judge()
    
    # Create 500 test task results with varying confidence
    test_results = []
    for i in range(500):
        result = {
            "task_id": f"judge_perf_{i}",
            "confidence": 0.5 + (i % 50) * 0.01,  # Vary confidence from 0.5 to 0.99
            "output": f"Test output {i}",
            "task_type": "regular"
        }
        test_results.append(result)
    
    # Add some HITL triggers
    for i in range(50, 60):  # 10 finance tasks > $50
        test_results[i]["task_type"] = "finance"
        test_results[i]["amount"] = 100
    
    # Evaluate concurrently
    start_time = time.time()
    
    decisions = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Submit all evaluations
        future_to_result = {
            executor.submit(judge.evaluate, result): result 
            for result in test_results
        }
        
        # Collect decisions as they complete
        for future in concurrent.futures.as_completed(future_to_result):
            decisions.append(future.result())
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"⏱️  Judge Performance:")
    print(f"   Results evaluated: {len(decisions)}")
    print(f"   Time elapsed: {elapsed:.3f} seconds")
    print(f"   SLA: < 3.0 seconds")
    print(f"   Throughput: {len(decisions)/elapsed:.1f} evaluations/second")
    
    # Analyze decisions
    approved = sum(1 for d in decisions if d["action"] == "approve")
    queued = sum(1 for d in decisions if d["action"] == "queue")
    escalated = sum(1 for d in decisions if d["action"] == "escalate")
    
    print(f"   Decisions: {approved} approved, {queued} queued, {escalated} escalated")
    
    # Assertions from spec
    assert len(decisions) == 500, f"Expected 500 decisions, got {len(decisions)}"
    assert elapsed < 3.0, f"Judge too slow: {elapsed:.3f}s (SLA: <3s)"
    
    print(f"✅ PASS: Evaluated {len(decisions)} results in {elapsed:.3f}s (< 3.0s SLA)")
