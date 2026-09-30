import random
from pathlib import Path

import pandas as pd


OUTPUT_PATH = Path("data/sample_transactions.csv")
NUMBER_OF_ROWS = 2000


def generate_transaction(index: int) -> dict:
    amount = round(random.uniform(5, 10000), 2)
    transaction_hour = random.randint(0, 23)
    account_age_days = random.randint(1, 2500)
    previous_transactions_24h = random.randint(0, 30)
    failed_attempts_24h = random.randint(0, 8)
    foreign_transaction = random.choice([True, False])
    new_device = random.choice([True, False])

    fraud_score = 0

    if amount >= 5000:
        fraud_score += 25
    elif amount >= 2000:
        fraud_score += 15

    if transaction_hour <= 5:
        fraud_score += 12

    if account_age_days < 30:
        fraud_score += 15
    elif account_age_days < 90:
        fraud_score += 8

    if previous_transactions_24h >= 20:
        fraud_score += 15
    elif previous_transactions_24h >= 10:
        fraud_score += 8

    if failed_attempts_24h >= 5:
        fraud_score += 15
    elif failed_attempts_24h >= 2:
        fraud_score += 8

    if foreign_transaction:
        fraud_score += 10

    if new_device:
        fraud_score += 8

    fraud_probability = min(fraud_score / 100, 1.0)

    is_fraud = int(
        random.random() < fraud_probability
    )

    return {
        "transaction_id": f"TX-{index:06d}",
        "amount": amount,
        "transaction_hour": transaction_hour,
        "account_age_days": account_age_days,
        "previous_transactions_24h": previous_transactions_24h,
        "failed_attempts_24h": failed_attempts_24h,
        "foreign_transaction": int(foreign_transaction),
        "new_device": int(new_device),
        "is_fraud": is_fraud,
    }


def generate_dataset():
    random.seed(42)

    transactions = [
        generate_transaction(index)
        for index in range(1, NUMBER_OF_ROWS + 1)
    ]

    dataframe = pd.DataFrame(transactions)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dataframe.to_csv(
        OUTPUT_PATH,
        index=False
    )

    fraud_count = dataframe["is_fraud"].sum()

    print(
        f"Dataset created successfully: {OUTPUT_PATH}"
    )
    print(
        f"Total transactions: {len(dataframe)}"
    )
    print(
        f"Fraud transactions: {fraud_count}"
    )
    print(
        f"Fraud rate: {fraud_count / len(dataframe):.2%}"
    )


if __name__ == "__main__":
    generate_dataset()
