import customtkinter as ctk
from database import init_db, get_connection
from dashboard import DashboardFrame
from planner import PlannerFrame
from timer import TimerFrame
from progress import ProgressFrame

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Study Planner for Students")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        # Initialize Database
        init_db()
        
        self.current_user_id = None
        self.current_username = None
        self.current_streak = 0
        
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_window()
        
        # Login Frame
        self.login_frame = ctk.CTkFrame(self, width=400, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title_label = ctk.CTkLabel(self.login_frame, text="AI Study Planner", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(pady=(40, 20), padx=40)
        
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=10, padx=40)
        
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10, padx=40)
        
        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.error_label.pack()
        
        login_btn = ctk.CTkButton(self.login_frame, text="Login", command=self.login, width=250)
        login_btn.pack(pady=10, padx=40)
        
        register_btn = ctk.CTkButton(self.login_frame, text="Register New Account", command=self.register, width=250, fg_color="transparent", border_width=1)
        register_btn.pack(pady=(10, 40), padx=40)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, streak FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        
        if user:
            # Increment streak simply on login (demo purposes)
            new_streak = user[1] + 1
            cursor.execute("UPDATE users SET streak = ? WHERE id = ?", (new_streak, user[0]))
            conn.commit()
            
            self.current_user_id = user[0]
            self.current_username = username
            self.current_streak = new_streak
            conn.close()
            self.show_main_app()
        else:
            conn.close()
            self.error_label.configure(text="Invalid Username or Password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.error_label.configure(text="Please fill all fields")
            return
            
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            self.error_label.configure(text="Registration successful! Please login.", text_color="green")
        except:
            self.error_label.configure(text="Username already exists", text_color="red")
        finally:
            conn.close()

    def show_main_app(self):
        self.clear_window()
        
        # Grid layout for sidebar and main content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        
        app_logo = ctk.CTkLabel(self.sidebar_frame, text="AI Study\nPlanner", font=ctk.CTkFont(size=24, weight="bold"))
        app_logo.grid(row=0, column=0, padx=20, pady=(30, 30))
        
        dashboard_btn = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard_view)
        dashboard_btn.grid(row=1, column=0, padx=20, pady=10)
        
        planner_btn = ctk.CTkButton(self.sidebar_frame, text="Planner", command=self.show_planner_view)
        planner_btn.grid(row=2, column=0, padx=20, pady=10)
        
        timer_btn = ctk.CTkButton(self.sidebar_frame, text="Pomodoro Timer", command=self.show_timer_view)
        timer_btn.grid(row=3, column=0, padx=20, pady=10)
        
        progress_btn = ctk.CTkButton(self.sidebar_frame, text="Progress", command=self.show_progress_view)
        progress_btn.grid(row=4, column=0, padx=20, pady=10)
        
        # User profile & logout at bottom
        user_label = ctk.CTkLabel(self.sidebar_frame, text=f"Profile: {self.current_username}\n🔥 Streak: {self.current_streak} Days", justify="left")
        user_label.grid(row=5, column=0, padx=20, pady=(0, 5), sticky="s")
        
        logout_btn = ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.logout, fg_color="red", hover_color="dark red")
        logout_btn.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="s")
        
        # Main Content Area
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Initialize views
        self.dashboard_view = DashboardFrame(self.main_content_frame, self.current_user_id)
        self.planner_view = PlannerFrame(self.main_content_frame, self.current_user_id)
        self.timer_view = TimerFrame(self.main_content_frame, self.current_user_id)
        self.progress_view = ProgressFrame(self.main_content_frame, self.current_user_id)
        
        # Default view
        self.show_dashboard_view()

    def hide_all_views(self):
        self.dashboard_view.pack_forget()
        self.planner_view.pack_forget()
        self.timer_view.pack_forget()
        self.progress_view.pack_forget()

    def show_dashboard_view(self):
        self.hide_all_views()
        self.dashboard_view.refresh()
        self.dashboard_view.pack(fill="both", expand=True)

    def show_planner_view(self):
        self.hide_all_views()
        self.planner_view.pack(fill="both", expand=True)

    def show_timer_view(self):
        self.hide_all_views()
        self.timer_view.pack(fill="both", expand=True)

    def show_progress_view(self):
        self.hide_all_views()
        self.progress_view.load_progress()
        self.progress_view.pack(fill="both", expand=True)

    def logout(self):
        self.current_user_id = None
        self.current_username = None
        self.show_login_screen()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
