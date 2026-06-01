# SHAP EXPLAINABILITY DASHBOARD

import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt

model = joblib.load("src/models/model.pkl")


FEATURES = joblib.load("src/models/features.pkl")


df = pd.read_csv(
    "data/processed/processed_data.csv"
)

X = df[FEATURES]

explainer = shap.Explainer(model)

shap_values = explainer(X[:100])

plt.figure(figsize=(12, 8))

shap.plots.beeswarm(
    shap_values,
    show=False
)

plt.savefig(
    "src/dashboard/shap_summary.png",
    dpi=300,
    bbox_inches="tight"
)

print("SHAP dashboard created.")