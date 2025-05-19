import numpy as np
import pandas as pd
import json
from keras.models import load_model
import joblib
from typing import List, Dict

class DiseasePredictor:
    def __init__(self):
        try:
            self.model = load_model("ml_models/disease/disease_model.h5")
            self.disease_encoder = joblib.load("ml_models/disease/disease_encoder.pkl")
            # self.symptom_mappings = pd.read_csv("ml_models/disease/symptom_mappings.csv").drop(columns='diseases').apply(pd.to_numeric, errors='coerce').fillna(0).astype('float32')
            with open("ml_models/disease/symptom_columns.json", "r") as f:
                self.symptom_columns = pd.Index(json.load(f))
        except Exception as e:
            raise RuntimeError(f"Failed to load disease prediction models: {str(e)}")

    def predict(self, symptoms: List[str], top_n: int = 3) -> List[Dict[str, float]]:
        if not symptoms:
            raise ValueError("At least one symptom must be provided")

        # input_vector = np.zeros(len(self.symptom_mappings.columns), dtype='float32')
        input_vector = np.zeros(len(self.symptom_columns), dtype='float32')
        found_symptoms = []

        for symptom in symptoms:
            norm_symptom = symptom.lower().strip()
            if norm_symptom in self.symptom_columns:
                idx = self.symptom_columns.get_loc(norm_symptom)
                input_vector[idx] = 1.0
                found_symptoms.append(norm_symptom)

        if not found_symptoms:
            return [{"disease": "No matching symptoms found", "probability": 0.0}]

        proba = self.model.predict(input_vector.reshape(1, -1), verbose=0)[0]
        top_indices = np.argsort(proba)[-top_n:][::-1]

        return [
            {"disease": self.disease_encoder.inverse_transform([idx])[0], "probability": float(proba[idx])}
            for idx in top_indices
        ]
