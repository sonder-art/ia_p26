"""Train a sign gesture classifier from collected hand landmarks."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from src.preprocessing import FEATURE_COUNT, feature_columns, normalize_landmarks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the gesture classifier.")
    parser.add_argument("--dataset", default="dataset.csv", help="Input CSV dataset.")
    parser.add_argument("--output", default="model.joblib", help="Output model file.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Minimum probability required to display a gesture.",
    )
    parser.add_argument(
        "--estimators",
        type=int,
        default=200,
        help="Number of trees for RandomForestClassifier.",
    )
    return parser.parse_args()


def load_dataset(path: Path) -> tuple[np.ndarray, np.ndarray]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)
    expected_columns = ["label", *feature_columns()]
    missing_columns = [column for column in expected_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {missing_columns}")

    if df.empty:
        raise ValueError("Dataset is empty. Collect samples before training.")

    y = df["label"].astype(str).to_numpy()
    raw_features = df[feature_columns()].to_numpy(dtype=np.float32)

    if raw_features.shape[1] != FEATURE_COUNT:
        raise ValueError(f"Expected {FEATURE_COUNT} features.")

    x = np.vstack([normalize_landmarks(row) for row in raw_features])
    return x, y


def main() -> None:
    args = parse_args()
    x, y = load_dataset(Path(args.dataset))

    label_counts = pd.Series(y).value_counts()
    if len(label_counts) < 2:
        raise ValueError("At least two labels are required to train a classifier.")
    if (label_counts < 2).any():
        raise ValueError("Each label needs at least two samples for train/test split.")

    test_sample_count = max(int(np.ceil(len(y) * 0.2)), len(label_counts))

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_sample_count,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=args.estimators,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    labels = sorted(np.unique(y).tolist())

    print("Classification Report")
    print(classification_report(y_test, y_pred, labels=labels))

    print("Confusion Matrix")
    print(pd.DataFrame(confusion_matrix(y_test, y_pred, labels=labels), index=labels, columns=labels))

    artifact = {
        "model": model,
        "labels": labels,
        "threshold": args.threshold,
        "feature_columns": feature_columns(),
    }
    joblib.dump(artifact, args.output)
    print(f"Model saved to {args.output}")


if __name__ == "__main__":
    main()
