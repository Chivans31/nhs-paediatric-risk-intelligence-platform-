# DATA DRIFT MONITORING

import pandas as pd

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

reference_data = pd.read_csv(
    "data/processed/processed_data.csv"
)

current_data = reference_data.sample(
    1000,
    random_state=42
)

report = Report(
    metrics=[DataDriftPreset()]
)

report.run(
    reference_data=reference_data,
    current_data=current_data
)

report.save_html(
     "drift_report.html"
)

print("Drift report generated.")