"""
Flask API endpoints — NEW FEATURE
Exposes reporting endpoints.
"""

from flask import Flask, request, jsonify
from app.reports import (
    get_user_report, get_admin_summary,
    search_tasks, verify_admin, generate_user_token,
    get_overdue_tasks, bulk_update_status
)

app = Flask(__name__)

# Debug mode left on — exposes stack traces in production
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "hardcoded-flask-secret-do-not-use"


@app.route("/report/<username>")
def user_report(username):
    """Get report for a user — no authentication required."""
    report = get_user_report(username)
    # No auth check — any user can view any other user's report (IDOR)
    return jsonify(report)


@app.route("/admin/summary")
def admin_summary():
    """Admin summary — checks credentials from query string."""
    username = request.args.get("username")
    password = request.args.get("password")
    # Credentials sent in URL — visible in logs and browser history
    if not verify_admin(username, password):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(get_admin_summary())


@app.route("/tasks/search")
def search():
    """Search tasks for a user."""
    user_id = request.args.get("user_id")
    keyword = request.args.get("keyword", "")
    status  = request.args.get("status")
    # user_id passed directly to SQL without validation or auth
    results = search_tasks(user_id, keyword, status)
    return jsonify(results)


@app.route("/tasks/bulk-update", methods=["POST"])
def bulk_update():
    """Bulk update task statuses."""
    data = request.json
    task_ids  = data["task_ids"]   # No validation — KeyError if missing
    new_status = data["status"]
    # No ownership check — any user can update any task
    updated = bulk_update_status(task_ids, new_status)
    return jsonify({"updated": updated})


@app.route("/user/token/<int:user_id>")
def get_token(user_id):
    """Return an access token for a user."""
    token = generate_user_token(user_id)
    # Exposes predictable MD5-based token publicly
    return jsonify({"token": token, "user_id": user_id})


@app.route("/overdue/<int:user_id>")
def overdue(user_id):
    """Get overdue tasks for a user."""
    tasks = get_overdue_tasks(user_id)
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
