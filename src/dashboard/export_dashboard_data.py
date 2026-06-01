import pandas as pd
import joblib

# Load processed data
df = pd.read_csv(
    "data/processed/processed_data.csv"
)

# Load model
model = joblib.load(
    "src/models/model.pkl"
)

# Load features
FEATURES = joblib.load(
    "src/models/features.pkl"
)

# Keep required features
X = df[FEATURES]

# Generate predictions
df["risk_probability"] = model.predict_proba(X)[:, 1]

# Risk categories
def classify_risk(prob):

    if prob < 0.3:
        return "Low"

    elif prob < 0.7:
        return "Medium"

    else:
        return "High"

df["risk_level"] = df["risk_probability"].apply(
    classify_risk
)

# Save for Power BI
df.to_csv(
    "data/processed/dashboard_data.csv",
    index=False
)

print("Dashboard dataset exported.")