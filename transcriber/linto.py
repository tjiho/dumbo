from transformers import pipeline

from consts import LINTO_MODEL, SAMPLE_RATE
from transcriber.audio import frames_to_float


def load():
    asr = pipeline("automatic-speech-recognition", model=LINTO_MODEL)

    def transcribe(frames):
        result = asr({"raw": frames_to_float(frames), "sampling_rate": SAMPLE_RATE})
        return result["text"].strip()

    return transcribe
