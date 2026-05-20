"""OpenAI helpers for natural text correction and realistic speech."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


DEFAULT_TEXT_MODEL = "gpt-4o-mini"
DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_TTS_VOICE = "coral"

VOICE_TONES = {
    "Normal": "Habla en espanol mexicano con voz clara, natural y calida. Usa ritmo conversacional.",
    "Alegre": "Habla en espanol mexicano con tono alegre, amable y optimista. Sonrie con la voz sin exagerar.",
    "Triste": "Habla en espanol mexicano con tono triste, suave y pausado. Transmite seriedad y vulnerabilidad.",
    "Enojado": "Habla en espanol mexicano con tono enojado y firme, pero sin gritar. Transmite molestia controlada.",
    "Emocionado": "Habla en espanol mexicano con tono emocionado, energetico y expresivo. Usa un ritmo vivo.",
    "Calmado": "Habla en espanol mexicano con tono calmado, lento y tranquilizador. Transmite paz y seguridad.",
    "Urgente": "Habla en espanol mexicano con tono urgente, claro y directo. Transmite prioridad sin sonar alarmista.",
}


def has_openai_api_key() -> bool:
    """Return True when the OpenAI API key is configured."""
    return bool(os.getenv("OPENAI_API_KEY"))


def get_openai_client():
    """Create an OpenAI client using OPENAI_API_KEY from the environment."""
    from openai import OpenAI

    return OpenAI()


def naturalize_signed_text(raw_text: str) -> str:
    """Convert detected sign spelling into a natural Spanish sentence."""
    text = raw_text.strip()
    if not text:
        raise ValueError("No hay texto para corregir.")

    client = get_openai_client()
    model = os.getenv("OPENAI_TEXT_MODEL", DEFAULT_TEXT_MODEL)

    response = client.responses.create(
        model=model,
        input=(
            "Eres un asistente que convierte texto deletreado desde lengua de "
            "senas a una frase natural en espanol. Corrige espacios, signos y "
            "acentos. No agregues informacion nueva. Devuelve solo la frase "
            "final, sin explicaciones.\n\n"
            f"Texto detectado: {text}"
        ),
    )

    corrected = response.output_text.strip()
    return corrected or text


def get_voice_tones() -> list[str]:
    """Return supported emotional tones for text-to-speech."""
    return list(VOICE_TONES.keys())


def synthesize_speech(text: str, tone: str = "Normal") -> bytes:
    """Generate MP3 speech bytes for a Spanish sentence using OpenAI TTS."""
    spoken_text = text.strip()
    if not spoken_text:
        raise ValueError("No hay texto para hablar.")

    client = get_openai_client()
    model = os.getenv("OPENAI_TTS_MODEL", DEFAULT_TTS_MODEL)
    voice = os.getenv("OPENAI_TTS_VOICE", DEFAULT_TTS_VOICE)
    tone_instructions = VOICE_TONES.get(tone, VOICE_TONES["Normal"])

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as file:
        speech_file = Path(file.name)

    try:
        with client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=spoken_text,
            instructions=(
                f"{tone_instructions} Evita sonar robotico y conserva buena diccion."
            ),
        ) as response:
            response.stream_to_file(speech_file)

        return speech_file.read_bytes()
    finally:
        speech_file.unlink(missing_ok=True)
