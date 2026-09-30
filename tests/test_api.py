from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "FraudShield AI"
    assert data["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_fraud_prediction_endpoint():
    payload = {
        "transaction_id": "TX-10001",
        "amount": 6500,
        "transaction_hour": 2,
        "account_age_days": 12,
        "previous_transactions_24h": 25,
        "failed_attempts_24h": 6,
        "foreign_transaction": True,
        "new_device": True,
    }

    response = client.post(
        "/api/v1/predict",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_id"] == "TX-10001"
    assert 0.0 <= data["fraud_probability"] <= 1.0
    assert 0 <= data["risk_score"] <= 100
    assert data["risk_level"] in [
        "low",
        "medium",
        "high",
        "critical",
    ]
    assert isinstance(data["is_suspicious"], bool)


def test_model_status_endpoint():
    response = client.get("/api/v1/model/status")

    assert response.status_code == 200

    data = response.json()

    assert data["model"] == "RandomForestClassifier"
    assert data["version"] == "1.0.0"
    assert isinstance(data["model_available"], bool)

    expected_features = [
        "amount",
        "transaction_hour",
        "account_age_days",
        "previous_transactions_24h",
        "failed_attempts_24h",
        "foreign_transaction",
        "new_device",
    ]

    assert data["features"] == expected_features
