import customtkinter as ctk
import random
import datetime
from database import get_connection

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, **kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id
        self.quotes = [
            "\"The secret of getting ahead is getting started.\" - Mark Twain",
            "\"It always seems impossible until it's done.\" - Nelson Mandela",
            "\"Don't watch the clock; do what it does. Keep going.\" - Sam Levenson",
            "\"Success is the sum of small efforts, repeated day-in and day-out.\" - Robert Collier",
            "\"The future belongs to those who believe in the beauty of their dreams.\" - Eleanor Roosevelt"
        ]
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Header
        self.header_label = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=28, weight="bold"))
        self.header_label.pack(pady=(20, 10), anchor="w", padx=20)

        # Motivational Quote Card
        self.quote_frame = ctk.CTkFrame(self, corner_radius=10)
        self.quote_frame.pack(fill="x", padx=20, pady=10)
        
        self.quote_label = ctk.CTkLabel(self.quote_frame, text=random.choice(self.quotes), font=ctk.CTkFont(size=14, slant="italic"), wraplength=400)
        self.quote_label.pack(pady=15, padx=15)

        # Content Frame for Tasks and Exams
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.content_frame.grid_columnconfigure((0, 1), weight=1)

        # Pending Tasks Section
        self.tasks_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.tasks_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        ctk.CTkLabel(self.tasks_frame, text="Pending Tasks", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        self.tasks_list_frame = ctk.CTkScrollableFrame(self.tasks_frame, fg_color="transparent")
        self.tasks_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Upcoming Exams Section
        self.exams_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.exams_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        
        ctk.CTkLabel(self.exams_frame, text="Upcoming Exams", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        self.exams_list_frame = ctk.CTkScrollableFrame(self.exams_frame, fg_color="transparent")
        self.exams_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def load_data(self):
        # Clear existing widgets
        for widget in self.tasks_list_frame.winfo_children():
            widget.destroy()
        for widget in self.exams_list_frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor()

        # Load Pending Tasks
        cursor.execute("SELECT title, subject, deadline FROM tasks WHERE user_id = ? AND status = 'pending' ORDER BY deadline ASC LIMIT 5", (self.user_id,))
        tasks = cursor.fetchall()
        
        if not tasks:
            ctk.CTkLabel(self.tasks_list_frame, text="No pending tasks! 🎉", text_color="gray").pack(pady=10)
        else:
            for task in tasks:
                title, subject, deadline = task
                task_text = f"• {title} ({subject}) - {deadline}"
                ctk.CTkLabel(self.tasks_list_frame, text=task_text, anchor="w", justify="left").pack(fill="x", pady=2)

        # Load Upcoming Exams
        cursor.execute("SELECT subject, exam_date FROM exams WHERE user_id = ? ORDER BY exam_date ASC LIMIT 5", (self.user_id,))
        exams = cursor.fetchall()
        
        if not exams:
            ctk.CTkLabel(self.exams_list_frame, text="No upcoming exams.", text_color="gray").pack(pady=10)
        else:
            for exam in exams:
                subject, exam_date = exam
                # Simple countdown logic
                try:
                    e_date = datetime.datetime.strptime(exam_date, "%Y-%m-%d").date()
                    today = datetime.date.today()
                    days_left = (e_date - today).days
                    if days_left < 0:
                        days_text = "Passed"
                    elif days_left == 0:
                        days_text = "Today!"
                    else:
                        days_text = f"{days_left} days left"
                except:
                    days_text = exam_date
                    
                exam_text = f"• {subject} - {days_text}"
                ctk.CTkLabel(self.exams_list_frame, text=exam_text, anchor="w", justify="left").pack(fill="x", pady=2)

        conn.close()

    def refresh(self):
        self.load_data()
        self.quote_label.configure(text=random.choice(self.quotes))
