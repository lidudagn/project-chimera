from agents.planner.task_decomposer import Planner  

def test_planner_exists():
    """Test we can create a Planner instance"""
    planner = Planner()
    assert planner is not None
