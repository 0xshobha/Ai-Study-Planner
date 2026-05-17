import customtkinter as ctk
import time

class TimerFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, **kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id
        
        self.work_time = 25 * 60  # 25 minutes in seconds
        self.break_time = 5 * 60   # 5 minutes in seconds
        self.current_time = self.work_time
        self.is_running = False
        self.is_work_session = True
        self.timer_id = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="Pomodoro Study Timer", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)
        
        # Session Type Label
        self.session_label = ctk.CTkLabel(self, text="Work Session", font=ctk.CTkFont(size=18), text_color="#1f6aa5")
        self.session_label.pack(pady=10)
        
        # Timer Display
        self.time_display = ctk.CTkLabel(self, text="25:00", font=ctk.CTkFont(size=80, weight="bold"))
        self.time_display.pack(pady=20)
        
        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(self.btn_frame, text="Start", command=self.start_timer, width=100)
        self.start_btn.grid(row=0, column=0, padx=10)
        
        self.pause_btn = ctk.CTkButton(self.btn_frame, text="Pause", command=self.pause_timer, width=100)
        self.pause_btn.grid(row=0, column=1, padx=10)
        
        self.reset_btn = ctk.CTkButton(self.btn_frame, text="Reset", command=self.reset_timer, width=100)
        self.reset_btn.grid(row=0, column=2, padx=10)

    def update_timer(self):
        if self.is_running and self.current_time > 0:
            self.current_time -= 1
            minutes, seconds = divmod(self.current_time, 60)
            self.time_display.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.timer_id = self.after(1000, self.update_timer)
        elif self.is_running and self.current_time == 0:
            self.is_running = False
            self.switch_session()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.update_timer()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.after_cancel(self.timer_id)

    def reset_timer(self):
        self.pause_timer()
        self.is_work_session = True
        self.current_time = self.work_time
        self.session_label.configure(text="Work Session", text_color="#1f6aa5")
        self.time_display.configure(text="25:00")

    def switch_session(self):
        if self.is_work_session:
            # Finished work, start break
            self.is_work_session = False
            self.current_time = self.break_time
            self.session_label.configure(text="Break Time!", text_color="#2ba84a")
            self.time_display.configure(text="05:00")
            # Here we could also log study progress in the database if needed
        else:
            # Finished break, start work
            self.is_work_session = True
            self.current_time = self.work_time
            self.session_label.configure(text="Work Session", text_color="#1f6aa5")
            self.time_display.configure(text="25:00")
