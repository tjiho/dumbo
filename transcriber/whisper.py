from faster_whisper import WhisperModel

from consts import LANGUAGE, WHISPER_COMPUTE_TYPE, WHISPER_DEVICE, WHISPER_MODEL
from transcriber.audio import frames_to_float


def load():
    model = WhisperModel(
        WHISPER_MODEL, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE_TYPE
    )

    def transcribe(frames):
        segments, _ = model.transcribe(frames_to_float(frames), language=LANGUAGE)
        return " ".join(s.text for s in segments).strip()

    return transcribe
