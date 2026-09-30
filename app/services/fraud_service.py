from app.schemas.transaction import TransactionRequest


def calculate_risk_score(transaction: TransactionRequest) -> int:
    """
    Calculate a rule-based fraud risk score between 0 and 100.
    """

    score = 0

    # High transaction amount
    if transaction.amount >= 5000:
        score += 25
    elif transaction.amount >= 2000:
        score += 15
    elif transaction.amount >= 1000:
        score += 8

    # Unusual transaction time
    if transaction.transaction_hour <= 5:
        score += 12

    # New account
    if transaction.account_age_days < 30:
        score += 15
    elif transaction.account_age_days < 90:
        score += 8

    # High transaction frequency
    if transaction.previous_transactions_24h >= 20:
        score += 15
    elif transaction.previous_transactions_24h >= 10:
        score += 8

    # Failed attempts
    if transaction.failed_attempts_24h >= 5:
        score += 15
    elif transaction.failed_attempts_24h >= 2:
        score += 8

    # Foreign transaction
    if transaction.foreign_transaction:
        score += 10

    # New device
    if transaction.new_device:
        score += 8

    return min(score, 100)


def get_risk_level(score: int) -> str:
    """
    Convert numerical risk score into a risk category.
    """

    if score >= 70:
        return "critical"

    if score >= 50:
        return "high"

    if score >= 30:
        return "medium"

    return "low"


def calculate_fraud_probability(score: int) -> float:
    """
    Convert risk score into a temporary fraud probability.

    This will later be replaced by the machine learning model.
    """

    return round(score / 100, 2)


def analyze_transaction(transaction: TransactionRequest) -> dict:
    """
    Analyze a transaction and return fraud intelligence results.
    """

    risk_score = calculate_risk_score(transaction)
    risk_level = get_risk_level(risk_score)
    fraud_probability = calculate_fraud_probability(risk_score)

    return {
        "transaction_id": transaction.transaction_id,
        "fraud_probability": fraud_probability,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "is_suspicious": risk_score >= 50,
    }
