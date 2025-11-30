import argparse
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.models.signature import infer_signature
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def parse_args():
    parser = argparse.ArgumentParser(description="Train RandomForest on Iris and log to MLflow")

    parser.add_argument("--data_path", type=str, default="Data/data_raw/Iris.csv")
    parser.add_argument("--test_size", type=float, default=0.2)
    parser.add_argument("--random_state", type=int, default=42)

    # гиперпараметры модели
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=5)

    return parser.parse_args()


def load_data(path: str):
    path_obj = Path(path)
    if not path_obj.is_file():
        raise FileNotFoundError(f"Dataset not found at {path_obj.resolve()}")

    df = pd.read_csv(path_obj)

    # Пытаемся угадать таргет:
    # 1) Если есть колонка 'Species' — используем её
    # 2) Иначе берём последнюю колонку как таргет
    if "Species" in df.columns:
        target_col = "Species"
    else:
        target_col = df.columns[-1]

    X = df.drop(columns=[target_col])
    y = df[target_col]

    return X, y


def main():
    args = parse_args()

    # 1) Настройка MLflow Tracking + Model Registry
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("l6-mlflow-iris")

    # 2) Данные
    X, y = load_data(args.data_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )

    # 3) Модель
    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        random_state=args.random_state,
    )

    run_name = f"rf_n{args.n_estimators}_d{args.max_depth}"

    with mlflow.start_run(run_name=run_name):
        # --- параметры ---
        mlflow.log_param("data_path", args.data_path)
        mlflow.log_param("test_size", args.test_size)
        mlflow.log_param("random_state", args.random_state)
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("max_depth", args.max_depth)

        # --- обучение ---
        model.fit(X_train, y_train)

        # --- метрика ---
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        mlflow.log_metric("accuracy", acc)

        # --- логирование модели + регистрация в Model Registry ---
        signature = infer_signature(X_train, model.predict(X_train))
        input_example = X_train.iloc[:5]

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            signature=signature,
            input_example=input_example,
            registered_model_name="iris_rf_model",  # Registered Model в Model Registry
        )

        print(f"Accuracy: {acc:.4f}")
        print("Model logged and registered in MLflow.")


if __name__ == "__main__":
    main()
