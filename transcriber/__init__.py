"""Moteurs de transcription interchangeables.

Chaque module de ce dossier expose une fonction `load()` qui charge le modèle
et renvoie une fonction `transcribe(frames) -> str`.
"""

import importlib

ENGINES = {
    "whisper": "transcriber.whisper",
    "linto": "transcriber.linto",
}


def load(engine):
    # import à la demande : seules les dépendances du moteur choisi sont requises
    return importlib.import_module(ENGINES[engine]).load()
