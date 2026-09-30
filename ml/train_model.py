from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


DATA_PATH = Path("data/sample_transactions.csv")
MODEL_PATH = Path("ml/model.pkl")
METRICS_PATH = Path("ml/metrics.json")


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

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )
    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )
    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )
    roc_auc = roc_auc_score(
        y_test,
        probabilities,
    )

    metrics = {
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1_score": round(float(f1), 4),
        "roc_auc": round(float(roc_auc), 4),
        "training_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "feature_count": len(FEATURE_COLUMNS),
        "model_type": "RandomForestClassifier",
        "model_version": "1.0.0",
    }

    print("Model training completed.")
    print()
    print("Model Metrics:")
    print(json.dumps(metrics, indent=2))
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

    with open(
        METRICS_PATH,
        "w",
        encoding="utf-8",
    ) as metrics_file:
        json.dump(
            metrics,
            metrics_file,
            indent=2,
        )

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Metrics saved to: {METRICS_PATH}")


if __name__ == "__main__":
    train_model()
