# GarudaTalon – System Monitoring (CLI)

A small, menu-driven system monitor in Python. It collects CPU, memory, and disk stats, lets you configure multiple alarms per category, and shows a live “monitoring mode” where alarms can trigger.

## Features

* Start/stop background monitoring (CPU/RAM/Disk)
* **List Active Monitoring**: snapshot of current usage
* **Configure Alarms**: multiple thresholds per type (CPU/RAM/Disk)
* **Show Alarms**: sorted, human-readable list
* **Monitoring Mode**: live view; alarms trigger here only
* JSON persistence of alarms (`data/alarms.json`)
* Per-run log file (`data/system-monitor-YYYYMMDD-HHMMSS.log`)

## Requirements

* Python 3.10+ (recommended)
* Dependencies:

  ```bash
  pip install psutil pygame colorama
  ```

> Note: On some systems, `pygame` may require SDL libraries (Linux) or extra permissions (macOS). If sound fails, alarms will still print to the console.

## Project Structure

```
.
├─ main.py              # CLI entrypoint (menus & logging)
├─ monitor.py           # background sampler & snapshot/live view
├─ alarms.py            # alarm config, checks, and monitoring-mode watcher
├─ stored_alarms.py     # JSON persistence helpers
└─ data/                # logs and alarms.json (created at runtime)
```

## Usage

1. Clone and install deps:

   ```bash
   git clone <your-repo-url>
   cd <repo>
   pip install -r requirements.txt  # if you add one, otherwise see above
   ```
2. Run:

   ```bash
   python main.py
   ```

### Menu (overview)

1. **START MONITORING** – starts background sampling (needed for snapshots).
2. **STOP MONITORING** – stops background sampling.
3. **LIST ACTIVE MONITORING** – prints a **snapshot** (if monitoring is active), then waits for Enter.
4. **CONFIGURE ALARMS** – set thresholds (1–100) for CPU/RAM/Disk; multiple per type are allowed.
5. **SHOW ALARMS** – lists all configured alarms (sorted), then waits for Enter.
6. **START MONITORING MODE** – live view; **alarms can trigger here** (sound + console). Press `Ctrl+C` to return.
7. **EXIT PROGRAM** – quit.

### Alarm Behavior (important)

* Alarms are **only evaluated** during **Monitoring Mode** (menu option 6).
* Multiple thresholds per type are supported; the **highest threshold ≤ current value** is considered the active trigger (avoids spamming lower ones).
* Alarms are stored in `data/alarms.json` and loaded at startup.

## Logs

* A new log file is created each run: `data/system-monitor-YYYYMMDD-HHMMSS.log`.
* Events like program start, menu choices, and configuration changes are appended.

## Troubleshooting

* **No sound?** Check that `pygame.mixer` can initialize; verify audio output device. The app will still print alarm warnings if audio fails.
* **No snapshot in option 3?** Make sure you started monitoring first (option 1).
* **High CPU flapping alarms?** Consider adding hysteresis or consecutive-hit logic (easy to drop in if needed).

© 2025 Mallard-Dash. All rights reserved.
