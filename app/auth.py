"""
Authentication helpers.
Clean implementation — good code.
"""

import hashlib
import hmac
import os
import secrets
from app.database import get_db


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with a random salt."""
    salt = secrets.token_hex(32)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(stored: str, password: str) -> bool:
    """Verify a password against a stored hash."""
    try:
        salt, hashed = stored.split(":", 1)
    except ValueError:
        return False
    expected = hashlib.sha256((salt + password).encode()).hexdigest()
    return hmac.compare_digest(expected, hashed)


def get_user_by_id(user_id: int) -> dict | None:
    """Return a user dict or None if not found."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, username, email, role FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
    return dict(row) if row else None


def get_user_by_username(username: str) -> dict | None:
    """Return a user dict or None if not found."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, username, email, password, role FROM users WHERE username = ?",
            (username,)
        ).fetchone()
    return dict(row) if row else None


def create_user(username: str, email: str, password: str, role: str = "user") -> int:
    """Insert a new user and return the new user ID."""
    password_hash = hash_password(password)
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, role)
        )
        return cursor.lastrowid
