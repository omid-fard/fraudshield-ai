from fastapi import FastAPI

from app.api.routes import router as fraud_router


app = FastAPI(
    title="FraudShield AI",
    description="AI-powered financial fraud detection and transaction risk intelligence API.",
    version="1.0.0",
)


app.include_router(fraud_router)


@app.get("/")
def root():
    return {
        "project": "FraudShield AI",
        "status": "running",
        "message": "Fraud detection API is operational."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
