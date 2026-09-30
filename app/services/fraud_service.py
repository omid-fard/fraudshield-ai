from pathlib import Path

import joblib
import pandas as pd

from app.schemas.transaction import TransactionRequest


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


_model = None


def load_model():
    global _model

    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Fraud detection model not found. "
                "Run `python data/generate_data.py` and "
                "`python ml/train_model.py` first."
            )

        _model = joblib.load(MODEL_PATH)

    return _model


def calculate_risk_score(transaction: TransactionRequest) -> int:
    score = 0

    if transaction.amount >= 5000:
        score += 25
    elif transaction.amount >= 2000:
        score += 15
    elif transaction.amount >= 1000:
        score += 8

    if transaction.transaction_hour <= 5:
        score += 12

    if transaction.account_age_days < 30:
        score += 15
    elif transaction.account_age_days < 90:
        score += 8

    if transaction.previous_transactions_24h >= 20:
        score += 15
    elif transaction.previous_transactions_24h >= 10:
        score += 8

    if transaction.failed_attempts_24h >= 5:
        score += 15
    elif transaction.failed_attempts_24h >= 2:
        score += 8

    if transaction.foreign_transaction:
        score += 10

    if transaction.new_device:
        score += 8

    return min(score, 100)


def get_risk_level(score: int) -> str:
    if score >= 70:
        return "critical"

    if score >= 50:
        return "high"

    if score >= 30:
        return "medium"

    return "low"


def predict_fraud_probability(
    transaction: TransactionRequest,
) -> float:
    model = load_model()

    input_data = pd.DataFrame(
        [
            {
                "amount": transaction.amount,
                "transaction_hour": transaction.transaction_hour,
                "account_age_days": transaction.account_age_days,
                "previous_transactions_24h": transaction.previous_transactions_24h,
                "failed_attempts_24h": transaction.failed_attempts_24h,
                "foreign_transaction": int(
                    transaction.foreign_transaction
                ),
                "new_device": int(
                    transaction.new_device
                ),
            }
        ],
        columns=FEATURE_COLUMNS,
    )

    probability = model.predict_proba(
        input_data
    )[0][1]

    return round(
        float(probability),
        4,
    )


def analyze_transaction(
    transaction: TransactionRequest,
) -> dict:
    risk_score = calculate_risk_score(
        transaction
    )

    risk_level = get_risk_level(
        risk_score
    )

    fraud_probability = predict_fraud_probability(
        transaction
    )

    return {
        "transaction_id": transaction.transaction_id,
        "fraud_probability": fraud_probability,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "is_suspicious": fraud_probability >= 0.50,
    }
