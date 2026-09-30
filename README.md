# FraudShield AI
![Python Tests](https://github.com/omid-fard/fraudshield-ai/actions/workflows/python-tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-black)

AI-powered financial fraud detection and transaction risk intelligence platform built with Python, FastAPI, Machine Learning, Docker, and GitHub Actions.

## Overview

FraudShield AI is a portfolio-grade fraud detection project designed to demonstrate how transaction risk analysis, machine learning, REST APIs, automated testing, and containerization can be combined in a production-style architecture.

The system analyzes financial transactions using both rule-based risk scoring and a trained Random Forest machine learning model.

## Key Features

- Fraud risk scoring from 0 to 100
- Machine-learning-based fraud probability
- Transaction risk classification
- FastAPI REST API
- Synthetic transaction data generation
- Random Forest model training pipeline
- Model performance metrics
- Automated API and ML tests
- GitHub Actions CI pipeline
- Docker support
- Docker integration testing

## Technology Stack

- Python 3.12
- FastAPI
- Scikit-learn
- Pandas
- Joblib
- Pydantic
- Pytest
- Docker
- GitHub Actions

## Project Architecture

```text
fraudshield-ai/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── transaction.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── fraud_service.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── data/
│   └── generate_data.py
│
├── ml/
│   └── train_model.py
│
├── tests/
│   ├── test_api.py
│   ├── test_fraud_service.py
│   └── test_ml_model.py
│
├── .github/
│   └── workflows/
│       └── python-tests.yml
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
