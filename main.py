from collections import deque

import numpy as np
from faster_whisper import WhisperModel
from openwakeword.model import Model

from consts import (
    LANGUAGE,
    MAX_FRAMES,
    PRE_FRAMES,
    SILENCE_FRAMES,
    SILENCE_THRESHOLD,
    WAKEWORD,
    WAKEWORD_THRESHOLD,
    WHISPER_COMPUTE_TYPE,
    WHISPER_DEVICE,
    WHISPER_MODEL,
)
from microphone import mic_frames
from mqtt import connect, publish

model = Model(wakeword_models=[WAKEWORD], inference_framework="onnx")

whisper = WhisperModel(
    WHISPER_MODEL, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE_TYPE
)
history = deque(maxlen=PRE_FRAMES)


def is_silence(frame, threshold=SILENCE_THRESHOLD):
    return np.sqrt(np.mean(frame.astype(np.float32) ** 2)) < threshold


connect()
frames = mic_frames()
for frame in frames:
    history.append(frame)
    scores = model.predict(frame)

    if scores[WAKEWORD] > WAKEWORD_THRESHOLD:
        print("detected")
        command = list(history)

        # continuer à lire le micro jusqu'au silence
        silent = 0
        for f in frames:
            command.append(f)
            silent = silent + 1 if is_silence(f) else 0
            if silent >= SILENCE_FRAMES or len(command) >= MAX_FRAMES:
                break

        audio = np.concatenate(command).astype(np.float32) / 32768.0
        segments, _ = whisper.transcribe(audio, language=LANGUAGE)
        text = " ".join(s.text for s in segments).strip()
        print("→", text)
        if text:
            publish(text)

        model.reset()
        history.clear()
