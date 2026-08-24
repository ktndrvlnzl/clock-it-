import tkinter as tk
from tkinter import messagebox
import json
import os
import datetime


# ============================================================
# CLOCK IT!
# Simple Pomodoro Timer
# Python + tkinter
# ============================================================

APP_NAME = "Clock It!"
DATA_FILE = "clock_it_data.json"

FOCUS = "Focus"
SHORT_BREAK = "Short Break"
LONG_BREAK = "Long Break"


# ============================================================
# DEFAULT SETTINGS
# ============================================================

DEFAULT_SETTINGS = {
    "focus_minutes": 25,
    "short_break_minutes": 5,
    "long_break_minutes": 15,
    "sessions_before_long_break": 4,
    "sound": "Classic Beep",
    "theme": "light"
}


# ============================================================
# COLORS
# ============================================================

THEMES = {
    "light": {
        "background": "#F5EDE7",
        "card": "#FFF8F2",
        "text": "#33262B",
        "muted": "#8B7680",
        "pink": "#D98C9A",
        "timer": "#C97878",
        "lavender": "#B9A7D8",
        "green": "#9CAF9A",
        "white": "#FFFFFF"
    },

    "dark": {
        "background": "#1F1B1D",
        "card": "#292326",
        "text": "#F7F0ED",
        "muted": "#B9AAAE",
        "pink": "#D98C9A",
        "timer": "#C97878",
        "lavender": "#B9A7D8",
        "green": "#9CAF9A",
        "white": "#FFFFFF"
    }
}


SOUND_OPTIONS = [
    "Classic Beep",
    "Double Beep",
    "Chime",
    "None"
]


# ============================================================
# APPLICATION
# ============================================================

