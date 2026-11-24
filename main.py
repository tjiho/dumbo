import openwakeword
from openwakeword.model import Model
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from collections import deque

from microphone import mic_frames

model = Model(wakeword_models=["hey_mycroft"], inference_framework="onnx")

FRAME_MS = 80
PRE_FRAMES = int(1500 / FRAME_MS)     # garder ~1,5 s avant la détection
SILENCE_FRAMES = int(800 / FRAME_MS)  # 800 ms de silence = fin de commande
MAX_FRAMES = int(8000 / FRAME_MS)     # 8 s max de commande

whisper = WhisperModel("small", device="cpu", compute_type="int8")
history = deque(maxlen=PRE_FRAMES)    # ring buffer : les plus anciennes sortent seules

def is_silence(frame, threshold=500):
    return np.sqrt(np.mean(frame.astype(np.float32) ** 2)) < threshold

frames = mic_frames()
for frame in frames:
    history.append(frame)
    scores = model.predict(frame)

    if scores["hey_mycroft"] > 0.4:
        print("detected")
        command = list(history)           # l'audio du passé (wake word compris)

        # continuer à lire le micro jusqu'au silence
        silent = 0
        for f in frames:
            command.append(f)
            silent = silent + 1 if is_silence(f) else 0
            if silent >= SILENCE_FRAMES or len(command) >= MAX_FRAMES:
                break

        audio = np.concatenate(command).astype(np.float32) / 32768.0
        segments, _ = whisper.transcribe(audio, language="fr")
        print("→", " ".join(s.text for s in segments))

        model.reset()       # vide l'état interne d'openWakeWord
        history.clear()
