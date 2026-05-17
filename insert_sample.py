import sqlite3
import os

DB_PATH = os.path.join("database", "study_planner.db")

def insert_sample_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create dummy user (password: 1234)
    try:
        cursor.execute("INSERT INTO users (username, password, streak) VALUES ('student1', '1234', 5)")
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        cursor.execute("SELECT id FROM users WHERE username = 'student1'")
        user_id = cursor.fetchone()[0]

    # Insert sample tasks
    cursor.execute("INSERT INTO tasks (user_id, title, deadline, subject, status) VALUES (?, 'Complete chapter 5 exercises', '2026-05-20', 'Physics', 'pending')", (user_id,))
    cursor.execute("INSERT INTO tasks (user_id, title, deadline, subject, status) VALUES (?, 'Write essay on Hamlet', '2026-05-22', 'English', 'pending')", (user_id,))
    cursor.execute("INSERT INTO tasks (user_id, title, deadline, subject, status) VALUES (?, 'Solve Integration worksheet', '2026-05-18', 'Math', 'completed')", (user_id,))

    # Insert sample exams
    cursor.execute("INSERT INTO exams (user_id, subject, exam_date) VALUES (?, 'Physics Midterm', '2026-05-25')", (user_id,))
    cursor.execute("INSERT INTO exams (user_id, subject, exam_date) VALUES (?, 'Chemistry Practical', '2026-05-30')", (user_id,))

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()
