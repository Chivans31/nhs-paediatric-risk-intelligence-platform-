import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):

    df = df.replace("?", pd.NA)

    categorical_cols = df.select_dtypes(include="object").columns

    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown")

    return df

def encode_features(df):

    encoders = {}

    categorical_cols = df.select_dtypes(include="object").columns

    for col in categorical_cols:

        le = LabelEncoder()

        df[col] = le.fit_transform(df[col].astype(str))

        encoders[col] = le

    return df, encoders

def prepare_target(df):

    df["readmitted"] = df["readmitted"].apply(
        lambda x: 1 if x == "<30" else 0
    )

    return df

if __name__ == "__main__":

    df = load_data("data/raw/diabetic_data.csv")

    df = clean_data(df)

    df = prepare_target(df)

    df, encoders = encode_features(df)

    df.to_csv("data/processed/processed_data.csv", index=False)

    print("Data pipeline completed.")