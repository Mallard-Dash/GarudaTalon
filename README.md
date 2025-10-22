# GarudaTalon

This is a command-line application for monitoring your system's CPU, RAM, and Disk usage in real-time. It allows you to set, save, and manage custom percentage-based alarms that trigger when a resource exceeds its configured threshold.

## Features

* **Live Monitoring:** View real-time CPU, RAM, and Disk usage statistics.
* **Custom Alarms:** Set custom alarms for CPU, RAM, or Disk (e.g., "trigger if CPU > 90%").
* **Persistent Alarms:** Your alarm configurations are saved to `Active_alarms.json` and are reloaded every time you start the app.
* **Arm/Disarm System:** The live monitoring view only checks for alarms when the system is "Armed," allowing you to configure alarms without triggering them.
* **Event Logging:** All major actions (app start, alarm set, alarm triggered, user menu choices) are logged to a timestamped `.jsonl` file (e.g., `log_2023-10-22_10-30-00.jsonl`) for each session.
* **Colored Output:** Uses `colorama` for easy-to-read, colored console output.

## Usage

To run the application, simply execute the `main.py` file:

```bash
python main.py

© 2025 Mallard-Dash. All rights reserved.
