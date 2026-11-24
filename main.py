import argparse
from collections import deque

import numpy as np
from openwakeword.model import Model

from consts import (
    MAX_FRAMES,
    PRE_FRAMES,
    SILENCE_FRAMES,
    SILENCE_THRESHOLD,
    TRANSCRIBER,
    WAKEWORD,
    WAKEWORD_THRESHOLD,
)
from microphone import mic_frames
from mqtt import connect, publish
from transcriber import ENGINES, load

parser = argparse.ArgumentParser()
parser.add_argument(
    "--transcriber",
    choices=ENGINES,
    default=TRANSCRIBER,
    help="moteur de transcription",
)
args = parser.parse_args()

transcribe = load(args.transcriber)
model = Model(wakeword_models=[WAKEWORD], inference_framework="onnx")

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

        text = transcribe(command)
        print("→", text)
        if text:
            publish(text)

        model.reset()
        history.clear()
