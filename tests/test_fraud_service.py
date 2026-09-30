from app.schemas.transaction import TransactionRequest
from app.services.fraud_service import (
    calculate_risk_score,
    get_risk_level,
    calculate_fraud_probability,
    analyze_transaction,
)


def create_low_risk_transaction():
    return TransactionRequest(
        transaction_id="TX-LOW-001",
        amount=50,
        transaction_hour=14,
        account_age_days=800,
        previous_transactions_24h=1,
        failed_attempts_24h=0,
        foreign_transaction=False,
        new_device=False,
    )


def create_high_risk_transaction():
    return TransactionRequest(
        transaction_id="TX-HIGH-001",
        amount=7500,
        transaction_hour=2,
        account_age_days=10,
        previous_transactions_24h=30,
        failed_attempts_24h=7,
        foreign_transaction=True,
        new_device=True,
    )


def test_low_risk_score():
    transaction = create_low_risk_transaction()

    score = calculate_risk_score(transaction)

    assert score == 0


def test_high_risk_score():
    transaction = create_high_risk_transaction()

    score = calculate_risk_score(transaction)

    assert score >= 70
    assert score <= 100


def test_risk_levels():
    assert get_risk_level(10) == "low"
    assert get_risk_level(35) == "medium"
    assert get_risk_level(55) == "high"
    assert get_risk_level(80) == "critical"


def test_fraud_probability():
    probability = calculate_fraud_probability(75)

    assert probability == 0.75


def test_transaction_analysis():
    transaction = create_high_risk_transaction()

    result = analyze_transaction(transaction)

    assert result["transaction_id"] == "TX-HIGH-001"
    assert result["risk_score"] >= 70
    assert result["risk_level"] == "critical"
    assert result["is_suspicious"] is True
