"""Compatibility helpers for MediaPipe legacy solutions imports."""

from __future__ import annotations

from importlib import import_module


def get_hand_solution_modules():
    """Return MediaPipe Hands, drawing utils, and drawing styles modules.

    Some MediaPipe builds do not expose the legacy API as ``mp.solutions`` even
    when the modules are still installed. This helper supports both layouts.
    """
    module_sets = (
        (
            "mediapipe.solutions.hands",
            "mediapipe.solutions.drawing_utils",
            "mediapipe.solutions.drawing_styles",
        ),
        (
            "mediapipe.python.solutions.hands",
            "mediapipe.python.solutions.drawing_utils",
            "mediapipe.python.solutions.drawing_styles",
        ),
    )

    errors: list[str] = []
    for hands_name, drawing_utils_name, drawing_styles_name in module_sets:
        try:
            hands = import_module(hands_name)
            drawing_utils = import_module(drawing_utils_name)
            drawing_styles = import_module(drawing_styles_name)
            return hands, drawing_utils, drawing_styles
        except ImportError as error:
            errors.append(f"{hands_name}: {error}")

    raise ImportError(
        "Could not import MediaPipe Hands legacy solutions. "
        "Replace your installed MediaPipe version with: "
        "pip uninstall -y mediapipe && pip install mediapipe==0.10.14\n"
        f"Import attempts: {' | '.join(errors)}"
    )
