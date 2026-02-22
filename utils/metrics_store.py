# utils/metrics_store.py
# Thread-safe store for live metrics shared between simulation thread and Streamlit UI

import threading
from collections import deque
from typing import List, Dict, Any


class MetricsStore:
    """
    Thread-safe ring buffer for simulation metrics.
    Simulation thread writes → Streamlit UI reads.
    """

    _instance = None
    _lock      = threading.Lock()

    def __new__(cls):
        """Singleton — one store shared across all imports."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._history  = deque(maxlen=5000)
                cls._instance._summary  = {}
                cls._instance._running  = False
                cls._instance._error    = None
        return cls._instance

    # ── Write (simulation thread) ────────────────────────────────

    def append(self, record: Dict[str, Any]):
        with self._lock:
            self._history.append(record)

    def set_summary(self, summary: dict):
        with self._lock:
            self._summary = summary

    def set_running(self, running: bool):
        with self._lock:
            self._running = running

    def set_error(self, error: str):
        with self._lock:
            self._error = error

    def reset(self):
        with self._lock:
            self._history.clear()
            self._summary = {}
            self._running = False
            self._error   = None

    # ── Read (Streamlit UI thread) ───────────────────────────────

    def get_history(self) -> List[Dict]:
        with self._lock:
            return list(self._history)

    def get_summary(self) -> dict:
        with self._lock:
            return dict(self._summary)

    def is_running(self) -> bool:
        with self._lock:
            return self._running

    def get_error(self):
        with self._lock:
            return self._error

    def latest(self) -> dict:
        with self._lock:
            return self._history[-1] if self._history else {}


# Global singleton instance
metrics_store = MetricsStore()
