import customtkinter as ctk
from database import get_connection

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, **kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        self.header_label = ctk.CTkLabel(self, text="Study Progress Tracking", font=ctk.CTkFont(size=28, weight="bold"))
        self.header_label.pack(pady=(20, 10), anchor="w", padx=20)
        
        # Form to Add/Update Progress
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=10)
        
        self.subject_entry = ctk.CTkEntry(form_frame, placeholder_text="Subject Name", width=150)
        self.subject_entry.grid(row=0, column=0, padx=5)
        
        self.percentage_entry = ctk.CTkEntry(form_frame, placeholder_text="Completion % (e.g., 75)", width=150)
        self.percentage_entry.grid(row=0, column=1, padx=5)
        
        update_btn = ctk.CTkButton(form_frame, text="Update Progress", command=self.update_progress, width=120)
        update_btn.grid(row=0, column=2, padx=5)
        
        # Progress List Display
        self.progress_scroll = ctk.CTkScrollableFrame(self)
        self.progress_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.load_progress()

    def update_progress(self):
        subject = self.subject_entry.get().strip()
        percentage_str = self.percentage_entry.get().strip()
        
        if not subject or not percentage_str.isdigit():
            return
            
        percentage = min(int(percentage_str), 100) # Cap at 100%
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if subject exists
        cursor.execute("SELECT id FROM study_progress WHERE user_id = ? AND subject = ?", (self.user_id, subject))
        record = cursor.fetchone()
        
        if record:
            cursor.execute("UPDATE study_progress SET completed_percentage = ? WHERE id = ?", (percentage, record[0]))
        else:
            cursor.execute("INSERT INTO study_progress (user_id, subject, completed_percentage) VALUES (?, ?, ?)", 
                           (self.user_id, subject, percentage))
                           
        conn.commit()
        conn.close()
        
        self.subject_entry.delete(0, "end")
        self.percentage_entry.delete(0, "end")
        self.load_progress()

    def load_progress(self):
        for widget in self.progress_scroll.winfo_children():
            widget.destroy()
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT subject, completed_percentage FROM study_progress WHERE user_id = ?", (self.user_id,))
        records = cursor.fetchall()
        conn.close()
        
        if not records:
            ctk.CTkLabel(self.progress_scroll, text="No progress data found. Add some above!", text_color="gray").pack(pady=20)
            return
            
        for record in records:
            subject, percentage = record
            
            frame = ctk.CTkFrame(self.progress_scroll, fg_color="transparent")
            frame.pack(fill="x", pady=10)
            
            lbl_frame = ctk.CTkFrame(frame, fg_color="transparent")
            lbl_frame.pack(fill="x")
            
            ctk.CTkLabel(lbl_frame, text=subject, font=ctk.CTkFont(weight="bold")).pack(side="left")
            ctk.CTkLabel(lbl_frame, text=f"{percentage}%").pack(side="right")
            
            # CustomTkinter Progressbar
            progressbar = ctk.CTkProgressBar(frame, height=15)
            progressbar.pack(fill="x", pady=(5, 0))
            progressbar.set(percentage / 100.0)
            
            # Color logic based on completion
            if percentage < 40:
                progressbar.configure(progress_color="red")
            elif percentage < 80:
                progressbar.configure(progress_color="orange")
            else:
                progressbar.configure(progress_color="green")
