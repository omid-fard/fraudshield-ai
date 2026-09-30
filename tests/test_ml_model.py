from app.schemas.transaction import TransactionRequest
from app.services.fraud_service import (
    predict_fraud_probability,
)


def test_ml_prediction_returns_probability():
    transaction = TransactionRequest(
        transaction_id="TX-ML-001",
        amount=4200,
        transaction_hour=1,
        account_age_days=20,
        previous_transactions_24h=18,
        failed_attempts_24h=4,
        foreign_transaction=True,
        new_device=True,
    )

    probability = predict_fraud_probability(transaction)

    assert isinstance(probability, float)
    assert 0.0 <= probability <= 1.0


def test_low_risk_transaction_has_valid_probability():
    transaction = TransactionRequest(
        transaction_id="TX-ML-LOW",
        amount=25,
        transaction_hour=13,
        account_age_days=1200,
        previous_transactions_24h=1,
        failed_attempts_24h=0,
        foreign_transaction=False,
        new_device=False,
    )

    probability = predict_fraud_probability(transaction)

    assert 0.0 <= probability <= 1.0
