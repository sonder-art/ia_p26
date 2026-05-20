"""Streamlit app for real-time sign gesture classification."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

import av
import cv2
import joblib
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from streamlit_webrtc import VideoProcessorBase, WebRtcMode, webrtc_streamer

from src.mediapipe_compat import get_hand_solution_modules
from src.openai_voice import (
    get_voice_tones,
    has_openai_api_key,
    naturalize_signed_text,
    synthesize_speech,
)
from src.preprocessing import landmarks_to_flat_list, normalize_landmarks


MODEL_PATH = Path("model.joblib")


@st.cache_resource
def load_artifact(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            "model.joblib was not found. Run `python train_model.py` first."
        )
    return joblib.load(path)


class GestureVideoProcessor(VideoProcessorBase):
    def __init__(self, artifact: dict):
        self.model = artifact["model"]
        self.threshold = float(artifact.get("threshold", 0.70))
        self.prediction = "Waiting"
        self.confidence = 0.0
        self.sentence = ""
        self.candidate = ""
        self.candidate_frames = 0
        self.release_frames = 0
        self.ready_for_next_letter = True
        self.stable_frames_required = 12
        self.release_frames_required = 8
        self.lock = Lock()

        self.mp_hands, self.mp_drawing, self.mp_styles = get_hand_solution_modules()
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_image)

        label = "No hand"
        confidence = 0.0

        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            flat_landmarks = landmarks_to_flat_list(hand_landmarks)
            normalized = normalize_landmarks(flat_landmarks).reshape(1, -1)

            probabilities = self.model.predict_proba(normalized)[0]
            best_index = int(np.argmax(probabilities))
            confidence = float(probabilities[best_index])
            predicted_label = str(self.model.classes_[best_index])
            label = predicted_label if confidence >= self.threshold else "Incierto"

            self.mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_styles.get_default_hand_landmarks_style(),
                self.mp_styles.get_default_hand_connections_style(),
            )

        self._update_sentence(label, confidence)

        color = (0, 255, 0) if confidence >= self.threshold else (0, 165, 255)
        cv2.putText(
            image,
            f"{label} ({confidence:.0%})",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            color,
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            f"Texto: {self.sentence[-28:]}",
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        return av.VideoFrame.from_ndarray(image, format="bgr24")

    def _update_sentence(self, label: str, confidence: float) -> None:
        with self.lock:
            self.prediction = label
            self.confidence = confidence

            if label in ("No hand", "Incierto"):
                self.candidate = ""
                self.candidate_frames = 0
                self.release_frames += 1
                if self.release_frames >= self.release_frames_required:
                    self.ready_for_next_letter = True
                return

            self.release_frames = 0

            if label == self.candidate:
                self.candidate_frames += 1
            else:
                self.candidate = label
                self.candidate_frames = 1

            if (
                self.ready_for_next_letter
                and self.candidate_frames >= self.stable_frames_required
            ):
                self.sentence += label
                self.ready_for_next_letter = False

    def get_state(self) -> tuple[str, float, str]:
        with self.lock:
            return self.prediction, self.confidence, self.sentence

    def append_space(self) -> None:
        with self.lock:
            if self.sentence and not self.sentence.endswith(" "):
                self.sentence += " "

    def backspace(self) -> None:
        with self.lock:
            self.sentence = self.sentence[:-1]

    def clear_sentence(self) -> None:
        with self.lock:
            self.sentence = ""
            self.candidate = ""
            self.candidate_frames = 0
            self.release_frames = 0
            self.ready_for_next_letter = True


def speak_in_browser(text: str) -> None:
    escaped_text = json.dumps(text)
    components.html(
        f"""
        <script>
        const text = {escaped_text};
        if (text.trim().length > 0) {{
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = "es-MX";
            utterance.rate = 0.95;
            window.speechSynthesis.speak(utterance);
        }}
        </script>
        """,
        height=0,
    )


def render_controls(processor: GestureVideoProcessor) -> None:
    prediction, confidence, sentence = processor.get_state()

    col1, col2, col3 = st.columns(3)
    if col1.button("Espacio"):
        processor.append_space()
        st.session_state["corrected_text"] = ""
        st.session_state["ai_audio"] = None
    if col2.button("Borrar"):
        processor.backspace()
        st.session_state["corrected_text"] = ""
        st.session_state["ai_audio"] = None
    if col3.button("Limpiar"):
        processor.clear_sentence()
        st.session_state["corrected_text"] = ""
        st.session_state["ai_audio"] = None

    prediction, confidence, sentence = processor.get_state()
    corrected_text = st.session_state.get("corrected_text", "")

    st.metric("Prediccion actual", prediction, f"{confidence:.0%}")
    st.text_area("Texto detectado", value=sentence, height=90, disabled=True)
    st.text_area("Texto corregido por IA", value=corrected_text, height=90, disabled=True)

    st.caption("La voz generada con IA es sintetica y no corresponde a una persona real.")
    voice_tone = st.selectbox("Tono de voz para la IA", get_voice_tones())

    col4, col5 = st.columns(2)
    if col4.button("Hablar gratis"):
        speak_in_browser(sentence)
    if col5.button("Hablar con IA"):
        if not sentence.strip():
            st.warning("Primero forma una oracion con las senas.")
        elif not has_openai_api_key():
            st.error(
                "Falta OPENAI_API_KEY. Configurala en la terminal antes de abrir Streamlit."
            )
        else:
            try:
                with st.spinner("Corrigiendo texto y generando voz con IA..."):
                    corrected_text = naturalize_signed_text(sentence)
                    audio_bytes = synthesize_speech(corrected_text, tone=voice_tone)
                st.session_state["corrected_text"] = corrected_text
                st.session_state["ai_audio"] = audio_bytes
                st.session_state["ai_voice_tone"] = voice_tone
                st.success("Audio generado con IA.")
            except Exception as error:
                st.error(f"No se pudo generar audio con IA: {error}")

    if st.session_state.get("ai_audio"):
        st.caption(f"Tono usado: {st.session_state.get('ai_voice_tone', 'Normal')}")
        st.audio(st.session_state["ai_audio"], format="audio/mp3")


def main() -> None:
    st.set_page_config(page_title="Clasificador de Gestos")
    st.title("Clasificador de Gestos de Lengua de Senas")

    try:
        artifact = load_artifact(MODEL_PATH)
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    labels = ", ".join(str(label) for label in artifact.get("labels", []))
    threshold = float(artifact.get("threshold", 0.70))

    st.write(f"Labels entrenados: {labels}")
    st.write(f"Umbral de confianza: {threshold:.0%}")

    ctx = webrtc_streamer(
        key="gesture-classifier",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=lambda: GestureVideoProcessor(artifact),
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if ctx.video_processor:
        render_controls(ctx.video_processor)


if __name__ == "__main__":
    main()
