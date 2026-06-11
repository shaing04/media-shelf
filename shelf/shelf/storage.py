import json
from pathlib import Path

DATA_DIR = Path.home() / ".shelf"
DATA_FILE = DATA_DIR / "data.json"


def _ensure_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]")


def load() -> list[dict]:
    _ensure_file()
    return json.loads(DATA_FILE.read_text())


def save(entries: list[dict]) -> None:
    _ensure_file()
    DATA_FILE.write_text(json.dumps(entries, indent=2))


def next_id(entries: list[dict]) -> int:
    return max((e["id"] for e in entries), default=0) + 1
