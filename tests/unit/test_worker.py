"""Tests for Worker agent from Project Chimera test specification."""

def test_worker_exists():
    """Test Worker class can be imported and instantiated."""
    from agents.worker.executor import Worker
    worker = Worker()
    assert worker is not None
