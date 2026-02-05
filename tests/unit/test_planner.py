from agents.planner.task_decomposer import Planner  

def test_planner_exists():
    """Test we can create a Planner instance"""
    planner = Planner()
    assert planner is not None

def test_planner_decomposes_goals():
    """Test planner generates correct number of tasks with unique IDs"""
    planner = Planner()
    campaign_goals = {"objective": "Test campaign", "budget": 100}
    
    tasks = planner.decompose(campaign_goals)
    
    assert len(tasks) > 0
    for task in tasks:
        assert "task_id" in task
        assert "spec" in task
        assert "deadline" in task  
        assert "priority" in task

def test_planner_assigns_tasks_evenly():
    """Test tasks are evenly distributed among available Workers"""
    planner = Planner()
    campaign_goals = {"objective": "Test campaign", "budget": 500}
    workers = ["worker_1", "worker_2", "worker_3"]
    
    # This will fail - assign_tasks() doesn't exist yet!
    assignments = planner.assign_tasks(campaign_goals, workers)
    
    # From spec: "Tasks are evenly distributed among available Workers"
    # From spec: "No Worker receives duplicate tasks"
    
    # Check all workers received assignments
    for worker in workers:
        assert worker in assignments
        assert isinstance(assignments[worker], list)
    
    # Check tasks are distributed evenly (difference ≤ 1)
    task_counts = [len(tasks) for tasks in assignments.values()]
    max_diff = max(task_counts) - min(task_counts)
    assert max_diff <= 1, f"Tasks not evenly distributed: {task_counts}"
    
    # Check no duplicate tasks across workers
    all_tasks = []
    for task_list in assignments.values():
        all_tasks.extend(task_list)
    
    task_ids = [task["task_id"] for task in all_tasks]
    assert len(set(task_ids)) == len(task_ids), "Duplicate tasks found!"

def test_tasks_have_valid_structure():
    """Test task objects contain valid specs, deadlines, and priority"""
    planner = Planner()
    campaign_goals = {"objective": "Marketing campaign", "budget": 1000}
    
    tasks = planner.decompose(campaign_goals)
    
    # Test we have tasks
    assert len(tasks) > 0, "No tasks generated"
    
    for task in tasks:
        # Required fields from spec
        required_fields = ["task_id", "spec", "deadline", "priority"]
        for field in required_fields:
            assert field in task, f"Task missing required field: {field}"
        
        # Field validation
        assert isinstance(task["spec"], str) and len(task["spec"]) > 0, \
            "Task spec must be non-empty string"
        
        # Priority validation
        valid_priorities = ["low", "medium", "high", "critical"]
        assert task["priority"] in valid_priorities, \
            f"Priority '{task['priority']}' not in {valid_priorities}"
        
        # Deadline should be valid ISO format
        from datetime import datetime
        try:
            deadline = datetime.fromisoformat(task["deadline"].replace('Z', '+00:00'))
            assert deadline > datetime.now(), "Deadline should be in future"
        except ValueError:
            pytest.fail(f"Invalid deadline format: {task['deadline']}")

def test_planner_generates_correct_task_count():
    """Test planner generates appropriate number of tasks based on budget"""
    planner = Planner()
    
    test_cases = [
        ({"budget": 50}, 1),    # $50 → 1 task (minimum)
        ({"budget": 250}, 2),   # $250 → 2 tasks (250/100 = 2.5 → floor = 2)
        ({"budget": 500}, 5),   # $500 → 5 tasks
        ({"budget": 1200}, 12), # $1200 → 12 tasks
    ]
    
    for goals, expected_count in test_cases:
        tasks = planner.decompose(goals)
        assert len(tasks) == expected_count, \
            f"Budget {goals['budget']} should generate {expected_count} tasks, got {len(tasks)}"
