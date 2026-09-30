from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    transaction_id: str = Field(
        ...,
        description="Unique transaction identifier"
    )

    amount: float = Field(
        ...,
        gt=0,
        description="Transaction amount"
    )

    transaction_hour: int = Field(
        ...,
        ge=0,
        le=23,
        description="Hour of transaction in 24-hour format"
    )

    account_age_days: int = Field(
        ...,
        ge=0,
        description="Age of customer account in days"
    )

    previous_transactions_24h: int = Field(
        ...,
        ge=0,
        description="Number of transactions in the previous 24 hours"
    )

    failed_attempts_24h: int = Field(
        ...,
        ge=0,
        description="Number of failed transaction attempts in the previous 24 hours"
    )

    foreign_transaction: bool = Field(
        ...,
        description="Whether the transaction was made from a foreign location"
    )

    new_device: bool = Field(
        ...,
        description="Whether the transaction was made using a new device"
    )


class FraudPredictionResponse(BaseModel):
    transaction_id: str
    fraud_probability: float
    risk_score: int
    risk_level: str
    is_suspicious: bool
