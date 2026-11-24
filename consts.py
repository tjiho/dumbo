# Audio
SAMPLE_RATE = 16000  # fréquence d'échantillonnage (Hz)
FRAME_MS = 80  # durée d'une frame (ms)
FRAME_SIZE = SAMPLE_RATE * FRAME_MS // 1000  # 1280 échantillons = 80 ms à 16 kHz

# Wakeword
WAKEWORD = "hey_mycroft"
WAKEWORD_THRESHOLD = 0.4

# Capture de la commande
PRE_FRAMES = int(1500 / FRAME_MS)  # garder ~1,5 s avant la détection
SILENCE_FRAMES = int(800 / FRAME_MS)  # 800 ms de silence = fin de commande
MAX_FRAMES = int(8000 / FRAME_MS)  # 8 s max de commande
SILENCE_THRESHOLD = 500  # RMS (int16) en dessous duquel on considère du silence

# Transcription
WHISPER_MODEL = "small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"
LANGUAGE = "fr"

# MQTT
MQTT_HOST = "10.10.10.10"
MQTT_PORT = 1883
MQTT_TOPIC = "dumbo/command"
