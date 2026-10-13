from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

# Load trained model and feature names
model = joblib.load(MODEL_DIR / "teratogenicity_descriptor_rf.joblib")
feature_columns = joblib.load(MODEL_DIR / "descriptor_columns.joblib")

# Initialize FastAPI
app = FastAPI(
    title="AI-Based QSAR Teratogenicity Prediction API",
    description=(
        "Predicts historical pregnancy-risk categories "
        "from molecular descriptors."
    ),
    version="1.0.0",
)

# CORS configuration for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DrugInput(BaseModel):
    a_acc: float = Field(
        ge=0, description="Number of hydrogen-bond acceptors"
    )
    a_don: float = Field(
        ge=0, description="Number of hydrogen-bond donors"
    )
    b_rotN: float = Field(
        ge=0, description="Number of rotatable bonds"
    )
    SlogP: float = Field(
        description="Molecular lipophilicity descriptor"
    )
    Weight: float = Field(
        gt=0, description="Molecular weight"
    )


@app.get("/")
def home():
    return {"message": "QSAR Prediction API is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "features": feature_columns,
    }


@app.post("/predict")
def predict_drug(data: DrugInput):
    input_data = data.model_dump()
    input_df = pd.DataFrame([input_data])[feature_columns]

    prediction = model.predict(input_df)[0]

    probabilities = {}

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_df)[0]
        probabilities = {
            str(label): round(float(prob), 4)
            for label, prob in zip(model.classes_, probs)
        }

    return {
        "predicted_risk_category": str(prediction),
        "class_probabilities": probabilities,
        "note": (
            "This is a model prediction based on historical pregnancy-risk "
            "categories, not a clinically validated assessment of fetal harm "
            "or drug safety."
        ),
    }
