import pandas as pd
import joblib

model = joblib.load(
    "src/models/model.pkl"
)

features = joblib.load(
    "src/models/features.pkl"
)

importance = model.feature_importances_

importance_df = pd.DataFrame({
    "feature": features,
    "importance": importance
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

importance_df.to_csv(
    "data/processed/feature_importance.csv",
    index=False
)

print("Feature importance exported.")