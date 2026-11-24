import queue

import numpy as np
import sounddevice as sd

from consts import FRAME_SIZE, SAMPLE_RATE

q: queue.Queue[np.ndarray] = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status)  # overflow, etc.
    q.put(indata[:, 0].copy())  # mono, copie obligatoire


def mic_frames(device=None):
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=FRAME_SIZE,
        device=device,
        callback=callback,
    ):
        while True:
            yield q.get()