class ClockIt(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("440x650")

        self.mode = FOCUS
        self.running = False
        self.after_id = None

        self.completed_sessions = 0

        self.task = tk.StringVar()

        self.settings = DEFAULT_SETTINGS.copy()
        self.history = []

        self.load_data()

        self.remaining_seconds = self.get_mode_seconds()

        self.build_main_screen()
        self.apply_theme()
        self.update_screen()


    # ========================================================
    # DATA
    # ========================================================

    def load_data(self):

        if not os.path.exists(DATA_FILE):
            return

        try:
            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            self.settings.update(
                data.get("settings", {})
            )

            self.history = data.get(
                "history",
                []
            )

        except Exception:
            self.settings = DEFAULT_SETTINGS.copy()
            self.history = []


    def save_data(self):

        data = {
            "settings": self.settings,
            "history": self.history
        }

        try:
            with open(
                DATA_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=2
                )

        except Exception:
            pass


    # ========================================================
    # MAIN SCREEN
    # ========================================================

    def build_main_screen(self):

        # Top bar
        self.top_bar = tk.Frame(self)

        self.top_bar.pack(
            fill="x",
            padx=24,
            pady=(20, 0)
        )


        self.title_label = tk.Label(
            self.top_bar,
            text="Clock It!",
            font=("Helvetica", 21, "bold")
        )

        self.title_label.pack(
            side="left"
        )


        self.theme_button = tk.Button(
            self.top_bar,
            text="Theme",
            relief="flat",
            borderwidth=0,
            command=self.toggle_theme,
            cursor="hand2"
        )

        self.theme_button.pack(
            side="right"
        )


        self.stats_button = tk.Button(
            self.top_bar,
            text="Stats",
            relief="flat",
            borderwidth=0,
            command=self.open_stats,
            cursor="hand2"
        )

        self.stats_button.pack(
            side="right",
            padx=(0, 8)
        )


        self.settings_button = tk.Button(
            self.top_bar,
            text="Settings",
            relief="flat",
            borderwidth=0,
            command=self.open_settings,
            cursor="hand2"
        )

        self.settings_button.pack(
            side="right",
            padx=(0, 8)
        )


        # Mode
        self.mode_label = tk.Label(
            self,
            text="FOCUS",
            font=("Helvetica", 14, "bold")
        )

        self.mode_label.pack(
            pady=(45, 5)
        )


        # Timer
        self.timer_label = tk.Label(
            self,
            text="25:00",
            font=("Helvetica", 64, "bold")
        )

        self.timer_label.pack(
            pady=(0, 5)
        )


        # Task
        self.task_prompt = tk.Label(
            self,
            text="What are you working on?",
            font=("Helvetica", 10)
        )

        self.task_prompt.pack(
            pady=(15, 5)
        )


        self.task_entry = tk.Entry(
            self,
            textvariable=self.task,
            font=("Helvetica", 11),
            justify="center"
        )

        self.task_entry.pack(
            padx=55,
            fill="x",
            ipady=7
        )


        # Controls
        self.control_frame = tk.Frame(self)

        self.control_frame.pack(
            pady=25
        )


        self.start_button = tk.Button(
            self.control_frame,
            text="Start",
            width=12,
            font=("Helvetica", 11, "bold"),
            command=self.start_timer,
            cursor="hand2"
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=5
        )


        self.pause_button = tk.Button(
            self.control_frame,
            text="Pause",
            width=8,
            command=self.pause_timer,
            cursor="hand2"
        )

        self.pause_button.grid(
            row=0,
            column=1,
            padx=5
        )


        self.reset_button = tk.Button(
            self.control_frame,
            text="Reset",
            width=8,
            command=self.reset_timer,
            cursor="hand2"
        )

        self.reset_button.grid(
            row=0,
            column=2,
            padx=5
        )


        self.skip_button = tk.Button(
            self.control_frame,
            text="Skip",
            width=8,
            command=self.skip_timer,
            cursor="hand2"
        )

        self.skip_button.grid(
            row=0,
            column=3,
            padx=5
        )


        # Session counter
        self.session_label = tk.Label(
            self,
            text="Session 1 / 4",
            font=("Helvetica", 11)
        )

        self.session_label.pack(
            pady=(0, 22)
        )


        # Mode buttons
        self.mode_frame = tk.Frame(self)

        self.mode_frame.pack()


        self.focus_button = tk.Button(
            self.mode_frame,
            text="Focus",
            width=12,
            command=lambda: self.change_mode(FOCUS),
            cursor="hand2"
        )

        self.focus_button.grid(
            row=0,
            column=0,
            padx=3
        )


        self.short_button = tk.Button(
            self.mode_frame,
            text="Short Break",
            width=12,
            command=lambda: self.change_mode(SHORT_BREAK),
            cursor="hand2"
        )

        self.short_button.grid(
            row=0,
            column=1,
            padx=3
        )


        self.long_button = tk.Button(
            self.mode_frame,
            text="Long Break",
            width=12,
            command=lambda: self.change_mode(LONG_BREAK),
            cursor="hand2"
        )

        self.long_button.grid(
            row=0,
            column=2,
            padx=3
        )


    # ========================================================
    # TIMER
    # ========================================================

    def get_mode_seconds(self):

        if self.mode == FOCUS:
            return self.settings["focus_minutes"] * 60

        if self.mode == SHORT_BREAK:
            return self.settings["short_break_minutes"] * 60

        return self.settings["long_break_minutes"] * 60


    def start_timer(self):

        if self.running:
            return

        self.running = True

        self.start_button.config(
            state="disabled"
        )

        self.tick()


    def tick(self):

        if not self.running:
            return

        self.update_screen()

        if self.remaining_seconds <= 0:
            self.finish_timer()
            return

        self.remaining_seconds -= 1

        self.after_id = self.after(
            1000,
            self.tick
        )


    def pause_timer(self):

        self.running = False

        if self.after_id is not None:

            try:
                self.after_cancel(
                    self.after_id
                )
            except Exception:
                pass

            self.after_id = None

        self.start_button.config(
            state="normal"
        )


    def reset_timer(self):

        self.pause_timer()

        self.remaining_seconds = (
            self.get_mode_seconds()
        )

        self.update_screen()


    def skip_timer(self):

        self.pause_timer()

        if self.mode == FOCUS:
            self.go_to_next_break()
        else:
            self.change_mode(FOCUS)


    def finish_timer(self):

        self.running = False
        self.after_id = None

        self.start_button.config(
            state="normal"
        )

        finished_mode = self.mode

        self.save_history(
            finished_mode
        )

        self.play_sound()

        if finished_mode == FOCUS:

            self.completed_sessions += 1

            sessions_needed = (
                self.settings[
                    "sessions_before_long_break"
                ]
            )

            if (
                self.completed_sessions
                % sessions_needed
                == 0
            ):
                next_mode = LONG_BREAK
            else:
                next_mode = SHORT_BREAK

        else:

            next_mode = FOCUS

        self.change_mode(
            next_mode
        )

        messagebox.showinfo(
            "Clock It!",
            finished_mode + " finished!"
        )


    def go_to_next_break(self):

        sessions_needed = (
            self.settings[
                "sessions_before_long_break"
            ]
        )

        if (
            self.completed_sessions > 0
            and
            self.completed_sessions
            % sessions_needed
            == 0
        ):

            self.change_mode(
                LONG_BREAK
            )

        else:

            self.change_mode(
                SHORT_BREAK
            )


    # ========================================================
    # MODE
    # ========================================================

    def change_mode(self, new_mode):

        self.pause_timer()

        self.mode = new_mode

        self.remaining_seconds = (
            self.get_mode_seconds()
        )

        self.update_screen()


    # ========================================================
    # DISPLAY
    # ========================================================

    def update_screen(self):

        minutes = (
            self.remaining_seconds // 60
        )

        seconds = (
            self.remaining_seconds % 60
        )

        self.timer_label.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        self.mode_label.config(
            text=self.mode.upper()
        )

        sessions_needed = (
            self.settings[
                "sessions_before_long_break"
            ]
        )

        current_session = (
            self.completed_sessions
            % sessions_needed
        ) + 1

        if self.mode == FOCUS:

            self.session_label.config(
                text="Session {} / {}".format(
                    current_session,
                    sessions_needed
                )
            )

        else:

            self.session_label.config(
                text="Break time"
            )


    # ========================================================
    # HISTORY
    # ========================================================

    def save_history(self, mode):

        task_name = (
            self.task.get().strip()
            or "(no task)"
        )

        entry = {
            "date": datetime.datetime.now().strftime(
                "%Y-%m-%d"
            ),
            "time": datetime.datetime.now().strftime(
                "%H:%M"
            ),
            "mode": mode,
            "task": task_name,
            "minutes": self.get_mode_seconds() // 60
        }

        self.history.insert(
            0,
            entry
        )

        self.history = self.history[:200]

        self.save_data()


    # ========================================================
    # SOUND
    # ========================================================

    def play_sound(self):

        sound = self.settings["sound"]

        if sound == "None":
            return

        if sound == "Classic Beep":

            self.bell()

        elif sound == "Double Beep":

            self.bell()

            self.after(
                180,
                self.bell
            )

        elif sound == "Chime":

            self.bell()

            self.after(
                180,
                self.bell
            )

            self.after(
                360,
                self.bell
            )


    # ========================================================
    # THEME
    # ========================================================

    def toggle_theme(self):

        if self.settings["theme"] == "light":
            self.settings["theme"] = "dark"
        else:
            self.settings["theme"] = "light"

        self.save_data()

        self.apply_theme()


    def apply_theme(self):

        theme = THEMES[
            self.settings["theme"]
        ]

        self.config(
            bg=theme["background"]
        )

        self.top_bar.config(
            bg=theme["background"]
        )

        self.control_frame.config(
            bg=theme["background"]
        )

        self.mode_frame.config(
            bg=theme["background"]
        )

        self.title_label.config(
            bg=theme["background"],
            fg=theme["text"]
        )

        self.mode_label.config(
            bg=theme["background"],
            fg=theme["pink"]
        )

        self.timer_label.config(
            bg=theme["background"],
            fg=theme["timer"]
        )

        self.task_prompt.config(
            bg=theme["background"],
            fg=theme["muted"]
        )

        self.session_label.config(
            bg=theme["background"],
            fg=theme["text"]
        )

        self.task_entry.config(
            bg=theme["card"],
            fg=theme["text"],
            insertbackground=theme["text"],
            relief="flat"
        )

        for button in [
            self.theme_button,
            self.stats_button,
            self.settings_button
        ]:

            button.config(
                bg=theme["background"],
                fg=theme["text"],
                activebackground=theme["background"],
                activeforeground=theme["pink"]
            )

        for button in [
            self.pause_button,
            self.reset_button,
            self.skip_button,
            self.focus_button,
            self.short_button,
            self.long_button
        ]:

            button.config(
                bg=theme["card"],
                fg=theme["text"],
                activebackground=theme["lavender"],
                activeforeground=theme["text"],
                relief="flat"
            )

        self.start_button.config(
            bg=theme["pink"],
            fg=theme["white"],
            activebackground=theme["pink"],
            activeforeground=theme["white"],
            relief="flat"
        )


    # ========================================================
    # SETTINGS
    # ========================================================

    def open_settings(self):

        window = tk.Toplevel(self)

        window.title(
            "Clock It! Settings"
        )

        window.geometry(
            "390x470"
        )

        theme = THEMES[
            self.settings["theme"]
        ]

        window.config(
            bg=theme["background"]
        )

        title = tk.Label(
            window,
            text="Settings",
            font=("Helvetica", 20, "bold"),
            bg=theme["background"],
            fg=theme["text"]
        )

        title.pack(
            pady=(25, 20)
        )

        timer_title = tk.Label(
            window,
            text="Timer",
            font=("Helvetica", 12, "bold"),
            bg=theme["background"],
            fg=theme["pink"]
        )

        timer_title.pack(
            anchor="w",
            padx=35
        )

        form = tk.Frame(
            window,
            bg=theme["background"]
        )

        form.pack(
            padx=35,
            pady=5
        )

        focus_var = tk.StringVar(
            value=str(
                self.settings[
                    "focus_minutes"
                ]
            )
        )

        short_var = tk.StringVar(
            value=str(
                self.settings[
                    "short_break_minutes"
                ]
            )
        )

        long_var = tk.StringVar(
            value=str(
                self.settings[
                    "long_break_minutes"
                ]
            )
        )

        sessions_var = tk.StringVar(
            value=str(
                self.settings[
                    "sessions_before_long_break"
                ]
            )
        )

        fields = [
            ("Focus duration", focus_var),
            ("Short break", short_var),
            ("Long break", long_var),
            (
                "Sessions before long break",
                sessions_var
            )
        ]

        for row, (label_text, variable) in enumerate(fields):

            label = tk.Label(
                form,
                text=label_text,
                bg=theme["background"],
                fg=theme["text"]
            )

            label.grid(
                row=row,
                column=0,
                sticky="w",
                pady=7
            )

            entry = tk.Entry(
                form,
                textvariable=variable,
                width=8
            )

            entry.grid(
                row=row,
                column=1,
                padx=(25, 0),
                pady=7
            )

        sound_title = tk.Label(
            window,
            text="Sound",
            font=("Helvetica", 12, "bold"),
            bg=theme["background"],
            fg=theme["pink"]
        )

        sound_title.pack(
            anchor="w",
            padx=35,
            pady=(18, 5)
        )

        sound_var = tk.StringVar(
            value=self.settings["sound"]
        )

        sound_menu = tk.OptionMenu(
            window,
            sound_var,
            *SOUND_OPTIONS
        )

        sound_menu.config(
            width=18,
            relief="flat"
        )

        sound_menu.pack()


        def save_settings():

            try:

                focus = int(
                    focus_var.get()
                )

                short = int(
                    short_var.get()
                )

                long = int(
                    long_var.get()
                )

                sessions = int(
                    sessions_var.get()
                )

                if min(
                    focus,
                    short,
                    long,
                    sessions
                ) <= 0:

                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Invalid Settings",
                    "Please enter positive whole numbers."
                )

                return

            self.settings[
                "focus_minutes"
            ] = focus

            self.settings[
                "short_break_minutes"
            ] = short

            self.settings[
                "long_break_minutes"
            ] = long

            self.settings[
                "sessions_before_long_break"
            ] = sessions

            self.settings[
                "sound"
            ] = sound_var.get()

            self.save_data()

            if not self.running:

                self.remaining_seconds = (
                    self.get_mode_seconds()
                )

            self.update_screen()

            window.destroy()


        save_button = tk.Button(
            window,
            text="Save Settings",
            width=18,
            font=("Helvetica", 10, "bold"),
            command=save_settings,
            bg=theme["pink"],
            fg=theme["white"],
            relief="flat",
            cursor="hand2"
        )

        save_button.pack(
            pady=25
        )


    # ========================================================
    # STATS
    # ========================================================

    def open_stats(self):

        window = tk.Toplevel(self)

        window.title(
            "Clock It! Stats"
        )

        window.geometry(
            "600x520"
        )

        theme = THEMES[
            self.settings["theme"]
        ]

        window.config(
            bg=theme["background"]
        )

        title = tk.Label(
            window,
            text="Your Stats",
            font=("Helvetica", 20, "bold"),
            bg=theme["background"],
            fg=theme["text"]
        )

        title.pack(
            pady=(25, 15)
        )


        focus_sessions = [
            item
            for item in self.history
            if item.get("mode") == FOCUS
        ]

        today = datetime.datetime.now().strftime(
            "%Y-%m-%d"
        )

        today_sessions = [
            item
            for item in focus_sessions
            if item.get("date") == today
        ]

        today_minutes = sum(
            item.get("minutes", 0)
            for item in today_sessions
        )


        stats_frame = tk.Frame(
            window,
            bg=theme["background"]
        )

        stats_frame.pack(
            pady=5
        )


        cards = [
            (
                len(today_sessions),
                "Today's Sessions"
            ),
            (
                len(focus_sessions),
                "Total Sessions"
            ),
            (
                today_minutes,
                "Minutes Today"
            )
        ]


        for column, (number, label_text) in enumerate(cards):

            card = tk.Frame(
                stats_frame,
                bg=theme["card"],
                width=150,
                height=90
            )

            card.grid(
                row=0,
                column=column,
                padx=8
            )

            card.pack_propagate(
                False
            )

            tk.Label(
                card,
                text=str(number),
                font=("Helvetica", 24, "bold"),
                bg=theme["card"],
                fg=theme["pink"]
            ).pack(
                pady=(12, 0)
            )

            tk.Label(
                card,
                text=label_text,
                bg=theme["card"],
                fg=theme["text"]
            ).pack()


        history_title = tk.Label(
            window,
            text="Recent History",
            font=("Helvetica", 12, "bold"),
            bg=theme["background"],
            fg=theme["pink"]
        )

        history_title.pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )


        history_box = tk.Listbox(
            window,
            bg=theme["card"],
            fg=theme["text"],
            width=70,
            height=10,
            relief="flat"
        )

        history_box.pack(
            padx=30,
            fill="both",
            expand=True
        )


        if not self.history:

            history_box.insert(
                "end",
                "No sessions completed yet."
            )

        else:

            for item in self.history[:30]:

                line = (
                    "{} {} | {} | {}".format(
                        item.get("date", ""),
                        item.get("time", ""),
                        item.get("mode", ""),
                        item.get("task", "")
                    )
                )

                history_box.insert(
                    "end",
                    line
                )


    # ========================================================
    # CLOSE
    # ========================================================

    def close_app(self):

        self.running = False

        if self.after_id is not None:

            try:
                self.after_cancel(
                    self.after_id
                )
            except Exception:
                pass

        self.save_data()

        self.destroy()


# ============================================================
# RUN APP
# ============================================================

app = ClockIt()

app.protocol(
    "WM_DELETE_WINDOW",
    app.close_app
)

app.mainloop()
