import os
import json
from typing import List, Dict, Any
from colorama import init
init(autoreset=True)

APP_DIR = os.path.join(os.getcwd(), "data")
ALARM_FILE = os.path.join(APP_DIR, "alarms.json")
os.makedirs(APP_DIR, exist_ok=True)

def _load_json() -> List[Dict[str, Any]]:
    if not os.path.exists(ALARM_FILE):
        return []
    try:
        with open(ALARM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                cleaned = []
                for item in data:
                    if not isinstance(item, dict):
                        continue
                    kind = item.get("kind")
                    thr  = item.get("threshold")
                    en   = item.get("enabled", True)
                    if kind in {"cpu", "ram", "disk"} and isinstance(thr, (int, float)):
                        cleaned.append({"kind": kind, "threshold": float(thr), "enabled": bool(en)})
                return cleaned
            return []
    except Exception:
        return []

def _save_json(alarms: List[Dict[str, Any]]) -> None:
    with open(ALARM_FILE, "w", encoding="utf-8") as f:
        json.dump(alarms, f, ensure_ascii=False, indent=2)

def load_alarms() -> List[Dict[str, Any]]:
    return _load_json()

def save_alarms(alarms: List[Dict[str, Any]]) -> None:
    _save_json(alarms)

def add_alarm(alarms: List[Dict[str, Any]], kind: str, threshold: float, enabled: bool = True) -> None:
    alarms.append({"kind": kind, "threshold": float(threshold), "enabled": bool(enabled)})
    _save_json(alarms)

def remove_alarm_by_index(alarms: List[Dict[str, Any]], index: int) -> bool:
    if 0 <= index < len(alarms):
        alarms.pop(index)
        _save_json(alarms)
        return True
    return False

def list_alarms_human(alarms: List[Dict[str, Any]]) -> List[str]:
    # sort by kind (cpu, disk, ram) and then threshold ascending
    order = {"cpu": 0, "disk": 1, "ram": 2}
    sorted_alarms = sorted(
        alarms,
        key=lambda a: (order.get(a["kind"], 99), a["threshold"])
    )
    out = []
    for a in sorted_alarms:
        kind = a["kind"]; thr = a["threshold"]
        if kind == "cpu":
            label = f"CPU threshold {int(thr)}%"
        elif kind == "ram":
            label = f"RAM threshold {int(thr)}%"
        else:
            label = f"Disk threshold {int(thr)}%"
        out.append(label)
    return out
