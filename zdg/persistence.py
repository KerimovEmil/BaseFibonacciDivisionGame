"""Cross-platform persistence for best scores and user preferences.

Uses ``window.localStorage`` when running under pygbag/Emscripten in the browser
and a JSON file in the user's home/config directory on desktop.
"""
import json
import os
import sys
from pathlib import Path
from zdg.settings import DEFAULT_DIFFICULTY, SOUND_ON

STORAGE_KEY = "base_fibonacci_division_save_v1"


def _default_data() -> dict:
    return {
        "best_scores": {},
        "difficulty": DEFAULT_DIFFICULTY,
        "muted": not SOUND_ON,
    }


def _desktop_save_path(custom_path=None) -> Path:
    if custom_path is not None:
        return Path(custom_path)
    env_path = os.environ.get("FIB_DIVISION_SAVE_PATH")
    if env_path:
        return Path(env_path)
    config_root = os.environ.get("XDG_CONFIG_HOME")
    if config_root:
        base = Path(config_root)
    else:
        base = Path.home() / ".config"
    return base / "fib_division" / "save.json"


def _normalize(raw) -> dict:
    data = _default_data()
    if not isinstance(raw, dict):
        return data
    scores = raw.get("best_scores")
    if isinstance(scores, dict):
        clean_scores = {}
        for k, v in scores.items():
            if isinstance(k, str) and isinstance(v, int) and v >= 0:
                clean_scores[k] = v
        data["best_scores"] = clean_scores
    diff = raw.get("difficulty")
    if isinstance(diff, str) and diff in ("Easy", "Medium", "Hard"):
        data["difficulty"] = diff
    muted = raw.get("muted")
    if isinstance(muted, bool):
        data["muted"] = muted
    return data


def load_save(path=None) -> dict:
    """Load saved best scores and preferences, falling back to defaults."""
    if sys.platform == "emscripten" and path is None:
        try:
            import platform
            raw_json = platform.window.localStorage.getItem(STORAGE_KEY)
            if raw_json:
                return _normalize(json.loads(raw_json))
        except Exception:
            pass
        return _default_data()

    try:
        target = _desktop_save_path(path)
        if target.is_file():
            with target.open("r", encoding="utf-8") as fh:
                return _normalize(json.load(fh))
    except Exception:
        pass
    return _default_data()


def save_data(data: dict, path=None) -> bool:
    """Persist best scores and preferences. Returns True on success."""
    payload = _normalize(data)
    if sys.platform == "emscripten" and path is None:
        try:
            import platform
            platform.window.localStorage.setItem(STORAGE_KEY, json.dumps(payload))
            return True
        except Exception:
            return False

    try:
        target = _desktop_save_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
        tmp.replace(target)
        return True
    except Exception:
        return False
