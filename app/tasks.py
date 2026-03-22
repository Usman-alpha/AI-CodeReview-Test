"""
Task management — clean CRUD operations.
Good code: parameterized queries, proper error handling, pagination.
"""

from app.database import get_db

VALID_STATUSES = ("pending", "in_progress", "done", "cancelled")
VALID_PRIORITIES = (1, 2, 3)


def get_tasks_for_user(user_id: int, page: int = 1, per_page: int = 20) -> list[dict]:
    """Return paginated tasks for a user."""
    offset = (page - 1) * per_page
    with get_db() as conn:
        rows = conn.execute(
            """SELECT id, title, description, status, priority, created_at
               FROM tasks
               WHERE user_id = ?
               ORDER BY priority DESC, created_at DESC
               LIMIT ? OFFSET ?""",
            (user_id, per_page, offset)
        ).fetchall()
    return [dict(row) for row in rows]


def get_task(task_id: int, user_id: int) -> dict | None:
    """Return a single task, ensuring it belongs to the requesting user."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        ).fetchone()
    return dict(row) if row else None


def create_task(user_id: int, title: str, description: str = "",
                priority: int = 1) -> int:
    """Create a new task and return its ID."""
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Priority must be one of {VALID_PRIORITIES}")
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (user_id, title, description, priority) VALUES (?, ?, ?, ?)",
            (user_id, title, description, priority)
        )
        return cursor.lastrowid


def update_task_status(task_id: int, user_id: int, status: str) -> bool:
    """Update task status. Returns True if the task was found and updated."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Status must be one of {VALID_STATUSES}")
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?",
            (status, task_id, user_id)
        )
        return cursor.rowcount > 0


def delete_task(task_id: int, user_id: int) -> bool:
    """Delete a task. Returns True if found and deleted."""
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )
        return cursor.rowcount > 0
