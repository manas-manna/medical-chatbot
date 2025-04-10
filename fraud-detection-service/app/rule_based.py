from datetime import datetime, timedelta

# A dummy in-memory store to simulate recent user activity
recent_expenses = {}

def check_rules(expense):
    email = expense.user_email
    now = expense.timestamp

    # Save recent transactions
    if email not in recent_expenses:
        recent_expenses[email] = []

    recent_expenses[email].append(now)
    
    # Keep only the last 5 mins data
    recent_expenses[email] = [ts for ts in recent_expenses[email] if ts > now - timedelta(minutes=5)]
    
    # RULE 1: Too many expenses in short time (>=5 in 1 minute)
    count_last_minute = len([ts for ts in recent_expenses[email] if ts > now - timedelta(minutes=1)])
    if count_last_minute >= 5:
        return True, "Too many expenses in short time"

    # RULE 2: Unusually high amount (e.g., > ₹10,000)
    if expense.amount > 10000:
        return True, "Amount exceeds ₹10,000"

    # RULE 3: Suspicious category
    suspicious_categories = ["electronics", "luxury", "other"]
    if expense.category.lower() in suspicious_categories and expense.amount > 5000:
        return True, "Suspicious category with high value"

    return False, None
