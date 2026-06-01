import pandas as pd
import joblib
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

# Load data
df = pd.read_csv("data/processed/processed_data.csv")

# SELECT FEATURES FOR APP
FEATURES = [
    "age",
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses"
]

TARGET = "readmitted"

# Keep only selected columns
df = df[FEATURES + [TARGET]]

X = df[FEATURES]
y = df[TARGET]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
)

mlflow.set_experiment("nhs-risk-platform")

with mlflow.start_run():

    model.fit(X_train, y_train)

    preds = model.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(y_test, preds)

    mlflow.log_metric("auc", auc)

    mlflow.sklearn.log_model(
        model,
        artifact_path="model"
    )

    print(f"AUC Score: {auc:.4f}")

# Save model
joblib.dump(model, "src/models/model.pkl")

# Save feature list
joblib.dump(FEATURES, "src/models/features.pkl")

print("Model and features saved successfully.")