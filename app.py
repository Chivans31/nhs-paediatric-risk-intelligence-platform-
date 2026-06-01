# STREAMLIT WITH AUTHENTICATION

import shap
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import streamlit as st
import requests

import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

st.title("NHS Healthcare AI Platform")

st.sidebar.title("Authentication")

username = st.sidebar.text_input("Username")

if st.sidebar.button("Generate Token"):

    response = requests.post(
        f"{API_URL}/login",
        params={"username": username}
    )

    token = response.json()["access_token"]

    st.session_state["token"] = token

    st.sidebar.success("Token generated")

age = st.slider("Age", 1, 100, 50)

time_in_hospital = st.slider(
    "Time in Hospital",
    1,
    14,
    5
)

num_lab_procedures = st.slider(
    "Lab Procedures",
    1,
    100,
    40
)

num_procedures = st.slider(
    "Procedures",
    0,
    10,
    1
)

num_medications = st.slider(
    "Medications",
    1,
    50,
    10
)

number_outpatient = st.slider(
    "Outpatient Visits",
    0,
    20,
    0
)

number_emergency = st.slider(
    "Emergency Visits",
    0,
    20,
    0
)

number_inpatient = st.slider(
    "Inpatient Visits",
    0,
    20,
    0
)

number_diagnoses = st.slider(
    "Diagnoses",
    1,
    20,
    5
)

if st.button("Predict"):

    payload = {
        "age": age,
        "time_in_hospital": time_in_hospital,
        "num_lab_procedures": num_lab_procedures,
        "num_procedures": num_procedures,
        "num_medications": num_medications,
        "number_outpatient": number_outpatient,
        "number_emergency": number_emergency,
        "number_inpatient": number_inpatient,
        "number_diagnoses": number_diagnoses
    }

    headers = {
        "Authorization": f"Bearer {st.session_state['token']}"
    }

    response = requests.post(
        f"{API_URL}/predict",
        json=payload,
        headers=headers
    )

    result = response.json()

    st.metric(
        "Risk Probability",
        f"{result['risk_probability']:.2%}"
    )

    st.write(
        f"### Risk Level: {result['risk_level']}"
    )

    st.subheader("Model Explanation")
    
    model = joblib.load("src/models/model.pkl")
    FEATURES = joblib.load("src/models/features.pkl")
    
    sample_df = pd.DataFrame([payload])
    sample_df = sample_df[FEATURES]
    
    explainer = shap.Explainer(model)
    shap_values = explainer(sample_df)
    
    fig = plt.figure(figsize=(12, 6))
    
    shap.plots.waterfall(
        shap_values[0],
        show=False
    )
    
    st.pyplot(fig)
