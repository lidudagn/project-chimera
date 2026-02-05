"""Tests for Judge agent from Project Chimera test specification."""

def test_judge_exists():
    """Test Judge class can be imported and instantiated."""
    from agents.judge.evaluator import Judge
    judge = Judge()
    assert judge is not None
