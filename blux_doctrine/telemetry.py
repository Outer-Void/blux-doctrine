"""Best-effort telemetry sink for doctrine evaluations."""
from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import Any, Dict


class TelemetryLogger:
    """Append-only JSONL logger that never raises."""

    def __init__(self) -> None:
        self.enabled = os.getenv("BLUX_DOCTRINE_TELEMETRY", "on").lower() != "off"
        self.warn_once = os.getenv("BLUX_DOCTRINE_TELEMETRY_WARN", "never").lower() == "once"
        self._warned = False
        self.lock = Lock()
        self.base_path = Path(os.getenv("BLUX_DOCTRINE_HOME", "~/.config/blux-doctrine")).expanduser()
        self.log_path = self.base_path / "logs" / "audit.jsonl"

    def record(self, event: str, payload: Dict[str, Any]) -> None:
        if not self.enabled:
            return

        entry = {"event": event, **payload}
        try:
            with self.lock:
                self.log_path.parent.mkdir(parents=True, exist_ok=True)
                with self.log_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(entry) + "\n")
        except OSError:
            if self.warn_once and not self._warned:
                self._warned = True
                print("[blux-doctrine] telemetry disabled: cannot write to log path", flush=True)
