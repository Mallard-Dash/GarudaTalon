# monitoring_core.py
import threading
import psutil
import time

# --- Globalt state (enkelt & tydligt) ---
_MONITOR_THREAD = None
_STOP_EVENT = threading.Event()
_LATEST = {}  # fylls av bakgrundsloopen

def _collect_loop(interval=1.0, disk_path="/"):
    # Initiera första mätningen så inte första CPU blir 0
    psutil.cpu_percent(interval=None)

    while not _STOP_EVENT.is_set():
        cpu = psutil.cpu_percent(interval=interval)  # blockar 'interval' sekunder
        vm  = psutil.virtual_memory()
        du  = psutil.disk_usage(disk_path)

        _LATEST.update({
            "cpu_percent": cpu,
            "ram_percent": vm.percent,
            "ram_used_gb": (vm.total - vm.available) / (1024**3),
            "ram_total_gb": vm.total / (1024**3),
            "disk_percent": du.percent,
            "disk_used_gb": du.used / (1024**3),
            "disk_total_gb": du.total / (1024**3),
        })

def start_monitoring(interval=1.0, disk_path="/"):
    """Starta övervakning (gör inget om den redan är igång)."""
    global _MONITOR_THREAD
    if is_monitoring_active():
        return False
    _STOP_EVENT.clear()
    _MONITOR_THREAD = threading.Thread(
        target=_collect_loop, args=(interval, disk_path), daemon=True
    )
    _MONITOR_THREAD.start()
    return True

def stop_monitoring():
    """Stoppa övervakningen om den är igång."""
    global _MONITOR_THREAD
    if not is_monitoring_active():
        return False
    _STOP_EVENT.set()
    _MONITOR_THREAD.join(timeout=2)
    _MONITOR_THREAD = None
    return True

def is_monitoring_active():
    """True om bakgrundstråden kör."""
    return _MONITOR_THREAD is not None and _MONITOR_THREAD.is_alive()

def get_status():
    """Returnera senaste mätningen (dict) eller None om inte aktiv."""
    if not is_monitoring_active():
        return None
    return dict(_LATEST)

def show_active_monitoring():
    if not is_monitoring_active():
        print("Ingen övervakning är aktiv.")
    else:
        s = get_status()
        print(f"CPU Användning: {s['cpu_percent']:.0f}%")
        print(f"Minnesanvändning: {s['ram_percent']:.0f}% "
              f"({s['ram_used_gb']:.1f} GB out of {s['ram_total_gb']:.1f} GB used)")
        print(f"Diskanvändning: {s['disk_percent']:.0f}% "
              f"({s['disk_used_gb']:.0f} GB out of {s['disk_total_gb']:.0f} GB used)")
    input("\nTryck Enter för att gå tillbaka till huvudmenyn...")
