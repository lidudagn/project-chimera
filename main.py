import os
from agents.planner.task_decomposer import Planner
# Assuming you have similar imports for Worker and Judge
# from agents.worker.executor import Worker
# from agents.judge.evaluator import Judge
from models.database import init_db

def run_swarm():
    print("🚀 Project Chimera: Swarm Initialized")
    
    # 1. Initialize DB and Agents
    db_session = init_db()
    planner = Planner()
    
    # 2. Define a Goal
    campaign_goal = {
        "objective": "Market research for eco-friendly sneakers",
        "budget": 300
    }
    
    print(f"📋 Goal received: {campaign_goal['objective']}")
    
    # 3. Planner Decomposes Goal
    workers = ["worker_alpha", "worker_beta"]
    assignments = planner.assign_tasks(campaign_goal, workers)
    
    for worker, tasks in assignments.items():
        print(f"🤖 {worker} assigned {len(tasks)} tasks.")
        for task in tasks:
            print(f"   - Task ID: {task['task_id'][:8]} | Action: {task['action']}")

    print("\n✅ Swarm execution dry-run complete.")

if __name__ == "__main__":
    run_swarm()