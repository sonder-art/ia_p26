"""Collect hand landmark samples from a webcam into dataset.csv."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import cv2

from src.mediapipe_compat import get_hand_solution_modules
from src.preprocessing import feature_columns, landmarks_to_flat_list


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect MediaPipe hand landmarks for one sign label."
    )
    label_group = parser.add_mutually_exclusive_group(required=True)
    label_group.add_argument("--label", help="Gesture label, for example A.")
    label_group.add_argument(
        "--labels",
        nargs="+",
        help="Gesture labels to collect in sequence, for example A B C.",
    )
    label_group.add_argument(
        "--alphabet",
        action="store_true",
        help="Collect one dataset batch for labels A through Z.",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=300,
        help="Number of samples to capture for this label.",
    )
    parser.add_argument(
        "--output",
        default="dataset.csv",
        help="CSV file where samples will be appended.",
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="OpenCV camera index.",
    )
    return parser.parse_args()


def ensure_csv_header(path: Path) -> None:
    if path.exists() and path.stat().st_size > 0:
        return

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["label", *feature_columns()])


def resolve_labels(args: argparse.Namespace) -> list[str]:
    if args.alphabet:
        return [chr(code) for code in range(ord("A"), ord("Z") + 1)]
    if args.labels:
        return [label.strip().upper() for label in args.labels if label.strip()]
    return [args.label.strip().upper()]


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    ensure_csv_header(output_path)
    labels = resolve_labels(args)

    mp_hands, mp_drawing, mp_styles = get_hand_solution_modules()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}.")

    with output_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        ) as hands:
            should_stop = False

            for label in labels:
                captured = 0
                print(f"Collecting {args.samples} samples for label '{label}'.")
                print("Press s to start this label, or q to quit.")

                started = False
                while cap.isOpened() and captured < args.samples:
                    success, frame = cap.read()
                    if not success:
                        should_stop = True
                        break

                    frame = cv2.flip(frame, 1)
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    rgb_frame.flags.writeable = False
                    result = hands.process(rgb_frame)
                    rgb_frame.flags.writeable = True

                    if started and result.multi_hand_landmarks:
                        hand_landmarks = result.multi_hand_landmarks[0]
                        row = [label, *landmarks_to_flat_list(hand_landmarks)]
                        writer.writerow(row)
                        file.flush()
                        captured += 1

                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_styles.get_default_hand_landmarks_style(),
                            mp_styles.get_default_hand_connections_style(),
                        )
                    elif result.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            result.multi_hand_landmarks[0],
                            mp_hands.HAND_CONNECTIONS,
                            mp_styles.get_default_hand_landmarks_style(),
                            mp_styles.get_default_hand_connections_style(),
                        )

                    status = "Capturing" if started else "Press s to start"
                    cv2.putText(
                        frame,
                        f"Label: {label} | Samples: {captured}/{args.samples}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        f"{status} | Press q to quit",
                        (10, 65),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )

                    cv2.imshow("Data collection", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("s"):
                        started = True
                    elif key == ord("q"):
                        should_stop = True
                        break

                print(f"Captured {captured} samples for label '{label}'.")
                if should_stop:
                    break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Saved samples in {output_path}.")


if __name__ == "__main__":
    main()
