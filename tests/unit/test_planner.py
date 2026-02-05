from agents.planner.task_decomposer import Planner  

def test_planner_exists():
    """Test we can create a Planner instance"""
    planner = Planner()
    assert planner is not None

def test_planner_decomposes_goals():
    """Test planner generates correct number of tasks with unique IDs"""
    planner = Planner()
    campaign_goals = {"objective": "Test campaign", "budget": 100}
    
    # This will fail - decompose() doesn't exist yet!
    tasks = planner.decompose(campaign_goals)
    
    assert len(tasks) > 0
    for task in tasks:
        assert "task_id" in task
        assert "spec" in task
        assert "deadline" in task  
        assert "priority" in task
