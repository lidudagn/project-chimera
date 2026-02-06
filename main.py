# main.py update
import uuid
from models.database import init_db, Task, Campaign

def run_swarm():
    print("🚀 Project Chimera: Swarm Initialized")
    db_session = init_db()

    # 1. Create a Campaign in the DB
    new_campaign = Campaign(
        id=str(uuid.uuid4()),
        objective="Market research for eco-friendly sneakers",
        budget=300.0,
        status="active"
    )
    db_session.add(new_campaign)
    
    # 2. Let the Planner do its thing
    from agents.planner.task_decomposer import TaskDecomposer
    planner = TaskDecomposer()
    assignments = planner.decompose_goal(new_campaign.objective, new_campaign.budget)

    # 3. Save Assignments to Postgres
    for worker_id, task_list in assignments.items():
        print(f"🤖 {worker_id} assigned {len(task_list)} tasks.")
        for t in task_list:
            db_task = Task(
                id=t.task_id,
                campaign_id=new_campaign.id,
                assigned_to=worker_id,
                action=t.action,
                status="pending"
            )
            db_session.add(db_task)
    
    db_session.commit()
    print("✅ Tasks persisted to PostgreSQL.")

if __name__ == "__main__":
    run_swarm()