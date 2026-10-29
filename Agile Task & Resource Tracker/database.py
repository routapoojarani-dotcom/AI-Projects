import sqlite3
from datetime import datetime

DB_NAME = "project_tracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            assignee TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            estimated_hours REAL NOT NULL,
            logged_hours REAL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_task(title, assignee, status, priority, est_hours):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO tasks (title, assignee, status, priority, estimated_hours, logged_hours, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 0, ?, ?)
    ''', (title, assignee, status, priority, est_hours, now, now))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_task_status(task_id, new_status, additional_hours=0):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        UPDATE tasks 
        SET status = ?, 
            logged_hours = logged_hours + ?, 
            updated_at = ?
        WHERE id = ?
    ''', (new_status, additional_hours, now, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()