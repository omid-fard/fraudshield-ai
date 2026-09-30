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


@router.post(
    "/predict",
    response_model=FraudPredictionResponse,
    summary="Analyze transaction fraud risk",
)
def predict_fraud(
    transaction: TransactionRequest,
) -> FraudPredictionResponse:
    """
    Analyze a financial transaction and return its fraud risk assessment.
    """

    result = analyze_transaction(transaction)

    return FraudPredictionResponse(**result)
