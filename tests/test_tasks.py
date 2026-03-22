"""
Tests for task management — good test coverage.
"""

import pytest
import os
os.environ["DB_PATH"] = ":memory:"

from app.database import init_db
from app.auth import create_user
from app.tasks import (
    create_task, get_task, get_tasks_for_user,
    update_task_status, delete_task
)


@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield


@pytest.fixture
def user_id():
    return create_user("testuser", "test@example.com", "password123")


def test_create_task(user_id):
    task_id = create_task(user_id, "Write tests", priority=2)
    assert task_id > 0


def test_get_task(user_id):
    task_id = create_task(user_id, "Buy groceries")
    task = get_task(task_id, user_id)
    assert task is not None
    assert task["title"] == "Buy groceries"
    assert task["status"] == "pending"


def test_get_task_wrong_user(user_id):
    task_id = create_task(user_id, "Private task")
    result = get_task(task_id, user_id + 999)
    assert result is None


def test_update_task_status(user_id):
    task_id = create_task(user_id, "Deploy app")
    updated = update_task_status(task_id, user_id, "in_progress")
    assert updated is True
    task = get_task(task_id, user_id)
    assert task["status"] == "in_progress"


def test_invalid_status_raises(user_id):
    task_id = create_task(user_id, "Test task")
    with pytest.raises(ValueError):
        update_task_status(task_id, user_id, "flying")


def test_delete_task(user_id):
    task_id = create_task(user_id, "Temp task")
    deleted = delete_task(task_id, user_id)
    assert deleted is True
    assert get_task(task_id, user_id) is None


def test_pagination(user_id):
    for i in range(25):
        create_task(user_id, f"Task {i}")
    page1 = get_tasks_for_user(user_id, page=1, per_page=10)
    page2 = get_tasks_for_user(user_id, page=2, per_page=10)
    assert len(page1) == 10
    assert len(page2) == 10
