GarudaTalon System Monitor
GarudaTalon is a lightweight, terminal-based system resource monitor written in Python. It allows you to track CPU, RAM, and disk usage in real-time and configure custom alarms that trigger when usage exceeds a specified threshold.

Features
Live Resource Monitoring: Get a real-time overview of your CPU, RAM, and Disk usage directly in your terminal.

Configurable Alarms: Easily add, view, and remove alarms based on percentage thresholds for each system resource.

Persistent Configuration: Your alarm settings are saved in an active_alarms.json file and automatically loaded every time you start the application.

Session-Based Logging: Each session creates a unique, timestamped log file (.jsonl format) to record user actions and triggered alarms.

Interactive CLI: A simple and intuitive command-line menu for easy navigation and control.

Colored Output: Uses colorama for a more readable and visually appealing interface.

Installation & Usage
Prerequisites
Python 3.8 or newer.

pip (Python package installer).

1. Clone the Repository
First, clone this repository to your local machine.

Bash

git clone <your-repository-url>
cd GarudaTalon
2. Create a requirements.txt file
Create a file named requirements.txt in the project's root directory and add the following lines to it:

Plaintext

psutil
colorama
3. Install Dependencies
Install the required Python libraries using the requirements.txt file.

Bash

pip install -r requirements.txt
4. Run the Application
Start the program by running the main.py script.

Bash

python main.py
You will be greeted by the main menu, where you can start monitoring, configure alarms, or view the live overview.

How It Works
The application is split into three main logical components:

main.py: This is the main entry point of the application. It handles the user menu, the main monitoring loop, and coordinates the other modules.

configurations.py: This module manages all aspects of the alarms. It handles creating, saving, loading, removing, and checking alarm thresholds against current system values.

metric_data.py: This module is responsible for fetching the raw system resource data (CPU, RAM, Disk) using the psutil library.

File Generation
When you run the program, it will create two types of files in the project directory:

active_alarms.json: A single file that stores all your alarm configurations. This file persists between sessions.

log_YYYY-MM-DD_HH-MM-SS.jsonl: A new log file is created for each session you start. It records menu choices, actions, and any alarms that are triggered.

© 2025 Mallard-Dash. All rights reserved.
