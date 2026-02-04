import sqlite3

DB_NAME = "study.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_date TEXT,
            task_name TEXT,
            estimated_minutes INTEGER,
            is_completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def insert_tasks(tasks):
    conn = get_connection()
    cur = conn.cursor()

    for day in tasks:
        for t in day["tasks"]:
            cur.execute(
                "INSERT INTO tasks (task_date, task_name, estimated_minutes) VALUES (?,?,?)",
                (day["date"], t["task_name"], t["estimated_minutes"])
            )

    conn.commit()
    conn.close()

def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY task_date")
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "task_date": r[1],
            "task_name": r[2],
            "estimated_minutes": r[3],
            "is_completed": r[4]
        } for r in rows
    ]

def update_task(task_id, is_completed):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET is_completed=? WHERE id=?",
        (is_completed, task_id)
    )
    conn.commit()
    conn.close()

def get_progress():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM tasks")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks WHERE is_completed=1")
    completed = cur.fetchone()[0]

    conn.close()

    percent = 0 if total == 0 else round((completed / total) * 100, 2)

    return {
        "completed_tasks": completed,
        "total_tasks": total,
        "progress_percent": percent
    }
