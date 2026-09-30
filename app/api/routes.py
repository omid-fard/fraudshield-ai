from pathlib import Path

from fastapi import APIRouter

from app.schemas.transaction import (
    TransactionRequest,
    FraudPredictionResponse,
)
from app.services.fraud_service import analyze_transaction


router = APIRouter(
    prefix="/api/v1",
    tags=["Fraud Detection"],
)


MODEL_PATH = Path("ml/model.pkl")


@router.post(
    "/predict",
    response_model=FraudPredictionResponse,
    summary="Analyze transaction fraud risk",
)
def predict_fraud(
    transaction: TransactionRequest,
) -> FraudPredictionResponse:
    result = analyze_transaction(transaction)

    return FraudPredictionResponse(**result)


@router.get(
    "/model/status",
    summary="Get fraud detection model status",
)
def model_status():
    return {
        "model": "RandomForestClassifier",
        "version": "1.0.0",
        "model_file": str(MODEL_PATH),
        "model_available": MODEL_PATH.exists(),
        "features": [
            "amount",
            "transaction_hour",
            "account_age_days",
            "previous_transactions_24h",
            "failed_attempts_24h",
            "foreign_transaction",
            "new_device",
        ],
    }
