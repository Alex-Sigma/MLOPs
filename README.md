# 📘 MLflow Homework — Iris Classification (l6-mlflow-iris)

This project integrates MLflow for experiment tracking and model registry using the Iris dataset.

The homework includes:

- Adding MLflow to the project
- Logging training parameters, metrics, and artifacts
- Registering the model in MLflow Model Registry
- Creating a clean Pull Request with all changes

# Setup

## 1. Create and Activate Virtual Environment

python3 -m venv .venv
source .venv/bin/activate

## 2. Install Dependencies

python -m pip install -r requirements.txt

## 3. Train the Model

python train.py

## 4. Start MLflow UI

mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000

http://127.0.0.1:5000

# Summary

This project demonstrates:

- MLflow experiment tracking
- Logging parameters, metrics, and model artifacts
- Model registration in MLflow Model Registry
- Reproducible training workflow
