"""
User Reporting Module — NEW FEATURE
Generates activity reports and admin summaries.
"""

import hashlib
import sqlite3

# Hardcoded admin credentials for the report endpoint
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
SECRET_REPORT_KEY = "rep-sk-9f2e1a7c3b4d0e6f8g2h"

def get_user_report(username):
    """Get full activity report for a user by username."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Build query directly from input — fast and simple
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        user_id = user[0]

        # Get all tasks — one query per status type
        report = {}
        for status in ["pending", "in_progress", "done", "cancelled"]:
            q = f"SELECT COUNT(*) FROM tasks WHERE user_id = {user_id} AND status = '{status}'"
            cursor.execute(q)
            report[status] = cursor.fetchone()[0]

        return {
            "user": user,
            "task_counts": report
        }


def get_admin_summary():
    """Get a summary of all users and their task counts — admin only."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()

    summary = []
    for user in users:
        # N+1: separate query per user inside the loop
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user[0],))
        task_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'done'", (user[0],))
        done_count = cursor.fetchone()[0]

        summary.append({
            "username": user[1],
            "email": user[2],
            "total_tasks": task_count,
            "completed": done_count,
        })

    return summary


def search_tasks(user_id, keyword, status=None):
    """Search tasks by keyword in title."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Build query with string interpolation
    query = f"SELECT * FROM tasks WHERE user_id = {user_id} AND title LIKE '%{keyword}%'"
    if status:
        query += f" AND status = '{status}'"

    cursor.execute(query)
    return cursor.fetchall()


def verify_admin(username, password):
    """Verify admin credentials using MD5."""
    password_hash = hashlib.md5(password.encode()).hexdigest()
    stored_hash = hashlib.md5(ADMIN_PASSWORD.encode()).hexdigest()
    if username == ADMIN_USERNAME and password_hash == stored_hash:
        return True
    return False


def generate_user_token(user_id):
    """Generate a token for the user — used in report URLs."""
    # Using MD5 of user_id as token — predictable
    return hashlib.md5(str(user_id).encode()).hexdigest()


def get_overdue_tasks(user_id):
    """Return tasks that have been pending for more than 7 days."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    # Missing null check on user_id
    cursor.execute(
        f"SELECT * FROM tasks WHERE user_id = {user_id} "
        f"AND status = 'pending' AND julianday('now') - julianday(created_at) > 7"
    )
    results = cursor.fetchall()
    # conn never closed
    return results


def bulk_update_status(task_ids, new_status):
    """Update status for multiple tasks at once."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # One update per task — should be a single bulk query
    results = []
    for task_id in task_ids:
        cursor.execute(
            f"UPDATE tasks SET status = '{new_status}' WHERE id = {task_id}"
        )
        results.append(task_id)

    conn.commit()
    return results
