# Dumbo

Simple Wake-word and STT component.

Listens to the microphone, waits for the wake word, transcribes the command
that follows and publishes it on an MQTT topic.

## Installation

Dependencies are managed with [uv](https://docs.astral.sh/uv/). Each
transcription engine is an optional extra, install the one(s) you need:

```bash
uv sync --extra whisper                  # faster-whisper
uv sync --extra linto                    # linagora/linto_stt_fr_fastconformer (transformers + torch CPU)
uv sync --extra whisper --extra linto    # both (or --all-extras)
```

`uv sync` removes anything not requested: switching from `--extra whisper` to
`--extra linto` uninstalls faster-whisper.

## Usage

```bash
uv run main.py                         # default engine (TRANSCRIBER in consts.py)
uv run main.py --transcriber linto
```

Transcriptions are published on `MQTT_TOPIC` as JSON:

```json
{"text": "allume la lumière", "timestamp": "2026-11-25T10:32:05.123+01:00"}
```

Settings (wake word, thresholds, models, MQTT broker) are in `consts.py`.

## Managing dependencies

```bash
uv add <package>                       # core dependency
uv add --optional linto <package>      # dependency of an extra
uv remove --optional linto <package>
```

## Adding a transcription engine

1. Create `transcriber/<name>.py` with a `load()` function returning
   `transcribe(frames) -> str`.
2. Register it in `ENGINES` in `transcriber/__init__.py`.
3. Add its dependencies as an extra: `uv add --optional <name> <package>`.

## Lint

```bash
uvx ruff check --fix .
uvx ruff format .
```
