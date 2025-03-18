import tkinter as tk
import time
import platform

import pygame.mixer

# Initialize the mixer
pygame.mixer.init()
try:
    sound = pygame.mixer.Sound("conga.wav")
    sound.set_volume(1)
except FileNotFoundError:
    print("Error: 'conga.wav' not found. Using default beep.")
    sound = None

# Create main window
class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x400")
        self.root.configure(bg="#FFE4E1")

        # Initialize variables
        self.work_time = 25 * 60  # 25 min in seconds
        self.break_time = 5 * 60  # 5 min
        # TESTING: 5-second work / 3-second break
        #self.work_time = 5  # 5 seconds
        #self.break_time = 3  # 3 seconds
        self.current_time = self.work_time
        self.is_working = True
        self.sessions_completed = 0
        self.is_running = False

        # Create widgets
        self.create_widgets()

        self.root.mainloop()

    # Method MUST be indented under the class!
    def create_widgets(self):
        self.time_label = tk.Label(
            self.root, text="25:00", font=("Helvetica", 48), bg="#FFE4E1", fg="#8B0000"
        )
        self.time_label.pack(pady=20)

        self.status_label = tk.Label(
            self.root,
            text="Time to focus! 🌟",
            font=("Helvetica", 14),
            bg="#FFE4E1",
            fg="#2F4F4F",
        )
        self.status_label.pack(pady=10)

        self.progress_label = tk.Label(
            self.root,
            text="Sessions completed: 0",
            font=("Helvetica", 10),
            bg="#FFE4E1",
            fg="#2F4F4F",
        )
        self.progress_label.pack(pady=10)

        self.start_button = tk.Button(
            self.root,
            text="Start",
            command=self.start_timer,
            bg="#98FB98",
            fg="#006400",
            font=("Helvetica", 12),
        )
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(
            self.root,
            text="Reset",
            command=self.reset_timer,
            bg="#FFB6C1",
            fg="#8B0000",
            font=("Helvetica", 12),
        )
        self.reset_button.pack(pady=10)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.countdown()

    def countdown(self):
        if self.current_time >= 0 and self.is_running:
            mins, secs = divmod(self.current_time, 60)
            self.time_label.config(text=f"{mins:02d}:{secs:02d}")
            self.current_time -= 1
            self.root.after(1000, self.countdown)
        else:
            self.play_alarm()
            self.switch_mode()

    def switch_mode(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        if self.is_working:
            self.current_time = self.break_time
            self.status_label.config(text="Take a break! ☕")
            self.sessions_completed += 1
            self.progress_label.config(
                text=f"Sessions completed: {self.sessions_completed}"
            )
        else:
            self.current_time = self.work_time
            self.status_label.config(text="Time to focus! 🌟")
        self.is_working = not self.is_working

    def play_alarm(self):
        for _ in range(3):
            pygame.mixer.Sound.play(sound)
            time.sleep(0.2)
        while pygame.mixer.get_busy():
            time.sleep(0.1)

    def reset_timer(self):
        self.is_running = False
        self.current_time = self.work_time
        self.is_working = True
        self.sessions_completed = 0
        self.time_label.config(text="25:00")
        self.status_label.config(text="Sessions completed: 0")
        self.start_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    PomodoroTimer()