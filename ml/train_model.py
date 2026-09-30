from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split


DATA_PATH = Path("data/sample_transactions.csv")
MODEL_PATH = Path("ml/model.pkl")


FEATURE_COLUMNS = [
    "amount",
    "transaction_hour",
    "account_age_days",
    "previous_transactions_24h",
    "failed_attempts_24h",
    "foreign_transaction",
    "new_device",
]


def load_data():
    dataframe = pd.read_csv(DATA_PATH)

    X = dataframe[FEATURE_COLUMNS]
    y = dataframe["is_fraud"]

    return X, y


def train_model():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    auc_score = roc_auc_score(
        y_test,
        probabilities,
    )

    print("Model training completed.")
    print(f"ROC-AUC: {auc_score:.4f}")
    print()
    print(
        classification_report(
            y_test,
            predictions,
        )
    )

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print(
        f"Model saved to: {MODEL_PATH}"
    )


if __name__ == "__main__":
    train_model()
