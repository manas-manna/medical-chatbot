from pydantic import BaseModel

class ExpenseInput(BaseModel):
    amount: float
    category: str
    hour_of_day: int
    day_of_week: int
