# utils/helpers.py

import os
import json
import numpy as np
from datetime import datetime


def ensure_dir(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def timestamp() -> str:
    """Returns current timestamp string for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def safe_divide(numerator: float, denominator: float, fallback: float = 0.0) -> float:
    """Division that returns fallback instead of ZeroDivisionError."""
    return numerator / denominator if denominator != 0 else fallback


def clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp integer between min and max."""
    return max(min_val, min(value, max_val))


def save_json(data: dict, filepath: str):
    """Save dict as JSON file."""
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_json(filepath: str) -> dict:
    """Load JSON file as dict."""
    with open(filepath, "r") as f:
        return json.load(f)


def format_seconds(seconds: float) -> str:
    """Convert seconds to mm:ss string."""
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"
