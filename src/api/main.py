# ADVANCED FASTAPI BACKEND

from fastapi import FastAPI, Depends
from fastapi.security import HTTPAuthorizationCredentials
import pandas as pd
import joblib
from pathlib import Path

from src.api.auth import (
    security,
    verify_token,
    create_token
)

from src.api.schemas import PatientData

from src.utils.logger import logger

app = FastAPI(
    title="NHS Healthcare AI Platform",
    version="1.0"
)


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "src/models/model.pkl"

model = joblib.load(MODEL_PATH)
FEATURES = joblib.load("src/models/features.pkl")


@app.get("/")
def home():

    return {
        "message": "NHS Healthcare AI Platform Running"
    }


@app.post("/login")
def login(username: str):

    token = create_token(username)

    return {
        "access_token": token
    }


@app.post("/predict")
def predict(
    data: PatientData,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    verify_token(credentials.credentials)

    df = pd.DataFrame([data.dict()])

    df = df[FEATURES]

    prediction = model.predict_proba(df)[0][1]

    if prediction < 0.3:
        risk_level = "Low"

    elif prediction < 0.7:
        risk_level = "Medium"

    else:
        risk_level = "High"

    logger.info(f"Prediction generated: {prediction}")

    return {
        "risk_probability": round(float(prediction), 4),
        "risk_level": risk_level
    }
