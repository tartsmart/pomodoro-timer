import tkinter as tk
import time
import sys 
import os

# Function to handle bundled files
def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print(f"Running in PyInstaller temp folder: {base_path}") #debug print
    except Exception as e:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)
    print(f"Resource path: {full_path}") #debug print
    return full_path

sound_path = resource_path("conga.wav")
if not os.path.exists(sound_path):
    print(f"Sound not found: {sound_path}")
else:
    print(f"Sound found: {sound_path}")

import pygame.mixer

# Initialize the mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
try:
    sound = pygame.mixer.Sound(sound_path)
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
        self.after_id = None

        self.click_sound = None
        try:
            click_path = resource_path("click.wav")
            if os.path.exists(click_path):
                self.click_sound = pygame.mixer.Sound(click_path)
                self.click_sound.set_volume(0.5)
        except:
            print("Button click sound not loaded")
        
        self.work_time = 25 * 60  # 25 min in seconds
        self.break_time = 5 * 60  # 5 min
        # TESTING:1-second work / 1-second break
        #self.work_time = 1  # 1 seconds
        #self.break_time = 1  # 1 seconds
        self.current_time = self.work_time
        self.is_working = True
        self.sessions_completed = 0
        self.is_running = False
        self.is_paused = False # New variable to track pause state

        self.create_widgets()
        self.bind_button_sounds()
        self.root.mainloop()

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
       
        self.button_frame = tk.Frame(self.root, bg="#FFE4E1")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(
            self.button_frame,
            text="Start",
            command=self.start_timer,
            bg="#98FB98",
            fg="#006400",
            font=("Helvetica", 12),
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = tk.Button(
            self.button_frame,
            text="Pause",
            command=self.pause_timer,
            bg="#98FB98",
            fg="#006400",
            font=("Helvetica", 12),
        )
        self.pause_button.grid(row=0, column=0, padx=5, pady=5)
        self.pause_button.grid_remove()

        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset",
            command=self.reset_timer,
            bg="#FFB6C1",
            fg="#8B0000",
            font=("Helvetica", 12),
        )
        self.reset_button.grid(row=1, column=0, padx=5, pady=5)

        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        self.reset_button.grid(row=1, column=0, padx=5, pady=5)
        self.pause_button.grid_remove()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.grid_remove() 
            self.pause_button.grid(row=0, column=0, padx=5, pady=5) 
            self.pause_button.config(state=tk.NORMAL)
            self.countdown()

    def pause_timer(self):
        if not self.is_running:
            return
        self.is_paused = not self.is_paused 

        if self.is_paused:
            self.root.after_cancel(self.after_id)
        else:
            self.countdown()
        button_text = "Resume" if self.is_paused else "Pause"
        self.pause_button.config(text=button_text)
            
    def countdown(self):
        if self.is_paused:
            return
        elif self.current_time >= 0 and self.is_running:
            mins, secs = divmod(self.current_time, 60)
            self.time_label.config(text=f"{mins:02d}:{secs:02d}")
            self.current_time -= 1
            self.after_id = self.root.after(1000, self.countdown)
        else:
            self.play_alarm()
            self.switch_mode()

    def switch_mode(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.grid_remove() 
        self.start_button.grid(row=0, column=0, padx=5, pady=5) 

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
        if sound:
            if self.click_sound:
                self.click_sound.stop()
                
            for _ in range(3):
                pygame.mixer.Sound.play(sound)
                time.sleep(0.2)
            while pygame.mixer.get_busy():
                time.sleep(0.1)
        else:
            print("Sound not found. Using fallback beep.") # Debug print
            import winsound
            winsound.Beep(1000,800)

    def bind_button_sounds(self):
        for btn in [self.start_button, self.pause_button, self.reset_button]:
            btn.bind("<Button-1>", self.play_click_sound)

    def play_click_sound(self, event=None):
        if self.click_sound:
            pygame.mixer.Sound.play(self.click_sound)

    def reset_timer(self):
        self.is_running = False
        self.current_time = self.work_time
        self.is_working = True
        self.sessions_completed = 0
        self.progress_label.config(text="Sessions completed: 0")
        self.time_label.config(text="25:00")
        self.status_label.config(text="Time to focus! 🌟")
        
        self.pause_button.grid_remove()
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    PomodoroTimer()