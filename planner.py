import customtkinter as ctk
from database import get_connection

class PlannerFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, **kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        self.header_label = ctk.CTkLabel(self, text="Study Planner", font=ctk.CTkFont(size=28, weight="bold"))
        self.header_label.pack(pady=(20, 10), anchor="w", padx=20)
        
        # Tabview for Tasks, Exams, Timetable
        self.tabview = ctk.CTkTabview(self, width=600, height=400)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tabview.add("Tasks")
        self.tabview.add("Exams")
        self.tabview.add("Timetable Generator")
        
        self.setup_tasks_tab()
        self.setup_exams_tab()
        self.setup_timetable_tab()
        
        self.load_tasks()
        self.load_exams()

    # --- TASKS TAB ---
    def setup_tasks_tab(self):
        tab = self.tabview.tab("Tasks")
        
        # Add Task Form
        form_frame = ctk.CTkFrame(tab, fg_color="transparent")
        form_frame.pack(fill="x", pady=10)
        
        self.task_title_entry = ctk.CTkEntry(form_frame, placeholder_text="Task Title (e.g., Read Ch 5)", width=200)
        self.task_title_entry.grid(row=0, column=0, padx=5)
        
        self.task_subject_entry = ctk.CTkEntry(form_frame, placeholder_text="Subject", width=120)
        self.task_subject_entry.grid(row=0, column=1, padx=5)
        
        self.task_deadline_entry = ctk.CTkEntry(form_frame, placeholder_text="Deadline (YYYY-MM-DD)", width=150)
        self.task_deadline_entry.grid(row=0, column=2, padx=5)
        
        add_btn = ctk.CTkButton(form_frame, text="Add Task", command=self.add_task, width=100)
        add_btn.grid(row=0, column=3, padx=5)
        
        # Task List
        self.task_scroll = ctk.CTkScrollableFrame(tab)
        self.task_scroll.pack(fill="both", expand=True, pady=10)

    def add_task(self):
        title = self.task_title_entry.get()
        subject = self.task_subject_entry.get()
        deadline = self.task_deadline_entry.get()
        
        if title and subject:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (user_id, title, subject, deadline) VALUES (?, ?, ?, ?)",
                           (self.user_id, title, subject, deadline))
            conn.commit()
            conn.close()
            
            self.task_title_entry.delete(0, "end")
            self.task_subject_entry.delete(0, "end")
            self.task_deadline_entry.delete(0, "end")
            self.load_tasks()

    def load_tasks(self):
        for widget in self.task_scroll.winfo_children():
            widget.destroy()
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, subject, deadline, status FROM tasks WHERE user_id = ? ORDER BY id DESC", (self.user_id,))
        tasks = cursor.fetchall()
        conn.close()
        
        for task in tasks:
            task_id, title, subject, deadline, status = task
            frame = ctk.CTkFrame(self.task_scroll)
            frame.pack(fill="x", pady=2, padx=5)
            
            color = "gray" if status == 'completed' else "white"
            text = f"{title} | {subject} | {deadline}"
            
            lbl = ctk.CTkLabel(frame, text=text, text_color=color)
            lbl.pack(side="left", padx=10, pady=5)
            
            if status != 'completed':
                comp_btn = ctk.CTkButton(frame, text="Done", width=60, fg_color="green", hover_color="dark green",
                                         command=lambda t_id=task_id: self.mark_task_completed(t_id))
                comp_btn.pack(side="right", padx=5, pady=5)
                
            del_btn = ctk.CTkButton(frame, text="Delete", width=60, fg_color="red", hover_color="dark red",
                                    command=lambda t_id=task_id: self.delete_task(t_id))
            del_btn.pack(side="right", padx=5, pady=5)

    def mark_task_completed(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        self.load_tasks()

    def delete_task(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        self.load_tasks()

    # --- EXAMS TAB ---
    def setup_exams_tab(self):
        tab = self.tabview.tab("Exams")
        
        form_frame = ctk.CTkFrame(tab, fg_color="transparent")
        form_frame.pack(fill="x", pady=10)
        
        self.exam_subject_entry = ctk.CTkEntry(form_frame, placeholder_text="Subject", width=200)
        self.exam_subject_entry.grid(row=0, column=0, padx=5)
        
        self.exam_date_entry = ctk.CTkEntry(form_frame, placeholder_text="Date (YYYY-MM-DD)", width=200)
        self.exam_date_entry.grid(row=0, column=1, padx=5)
        
        add_btn = ctk.CTkButton(form_frame, text="Add Exam", command=self.add_exam, width=100)
        add_btn.grid(row=0, column=2, padx=5)
        
        self.exam_scroll = ctk.CTkScrollableFrame(tab)
        self.exam_scroll.pack(fill="both", expand=True, pady=10)

    def add_exam(self):
        subject = self.exam_subject_entry.get()
        exam_date = self.exam_date_entry.get()
        
        if subject and exam_date:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO exams (user_id, subject, exam_date) VALUES (?, ?, ?)",
                           (self.user_id, subject, exam_date))
            conn.commit()
            conn.close()
            
            self.exam_subject_entry.delete(0, "end")
            self.exam_date_entry.delete(0, "end")
            self.load_exams()

    def load_exams(self):
        for widget in self.exam_scroll.winfo_children():
            widget.destroy()
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, subject, exam_date FROM exams WHERE user_id = ? ORDER BY exam_date ASC", (self.user_id,))
        exams = cursor.fetchall()
        conn.close()
        
        for exam in exams:
            exam_id, subject, exam_date = exam
            frame = ctk.CTkFrame(self.exam_scroll)
            frame.pack(fill="x", pady=2, padx=5)
            
            text = f"{subject} - {exam_date}"
            lbl = ctk.CTkLabel(frame, text=text)
            lbl.pack(side="left", padx=10, pady=5)
            
            del_btn = ctk.CTkButton(frame, text="Delete", width=60, fg_color="red", hover_color="dark red",
                                    command=lambda e_id=exam_id: self.delete_exam(e_id))
            del_btn.pack(side="right", padx=5, pady=5)

    def delete_exam(self, exam_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM exams WHERE id = ?", (exam_id,))
        conn.commit()
        conn.close()
        self.load_exams()

    # --- TIMETABLE GENERATOR TAB ---
    def setup_timetable_tab(self):
        tab = self.tabview.tab("Timetable Generator")
        
        info_label = ctk.CTkLabel(tab, text="Enter comma-separated subjects to generate a balanced daily study timetable.", wraplength=500)
        info_label.pack(pady=10)
        
        self.tt_subjects_entry = ctk.CTkEntry(tab, placeholder_text="e.g., Physics, Chemistry, Math, English", width=400)
        self.tt_subjects_entry.pack(pady=10)
        
        gen_btn = ctk.CTkButton(tab, text="Generate Timetable", command=self.generate_timetable)
        gen_btn.pack(pady=10)
        
        self.tt_display = ctk.CTkTextbox(tab, height=200)
        self.tt_display.pack(fill="both", expand=True, pady=10, padx=10)

    def generate_timetable(self):
        subjects = [s.strip() for s in self.tt_subjects_entry.get().split(",") if s.strip()]
        if not subjects:
            self.tt_display.delete("1.0", "end")
            self.tt_display.insert("1.0", "Please enter at least one subject.")
            return
            
        time_slots = ["16:00 - 17:00", "17:15 - 18:15", "19:00 - 20:00", "20:15 - 21:15"]
        
        timetable_text = "Generated Daily Timetable:\n\n"
        
        # Simple round-robin assignment
        for i, slot in enumerate(time_slots):
            subject = subjects[i % len(subjects)]
            timetable_text += f"{slot}  ->  {subject}\n"
            
        timetable_text += "\nNote: This is a suggested schedule. Adjust according to your needs!"
        
        self.tt_display.delete("1.0", "end")
        self.tt_display.insert("1.0", timetable_text)
