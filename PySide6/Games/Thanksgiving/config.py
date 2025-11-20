# config.py
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "phrases": [
        {"phrase": "A FUN FAMILY GAME", "category": "EVENT"},
        {"phrase": "GIVE THANKS", "category": "HOLIDAY"}
    ],
    "points": {chr(c): 5 for c in range(ord('A'), ord('Z')+1)},
    # default time limit (seconds)
    "time_limit": 20
}

CONFIG_FILE = Path(__file__).parent / 'game_config.json'


def load_config(path: Path = CONFIG_FILE):
    if not path.exists():
        save_config(DEFAULT_CONFIG, path)
        return DEFAULT_CONFIG
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    # validate minimal structure
    data.setdefault('phrases', [])
    data.setdefault('points', {chr(c): 5 for c in range(ord('A'), ord('Z')+1)})
    return data


def save_config(data: dict, path: Path = CONFIG_FILE):
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)