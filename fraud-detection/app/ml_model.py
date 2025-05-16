import joblib
import os

# Load model only once when server starts
model_path = os.path.join(os.path.dirname(__file__), 'models', 'fraud_model.pkl')
model = joblib.load(model_path)
 
CATEGORY_MAP = {
    'Food': 0,
    'Electronics': 1,
    'Travel': 2,
    'Stationary': 3
}

def predict_fraud(data: dict) -> bool:
    amount = data["amount"]
    category = data["category"]
    hour = data["hour_of_day"]
    day = data["day_of_week"]


    # ✅ Rule-based fraud detection
    if amount > 50000:
        return True  # This should immediately return fraud = True

    # If not caught by rule, use ML model
    category_encoded = CATEGORY_MAP.get(category, -1)
    if category_encoded == -1:
        return True
 
    user_id = 1
    location = 0
    device_type = 0
    features = [[amount, hour, day, category_encoded, user_id, location, device_type]]
    prediction = model.predict(features)[0]
    return bool(prediction)
