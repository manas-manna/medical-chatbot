from fastapi import FastAPI
from app.model import ExpenseInput
from app.ml_model import predict_fraud

app = FastAPI()

@app.post("/predict-fraud")
def predict(expense: ExpenseInput):
    print("[DEBUG] Incoming data:", expense.dict())
    return {"fraud": predict_fraud(expense.dict())}
