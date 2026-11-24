import queue
import numpy as np
import sounddevice as sd

SR = 16000
FRAME = 1280  # 80 ms à 16 kHz

q: queue.Queue[np.ndarray] = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)               # overflow, etc.
    q.put(indata[:, 0].copy())      # mono, copie obligatoire

def mic_frames(device=None):
    with sd.InputStream(samplerate=SR, channels=1, dtype="int16",
                        blocksize=FRAME, device=device, callback=callback):
        while True:
            yield q.get()
