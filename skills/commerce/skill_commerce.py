# Implementing FR 5.2
MAX_DAILY_LIMIT = 50.0  # USDC

async def cfo_judge_check(amount: float, current_daily_spend: float):
    if (current_daily_spend + amount) > MAX_DAILY_LIMIT:
        return "REJECTED: Budget Exceeded"
    return "APPROVED"