from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from solver import solve_math
import sqlite3
import json
import os

app = Flask(__name__)
app.secret_key = "cs50_math_solver_secret_key_2024"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ─── DATABASE SETUP ─────────────────────────────

def get_db():
    conn = sqlite3.connect("math.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem TEXT NOT NULL,
            problem_type TEXT NOT NULL,
            result TEXT NOT NULL,
            steps TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# Create tables when app starts
init_db()

# ─── LOGIN REQUIRED ──────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ─── ROUTES ──────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    problem = data.get("problem", "").strip()
    problem_type = data.get("type", "auto")

    if not problem:
        return jsonify({"error": "Please enter a math problem."}), 400

    result = solve_math(problem, problem_type)

    # Save to history if logged in
    if session.get("user_id") and not result.get("error"):
        conn = get_db()
        conn.execute(
            "INSERT INTO history (user_id, problem, problem_type, result, steps) VALUES (?, ?, ?, ?, ?)",
            (
                session["user_id"],
                problem,
                result.get("type", problem_type),
                result.get("result", ""),
                json.dumps(result.get("steps", []))
            )
        )
        conn.commit()
        conn.close()

    return jsonify(result)


@app.route("/history")
@login_required
def history():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 50",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    history_list = []
    for row in rows:
        item = dict(row)
        item["steps"] = json.loads(item["steps"])
        history_list.append(item)

    return render_template("history.html", history=history_list)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        if not username:
            flash("Username is required.", "danger")
            return render_template("register.html")
        if not password:
            flash("Password is required.", "danger")
            return render_template("register.html")
        if password != confirmation:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        conn = get_db()
        existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            conn.close()
            flash("Username already taken.", "danger")
            return render_template("register.html")

        conn.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
        conn.close()
        flash("Registered successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if row is None or not check_password_hash(row["hash"], password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

        session["user_id"] = row["id"]
        session["username"] = row["username"]
        flash(f"Welcome back, {username}!", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
