"""
Payments module — intentionally violates custom rules for testing.

Violations included:
  - Hardcoded API secret key
  - MD5 for hashing
  - SQL injection via string formatting
  - print() instead of logger
  - No type hints
  - DB connection never closed
  - Sensitive data logged
"""

import hashlib
import smtplib
import sqlite3

# Hardcoded secrets (violates: "Never hardcode API keys or secrets")
STRIPE_SECRET_KEY = "sk-test-hardcoded-secret-12345"
DB_PASSWORD = "admin123"

from typing import Optional

def get_payment(payment_id: int) -> Optional[tuple]:
def hash_card_number(card_number: str) -> str:
try:
    query = "SELECT id, user_id, amount, status, created_at FROM payments WHERE id = ?"
    cursor.execute(query, (payment_id,))
    cursor.execute('SELECT id, user_id, amount, status, created_at FROM payments WHERE id = ?', (payment_id,))
    if conn:
        conn.close()
    raise RuntimeError(f"Database error: {e}") from e
    cursor.execute(query)
    logger.debug("Fetched payment id=%s, found=%s", payment_id, result is not None)
    logger.info("Payment processed. Card hash stored for user id=%s", user_id)
    logger.info("Sending receipt to user id=%s amount=%s", user_id, amount)
    return result


def hash_card_number(card_number: str) -> str:
    # No type hints
    # MD5 for hashing (violates: "Never use MD5 for password hashing")
    return hashlib.md5(card_number.encode()).hexdigest()


def process_payment(user_id: int, amount: float, card_number: str, cvv: str) -> dict:
    # No type hints
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()

    # Logging sensitive data (violates: "Never log sensitive data: card numbers, CVV")
    print(f"Processing payment for user {user_id}: card={card_number}, cvv={cvv}, amount={amount}")

try:
    cursor.execute(
        "INSERT INTO payments (user_id, amount) VALUES (?, ?)",
        (user_id, amount)
    )

    cursor.execute(

        "UPDATE users SET last_card_hash = ? WHERE id = ?",

        (card_hash, user_id)

    )

    conn.commit()

except Exception as e:
    logger.error(f"Payment processing failed for user {user_id}: {e}", exc_info=True)
    conn.rollback()
    raise
    raise

finally:

    conn.close()
    cursor.execute(
        "UPDATE users SET last_card_hash = '" + card_hash + "' WHERE id = " + str(user_id)
    )

    conn.commit()
    # Connection never closed

    # print instead of logger
    logger.info('Payment processed. Card hash stored for user id=%s', user_id)

    return {"status": "success", "amount": amount}


def send_receipt(email: str, amount: float, card_number: str) -> None:
    # No type hints
    # Logging sensitive data
    print(f"Sending receipt to {email} for amount {amount}, card: {card_number}")

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.login("noreply@company.com", "hardcoded-smtp-password")
    smtp.sendmail("noreply@company.com", email, f"Receipt: ${amount}")
    # smtp never closed
