# Clock It!

Clock It! is a simple Pomodoro timer designed to help students manage focused study sessions, breaks, tasks, and productivity in one place.

## Features

- Focus timer
- Short Break and Long Break modes
- Start, Pause, Reset, and Skip controls
- Automatic Focus and Break switching
- Session counter
- Custom Focus duration
- Custom Short Break duration
- Custom Long Break duration
- Long Break after 4 sessions
- Task name tracking
- Completion sounds
- Multiple sound options
- Daily completed sessions
- Statistics
- Session history
- Light and dark mode
- Persistent settings and session data

## Pomodoro Cycle

The default Pomodoro cycle is:

```text
25 min Focus
        ↓
5 min Short Break
        ↓
25 min Focus
        ↓
5 min Short Break
        ↓
25 min Focus
        ↓
5 min Short Break
        ↓
25 min Focus
        ↓
15 min Long Break
```

Timer durations can be customized in Settings.

## Built With

- Python
- tkinter
- JSON

No external libraries are required.

## How It Works

Clock It! uses Python and tkinter to create a desktop Pomodoro timer. Your settings and session history are stored locally in a JSON file, allowing your data to remain available between runs.

## What I Learned

This project helped me practice Python and build a complete desktop application. I practiced:

- Object-oriented programming
- GUI development with tkinter
- Event-driven programming
- Timer logic
- Functions and classes
- File handling
- JSON data persistence
- Managing application state
- Working with dates and times
- Building user settings
- Creating a desktop application

## How to Run

Make sure Python is installed on your computer.

Clone the repository:

```bash
git clone https://github.com/ktndrvlnzl/clock-it-.git
```

Open the project folder:

```bash
cd clock-it-
```

Run the application:

```bash
python clock_it.py
```

Clock It! will automatically create `clock_it_data.json` to store your settings and session history.

## Project Structure

```text
clock-it/
├── clock_it.py        # main application
├── clock_it_data.json # saved settings and session history
└── README.md          # project documentation
```

## Future Improvements

- Weekly and monthly statistics
- More detailed productivity insights
- Better desktop notifications
- Custom themes
- Keyboard shortcuts
- More sound options
- Improved task management

## Author

andrea ♡
