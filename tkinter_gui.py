#!/usr/bin/env python3
# Garuda Talon v2.2 — Tkinter GUI with visual alarm states (fixed metric_cards init order)

import tkinter as tk
from tkinter import ttk, messagebox
import os, datetime

import monitor
import alarms
from stored_alarms import load_alarms, save_alarms, add_alarm, remove_alarm_by_index, list_alarms_human

APP_TITLE = "Garuda Talon v2.2"
APP_SIZE  = "1000x700"
APP_DIR   = os.path.join(os.getcwd(), "data")
os.makedirs(APP_DIR, exist_ok=True)

def _logfile_path():
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return os.path.join(APP_DIR, f"system-monitor-{ts}.log")

LOG_FILE = _logfile_path()

def _timestamp_swe() -> str:
    now = datetime.datetime.now()
    return f"{now.day}/{now.month}/{now.year}_{now.strftime('%H:%M')}"

def log_event(*parts: str) -> None:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    clean_parts = [str(p).replace(" ", "_") for p in parts]
    line = f"{_timestamp_swe()}_{'_'.join(clean_parts)}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

KIND_LABEL = {"cpu": "CPU", "ram": "RAM", "disk": "DISK"}
KINDS = ("cpu", "ram", "disk")

def _sync_alarm_ON_from_storage():
    """Enable alarms.ON[k] if any enabled alarm of that kind exists in storage."""
    data = load_alarms()
    kinds_enabled = {a["kind"] for a in data if a.get("enabled", True)}
    for k in KINDS:
        alarms.ON[k] = (k in kinds_enabled)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.minsize(900, 600)

        # ---- app state ----
        self.is_monitoring = tk.BooleanVar(value=False)
        self.fast_mode     = tk.BooleanVar(value=False)
        self.status_text   = tk.StringVar(value="Ready.")

        # IMPORTANT: initialize metric_cards BEFORE creating frames
        self.metric_cards: dict[str, "AlarmCard"] = {}

        self._build_menu()

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (MainMenu, MonitorView, AlarmConfig, AlarmList):
            frame = Page(parent=container, controller=self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self._build_statusbar()
        self.show_frame("MainMenu")

        self._tick()

    # ---------- chrome ----------
    def _build_menu(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Main menu", command=lambda: self.show_frame("MainMenu"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        monmenu = tk.Menu(menubar, tearoff=0)
        monmenu.add_command(label="Start monitoring", command=self.start_monitoring)
        monmenu.add_command(label="Stop monitoring",  command=self.stop_monitoring)
        monmenu.add_command(label="Monitoring view",  command=lambda: self.show_frame("MonitorView"))
        monmenu.add_separator()
        monmenu.add_checkbutton(label="Monitoring mode (faster refresh)",
                                variable=self.fast_mode, onvalue=True, offvalue=False)
        menubar.add_cascade(label="Monitor", menu=monmenu)

        alarmmenu = tk.Menu(menubar, tearoff=0)
        alarmmenu.add_command(label="Configure alarms", command=lambda: self.show_frame("AlarmConfig"))
        alarmmenu.add_command(label="Show alarms",      command=lambda: self.show_frame("AlarmList"))
        menubar.add_cascade(label="Alarms", menu=alarmmenu)

        self.config(menu=menubar)

    def _build_statusbar(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", side="bottom")
        ttk.Label(bar, textvariable=self.status_text, anchor="w").pack(fill="x", padx=8, pady=4)

    def show_frame(self, name: str):
        self.frames[name].tkraise()
        self.status_text.set(f"Showing: {name}")

    # ---------- monitor control ----------
    def start_monitoring(self):
        log_event("Monitoring_started")
        ok = monitor.start_monitoring(interval=0.5, disk_path="/")
        _sync_alarm_ON_from_storage()
        try:
            alarms.start_alarm_watcher(poll_s=0.5)
        except Exception as e:
            print(f"[alarm watcher warn] {e}")
        self.is_monitoring.set(True)
        self.status_text.set("Monitoring started." if ok else "Monitoring already running.")

    def stop_monitoring(self):
        log_event("Monitoring_stopped")
        try:
            alarms.stop_alarm_watcher()
        except Exception:
            pass
        ok = monitor.stop_monitoring()
        self.is_monitoring.set(False)
        self.status_text.set("Monitoring stopped." if ok else "Monitoring not active.")
        for card in self.metric_cards.values():
            card.set_normal()
            card.set_value("—")

    def list_active_monitoring_text(self) -> str:
        st = monitor.get_status()
        if not st:
            return "No active tasks"
        return (f"CPU {st['cpu_percent']:.1f}%, "
                f"RAM {st['ram_percent']:.1f}% ({st['ram_used_gb']:.1f}/{st['ram_total_gb']:.1f} GB), "
                f"DISK {st['disk_percent']:.1f}% ({st['disk_used_gb']:.1f}/{st['disk_total_gb']:.1f} GB)")

    # ---------- alarms storage helpers ----------
    def save_alarm_config_replace(self, cfg: dict):
        cur = [a for a in load_alarms() if a.get("kind") not in KINDS]
        to_add = []
        for k in KINDS:
            thr = cfg.get(k)
            if isinstance(thr, (int, float)):
                to_add.append({"kind": k, "threshold": float(thr), "enabled": True})
        save_alarms(cur + to_add)
        _sync_alarm_ON_from_storage()

    def add_single_alarm(self, kind: str, thr: float):
        a = load_alarms()
        add_alarm(a, kind=kind, threshold=float(thr), enabled=True)
        _sync_alarm_ON_from_storage()

    def set_alarm_enabled(self, orig_index: int, enabled: bool):
        a = load_alarms()
        if 0 <= orig_index < len(a):
            a[orig_index]["enabled"] = bool(enabled)
            save_alarms(a)
        _sync_alarm_ON_from_storage()

    def remove_alarm_orig_index(self, orig_index: int) -> bool:
        a = load_alarms()
        ok = remove_alarm_by_index(a, orig_index)
        _sync_alarm_ON_from_storage()
        return ok

    # ---------- heartbeat ----------
    def _tick(self):
        try:
            self._poll_metrics_and_alarms()
        finally:
            delay = 200 if (self.fast_mode.get() and self.is_monitoring.get()) else 600
            self.after(delay, self._tick)

    def _poll_metrics_and_alarms(self):
        st = monitor.get_status()
        if st:
            if "cpu" in self.metric_cards:
                self.metric_cards["cpu"].set_value(f"{st['cpu_percent']:.1f} %")
            if "ram" in self.metric_cards:
                self.metric_cards["ram"].set_value(f"{st['ram_percent']:.1f} %  ({st['ram_used_gb']:.1f}/{st['ram_total_gb']:.1f} GB)")
            if "disk" in self.metric_cards:
                self.metric_cards["disk"].set_value(f"{st['disk_percent']:.1f} %  ({st['disk_used_gb']:.1f}/{st['disk_total_gb']:.1f} GB)")
        else:
            for card in self.metric_cards.values():
                if self.is_monitoring.get():
                    card.set_value("…")

        for kind in KINDS:
            card = self.metric_cards.get(kind)
            if not card:
                continue
            if alarms.OVER.get(kind, False):
                card.set_alarm(f"Warning {KIND_LABEL[kind]} has triggered an alarm")
            else:
                card.set_normal()

    def on_exit(self):
        log_event("Program_shutting_down")
        try: alarms.stop_alarm_watcher()
        except Exception: pass
        try: monitor.stop_monitoring()
        except Exception: pass
        self.destroy()

# -------------------- pages --------------------

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Garuda Talon — Main menu", font=("Segoe UI", 18, "bold"))\
            .pack(pady=(24, 12))

        grid = ttk.Frame(self); grid.pack(pady=12, padx=10)
        ttk.Button(grid, text="Start monitoring", command=controller.start_monitoring)\
            .grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(grid, text="Stop monitoring", command=controller.stop_monitoring)\
            .grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(grid, text="Monitoring view", command=lambda: controller.show_frame("MonitorView"))\
            .grid(row=1, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(grid, text="Configure alarms", command=lambda: controller.show_frame("AlarmConfig"))\
            .grid(row=1, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(grid, text="Show alarms", command=lambda: controller.show_frame("AlarmList"))\
            .grid(row=2, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(grid, text="Exit", command=controller.on_exit)\
            .grid(row=2, column=1, padx=6, pady=6, sticky="ew")

        for c in range(2):
            grid.grid_columnconfigure(c, weight=1)

        self.active_lbl = ttk.Label(self, text="", foreground="#777")
        self.active_lbl.pack(pady=(8, 2))

        ttk.Button(self, text="List active monitoring (snapshot)",
                   command=self._refresh_active).pack()

        box = ttk.Frame(self); box.pack(pady=10)
        ttk.Checkbutton(box, text="Monitoring mode (faster refresh)",
                        variable=controller.fast_mode).pack()

    def _refresh_active(self):
        self.active_lbl.config(text=self.controller.list_active_monitoring_text())

class MonitorView(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        header = ttk.Frame(self); header.pack(fill="x", pady=(20, 8))
        ttk.Label(header, text="Monitoring", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)

        controls = ttk.Frame(self); controls.pack(fill="x", padx=10)
        ttk.Button(controls, text="Start", command=controller.start_monitoring).pack(side="left", padx=4)
        ttk.Button(controls, text="Stop",  command=controller.stop_monitoring).pack(side="left", padx=4)
        ttk.Button(controls, text="Back to menu", command=lambda: controller.show_frame("MainMenu")).pack(side="left", padx=4)

        cards = ttk.Frame(self); cards.pack(expand=True, fill="both", padx=10, pady=10)

        cpu_card  = AlarmCard(cards, title="CPU")
        ram_card  = AlarmCard(cards, title="RAM")
        disk_card = AlarmCard(cards, title="DISK")

        cpu_card.grid (row=0, column=0, padx=8, pady=8, sticky="nsew")
        ram_card.grid (row=0, column=1, padx=8, pady=8, sticky="nsew")
        disk_card.grid(row=0, column=2, padx=8, pady=8, sticky="nsew")

        for i in range(3):
            cards.grid_columnconfigure(i, weight=1)
        cards.grid_rowconfigure(0, weight=1)

        # now safe: controller.metric_cards exists
        controller.metric_cards["cpu"]  = cpu_card
        controller.metric_cards["ram"]  = ram_card
        controller.metric_cards["disk"] = disk_card

class AlarmCard(tk.Frame):
    COLOR_BG_NORMAL = "#1f2937"   # slate-800
    COLOR_FG_NORMAL = "#e5e7eb"   # gray-200
    COLOR_BG_ALARM  = "#7f1d1d"   # red-900
    COLOR_FG_ALARM  = "#ffffff"

    def __init__(self, parent, title: str):
        super().__init__(parent, bd=1, relief="groove", bg=self.COLOR_BG_NORMAL)
        self.title = title

        self.title_lbl = tk.Label(self, text=title, font=("Segoe UI", 12, "bold"),
                                  bg=self.COLOR_BG_NORMAL, fg=self.COLOR_FG_NORMAL)
        self.title_lbl.pack(anchor="w", padx=12, pady=(12, 0))

        self.value_lbl = tk.Label(self, text="—", font=("Consolas", 22),
                                  bg=self.COLOR_BG_NORMAL, fg=self.COLOR_FG_NORMAL)
        self.value_lbl.pack(anchor="center", pady=(10, 6))

        self.warn_lbl = tk.Label(self, text="", font=("Segoe UI", 12, "bold"),
                                 bg=self.COLOR_BG_NORMAL, fg=self.COLOR_FG_NORMAL, wraplength=280, justify="center")
        self.warn_lbl.pack(anchor="center", pady=(6, 12))

        self.pad = tk.Frame(self, bg=self.COLOR_BG_NORMAL)
        self.pad.pack(expand=True, fill="both", padx=10, pady=8)

        self._alarm_on = False

    def set_value(self, text: str):
        self.value_lbl.config(text=text)

    def set_alarm(self, message: str):
        if not self._alarm_on:
            self._set_colors(self.COLOR_BG_ALARM, self.COLOR_FG_ALARM)
            self._alarm_on = True
        self.warn_lbl.config(text=message)

    def set_normal(self):
        if self._alarm_on:
            self._set_colors(self.COLOR_BG_NORMAL, self.COLOR_FG_NORMAL)
            self._alarm_on = False
        self.warn_lbl.config(text="")

    def _set_colors(self, bg, fg):
        self.config(bg=bg)
        for w in (self.title_lbl, self.value_lbl, self.warn_lbl, self.pad):
            try:
                w.config(bg=bg, fg=fg)
            except tk.TclError:
                pass

class AlarmConfig(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Configure alarms", font=("Segoe UI", 16, "bold"))\
            .pack(anchor="w", padx=10, pady=(18, 8))

        wrap = ttk.Frame(self); wrap.pack(fill="x", padx=10)

        left = ttk.LabelFrame(wrap, text="Quick replace (one per kind)")
        left.pack(side="left", padx=6, pady=6, fill="both", expand=True)

        self.cpu_thr  = tk.IntVar(value=80)
        self.ram_thr  = tk.IntVar(value=80)
        self.disk_thr = tk.IntVar(value=90)

        self._row(left, "CPU threshold (%)",  self.cpu_thr)
        self._row(left, "RAM threshold (%)",  self.ram_thr)
        self._row(left, "DISK threshold (%)", self.disk_thr)
        ttk.Button(left, text="Save/Replace", command=self._save_replace).pack(pady=6)

        mid = ttk.LabelFrame(wrap, text="Add another threshold")
        mid.pack(side="left", padx=6, pady=6, fill="both", expand=True)

        self.add_kind = tk.StringVar(value="cpu")
        self.add_thr  = tk.IntVar(value=75)
        r1 = ttk.Frame(mid); r1.pack(pady=6, fill="x")
        ttk.Label(r1, text="Kind", width=10).pack(side="left")
        ttk.OptionMenu(r1, self.add_kind, "cpu", *KINDS).pack(side="left")
        r2 = ttk.Frame(mid); r2.pack(pady=6, fill="x")
        ttk.Label(r2, text="Threshold (%)", width=14).pack(side="left")
        ttk.Spinbox(r2, from_=1, to=100, textvariable=self.add_thr, width=6).pack(side="left")
        ttk.Button(mid, text="Add", command=self._add_alarm).pack(pady=6)

        right = ttk.LabelFrame(wrap, text="Current alarms")
        right.pack(side="left", padx=6, pady=6, fill="both", expand=True)

        self.listbox = tk.Listbox(right, height=14)
        self.listbox.pack(fill="both", expand=True, padx=6, pady=6)

        btns = ttk.Frame(right); btns.pack(fill="x", padx=6, pady=(0,8))
        ttk.Button(btns, text="Enable", command=lambda: self._set_selected(True)).pack(side="left", padx=3)
        ttk.Button(btns, text="Disable", command=lambda: self._set_selected(False)).pack(side="left", padx=3)
        ttk.Button(btns, text="Remove", command=self._remove_selected).pack(side="left", padx=3)
        ttk.Button(btns, text="Refresh", command=self._refresh).pack(side="left", padx=3)
        ttk.Button(btns, text="Back", command=lambda: controller.show_frame("MainMenu")).pack(side="right", padx=3)

        self._refresh()

    def _row(self, parent, label, var):
        r = ttk.Frame(parent); r.pack(fill="x", pady=4)
        ttk.Label(r, text=label, width=20).pack(side="left")
        ttk.Spinbox(r, from_=1, to=100, textvariable=var, width=6).pack(side="left")

    def _save_replace(self):
        cfg = {"cpu": int(self.cpu_thr.get()), "ram": int(self.ram_thr.get()), "disk": int(self.disk_thr.get())}
        self.controller.save_alarm_config_replace(cfg)
        messagebox.showinfo("Alarms", "Replaced thresholds (one per kind) and enabled them.")
        self._refresh()

    def _add_alarm(self):
        try:
            kind = self.add_kind.get()
            thr  = int(self.add_thr.get())
            assert kind in KINDS and 1 <= thr <= 100
        except Exception:
            messagebox.showerror("Invalid", "Choose kind cpu/ram/disk and threshold between 1–100.")
            return
        self.controller.add_single_alarm(kind, thr)
        self._refresh()

    def _refresh(self):
        self.listbox.delete(0, tk.END)
        lines = list_alarms_human(load_alarms())
        if not lines:
            self.listbox.insert(tk.END, "No configured alarms.")
        else:
            for line in lines:
                self.listbox.insert(tk.END, line)

    def _get_selected_orig_index(self):
        storage = load_alarms()
        items = list(enumerate(storage))
        order = {"cpu": 0, "disk": 1, "ram": 2}
        items.sort(key=lambda pair: (order.get(pair[1].get("kind"), 99), pair[1].get("threshold", 0)))
        sel = self.listbox.curselection()
        if not sel:
            return None
        idx = sel[0]
        if idx >= len(items): return None
        return items[idx][0]

    def _set_selected(self, enabled: bool):
        orig = self._get_selected_orig_index()
        if orig is None:
            messagebox.showwarning("Select", "Select an alarm first.")
            return
        self.controller.set_alarm_enabled(orig, enabled)
        self._refresh()

    def _remove_selected(self):
        orig = self._get_selected_orig_index()
        if orig is None:
            messagebox.showwarning("Select", "Select an alarm first.")
            return
        ok = self.controller.remove_alarm_orig_index(orig)
        if not ok:
            messagebox.showerror("Error", "Failed to remove alarm.")
        self._refresh()

class AlarmList(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Alarms", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=10, pady=(18, 8))

        self.listbox = tk.Listbox(self, height=16)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        btns = ttk.Frame(self); btns.pack(fill="x", padx=10, pady=8)
        ttk.Button(btns, text="Refresh", command=self.refresh).pack(side="left")
        ttk.Button(btns, text="Back", command=lambda: controller.show_frame("MainMenu")).pack(side="left", padx=6)

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        lines = list_alarms_human(load_alarms())
        if not lines:
            self.listbox.insert(tk.END, "No configured alarms.")
        else:
            for line in lines:
                self.listbox.insert(tk.END, line)

# -------------- entry --------------
if __name__ == "__main__":
    log_event("Program_started_GUI")
    app = App()
    app.mainloop()
