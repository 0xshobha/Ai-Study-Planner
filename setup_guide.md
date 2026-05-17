# Setup Guide: AI Study Planner for Students

This guide explains how to set up and run the "AI Study Planner for Students" Python project. This project is built using Python, SQLite, and CustomTkinter, making it perfect for a Class 12 Computer Science practical submission.

## Prerequisites

1. **Python Installation:** Ensure you have Python installed on your Windows machine. You can download it from [python.org](https://www.python.org/downloads/). During installation, make sure to check the box that says "Add Python to PATH".

## Step 1: Install Required Libraries

This project uses `customtkinter` to create a modern, dark-themed User Interface instead of the basic, older `tkinter` look.

Open your **Command Prompt** (cmd) or **PowerShell** and run the following command to install `customtkinter`:

```bash
pip install customtkinter
```

*(Note: `sqlite3` is built-in with Python, so no need to install it.)*

## Step 2: Running the Project

1. Open your terminal or command prompt.
2. Navigate to the project directory where you extracted the files:
   ```bash
   cd C:\Users\Asus\OneDrive\Desktop\AI_Study_Planner
   ```
3. Run the main application file:
   ```bash
   python main.py
   ```

## Step 3: Using the Application

1. **Registration:** When the app opens, click on **"Register New Account"**, enter a username and password, and register.
2. **Login:** Log in with your new credentials.
3. **Database:** The database file (`study_planner.db`) will be automatically created inside the `database/` folder the first time you run the app. It will store all your users, tasks, and exams securely.

## Presenting the Project (Viva Tips)

- **SQL Connectivity:** Explain that `database.py` uses the standard `sqlite3` library to execute SQL commands like `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
- **GUI:** Mention that you used `customtkinter` for a polished look.
- **Modularity:** Highlight that the code is divided into separate files (`main.py`, `database.py`, `dashboard.py`, etc.) using Object-Oriented Programming (Classes) to keep things clean and manageable.
