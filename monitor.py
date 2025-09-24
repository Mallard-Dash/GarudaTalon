# monitoring_core.py
import threading
import psutil
import time

_MONITOR_THREAD = None
_STOP_EVENT = threading.Event()
_LATEST = {} 

def _collect_loop(interval=1.0, disk_path="/"):
    psutil.cpu_percent(interval=None)

    while not _STOP_EVENT.is_set():
        cpu = psutil.cpu_percent(interval=interval) 
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
    global _MONITOR_THREAD
    if not is_monitoring_active():
        return False
    _STOP_EVENT.set()
    _MONITOR_THREAD.join(timeout=2)
    _MONITOR_THREAD = None
    return True

def is_monitoring_active():
    return _MONITOR_THREAD is not None and _MONITOR_THREAD.is_alive()

def get_status():
    if not is_monitoring_active():
        return None
    return dict(_LATEST)

def display_usage2():
    disk = psutil.disk_usage('/')
    ram  = psutil.virtual_memory()
    cpu  = psutil.cpu_percent(interval=0.5)

    total_disk_gb = disk.total / (1024**3)
    used_disk_gb  = disk.used / (1024**3)

    total_ram_gb = ram.total / (1024**3)
    used_ram_gb  = (ram.total - ram.available) / (1024**3)

    print(f"Disk-usage: {disk.percent}%  ({used_disk_gb:.0f}/{total_disk_gb:.0f} GB used)")
    print(f"RAM-usage:  {ram.percent}%  ({used_ram_gb:.0f}/{total_ram_gb:.0f} GB used)")
    print(f"CPU-usage:  {cpu:.0f}%  ")

def show_active_monitoring():
    if not is_monitoring_active():
        print("No active monitoring.")
    else:           
        print("\n\n\n")
    try:
        while True:
            print("\033[F\033[F\033[F", end="")
            display_usage2()
            time.sleep(0.2)
    except KeyboardInterrupt:
            print("\n--- Exiting to main-menu ---")
            return
