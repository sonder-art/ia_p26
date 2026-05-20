"""Inspect and clean the gesture dataset safely."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.preprocessing import feature_columns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage dataset.csv samples.")
    parser.add_argument("--dataset", default="dataset.csv", help="Dataset CSV path.")

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--summary",
        action="store_true",
        help="Show sample counts by label.",
    )
    action_group.add_argument(
        "--delete-label",
        help="Delete all samples for one label, for example R.",
    )
    action_group.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete all samples and keep only the header.",
    )

    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create a backup before deleting samples.",
    )
    return parser.parse_args()


def expected_columns() -> list[str]:
    return ["label", *feature_columns()]


def ensure_dataset_exists(path: Path) -> None:
    if path.exists():
        return

    pd.DataFrame(columns=expected_columns()).to_csv(path, index=False)


def load_dataset(path: Path) -> pd.DataFrame:
    ensure_dataset_exists(path)
    df = pd.read_csv(path)
    missing_columns = [column for column in expected_columns() if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {missing_columns}")
    return df


def create_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.with_name(f"{path.stem}_backup_{timestamp}{path.suffix}")
    shutil.copy2(path, backup_path)
    return backup_path


def print_summary(df: pd.DataFrame) -> None:
    if df.empty:
        print("Dataset is empty.")
        return

    counts = df["label"].astype(str).value_counts().sort_index()
    print("Samples by label:")
    print(counts.to_string())
    print(f"\nTotal samples: {len(df)}")


def delete_label(df: pd.DataFrame, label: str) -> tuple[pd.DataFrame, int]:
    normalized_label = label.strip().upper()
    labels = df["label"].astype(str).str.upper()
    keep_mask = labels != normalized_label
    deleted_count = int((~keep_mask).sum())
    return df.loc[keep_mask].copy(), deleted_count


def main() -> None:
    args = parse_args()
    dataset_path = Path(args.dataset)
    df = load_dataset(dataset_path)

    if args.summary:
        print_summary(df)
        return

    if not args.no_backup:
        backup_path = create_backup(dataset_path)
        print(f"Backup created: {backup_path}")

    if args.delete_label:
        updated_df, deleted_count = delete_label(df, args.delete_label)
        updated_df.to_csv(dataset_path, index=False)
        print(f"Deleted {deleted_count} samples for label '{args.delete_label.upper()}'.")
        print(f"Remaining samples: {len(updated_df)}")
        return

    if args.delete_all:
        pd.DataFrame(columns=expected_columns()).to_csv(dataset_path, index=False)
        print("Deleted all samples. Header was preserved.")


if __name__ == "__main__":
    main()
