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
import sqlite3
import smtplib

# Hardcoded secrets (violates: "Never hardcode API keys or secrets")
STRIPE_SECRET_KEY = "sk-test-hardcoded-secret-12345"
DB_PASSWORD = "admin123"

def get_payment(payment_id):
    # No type hints (violates: "All functions must have type hints")
    # DB connection never closed (violates: "All database connections must be closed after use")
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()

    # SQL injection (violates: "All SQL queries must use parameterized queries")
    query = "SELECT * FROM payments WHERE id = " + str(payment_id)
    cursor.execute(query)
    result = cursor.fetchone()

    # print() instead of logger (violates: "Never use print() — use the logger")
    print(f"Fetched payment: {result}")

    return result


def hash_card_number(card_number):
    # No type hints
    # MD5 for hashing (violates: "Never use MD5 for password hashing")
    return hashlib.md5(card_number.encode()).hexdigest()


def process_payment(user_id, amount, card_number, cvv):
    # No type hints
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()

    # Logging sensitive data (violates: "Never log sensitive data: card numbers, CVV")
    print(f"Processing payment for user {user_id}: card={card_number}, cvv={cvv}, amount={amount}")

    # SQL injection
    cursor.execute(
        "INSERT INTO payments (user_id, amount) VALUES (" + str(user_id) + ", " + str(amount) + ")"
    )

    # MD5 hash of card number
    card_hash = hashlib.md5(card_number.encode()).hexdigest()

    # SQL injection again
    cursor.execute(
        "UPDATE users SET last_card_hash = '" + card_hash + "' WHERE id = " + str(user_id)
    )

    conn.commit()
    # Connection never closed

    # print instead of logger
    print(f"Payment processed. Card hash stored: {card_hash}")

    return {"status": "success", "amount": amount}


def send_receipt(email, amount, card_number):
    # No type hints
    # Logging sensitive data
    print(f"Sending receipt to {email} for amount {amount}, card: {card_number}")

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.login("noreply@company.com", "hardcoded-smtp-password")
    smtp.sendmail("noreply@company.com", email, f"Receipt: ${amount}")
    # smtp never closed
