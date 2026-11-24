import numpy as np


def frames_to_float(frames):
    """Concatène des frames int16 en un signal float32 entre -1 et 1."""
    return np.concatenate(frames).astype(np.float32) / 32768.0
