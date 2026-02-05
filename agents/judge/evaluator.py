class Judge:
    def __init__(self):
        pass
    
    def evaluate(self, task_result):
        """Evaluate task result and make routing decision."""
        confidence = task_result.get("confidence", 0.0)
        task_id = task_result.get("task_id", "unknown")
        
        # Check for HITL triggers first
        if self._requires_hitl(task_result):
            return {
                "task_id": task_id,
                "action": "escalate",
                "reason": "HITL_REQUIRED",
                "details": "Sensitive task requiring human review"
            }
        
        # Route based on confidence
        if confidence < 0.7:
            action = "escalate"
            reason = "LOW_CONFIDENCE"
        elif confidence <= 0.9:
            action = "queue"
            reason = "REVIEW_REQUIRED"
        else:  # confidence > 0.9
            action = "approve"
            reason = "HIGH_CONFIDENCE"
        
        return {
            "task_id": task_id,
            "action": action,
            "reason": reason,
            "confidence": confidence
        }
    
    def _requires_hitl(self, task_result):
        """Check if task requires Human-in-the-Loop review."""
        # Finance > $50
        if task_result.get("task_type") == "finance":
            amount = task_result.get("amount", 0)
            if amount > 50:
                return True
        
        # Other sensitive categories
        sensitive_types = ["politics", "health", "legal"]
        if task_result.get("task_type") in sensitive_types:
            return True
        
        return False
