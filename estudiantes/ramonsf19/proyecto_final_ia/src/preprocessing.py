"""Preprocessing helpers for MediaPipe hand landmarks."""

from __future__ import annotations

import numpy as np


LANDMARK_COUNT = 21
COORDS_PER_LANDMARK = 3
FEATURE_COUNT = LANDMARK_COUNT * COORDS_PER_LANDMARK


def normalize_landmarks(flat_landmarks: list[float] | np.ndarray) -> np.ndarray:
    """Normalize flattened hand landmarks by wrist origin and unit scale.

    Args:
        flat_landmarks: Sequence with 63 values ordered as
            [x1, y1, z1, ..., x21, y21, z21].

    Returns:
        A flattened numpy array with 63 normalized values.

    Raises:
        ValueError: If the input does not contain exactly 63 values.
    """
    landmarks = np.asarray(flat_landmarks, dtype=np.float32)

    if landmarks.size != FEATURE_COUNT:
        raise ValueError(
            f"Expected {FEATURE_COUNT} values, received {landmarks.size}."
        )

    landmarks = landmarks.reshape(LANDMARK_COUNT, COORDS_PER_LANDMARK)
    wrist = landmarks[0].copy()
    translated = landmarks - wrist

    distances = np.linalg.norm(translated, axis=1)
    max_distance = float(np.max(distances))

    if max_distance > 0:
        translated = translated / max_distance

    return translated.flatten()


def landmarks_to_flat_list(hand_landmarks) -> list[float]:
    """Convert a MediaPipe hand landmark result into a flat 63-value list."""
    values: list[float] = []
    for landmark in hand_landmarks.landmark:
        values.extend([landmark.x, landmark.y, landmark.z])
    return values


def feature_columns() -> list[str]:
    """Return CSV feature names: x1, y1, z1, ..., x21, y21, z21."""
    columns: list[str] = []
    for index in range(1, LANDMARK_COUNT + 1):
        columns.extend([f"x{index}", f"y{index}", f"z{index}"])
    return columns
