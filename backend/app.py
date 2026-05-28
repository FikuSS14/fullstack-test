from flask import Flask, Response, request
from flask_cors import CORS
import json
import sqlite3
import os
import re

app = Flask(__name__)
CORS(app)

DATABASE = os.path.join(os.path.dirname(__file__), "database.db")


def get_db_connection():
    """Создаёт и возвращает соединение с базой данных SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализирует базу данных: создаёт таблицу users и тестовых пользователей."""
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Иван Петров", "ivan@example.com"),
    )
    conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Мария Сидорова", "maria@example.com"),
    )
    conn.commit()
    conn.close()
    print("База данных создана, таблица users готова, добавлены тестовые пользователи")


@app.route("/")
def home():
    """Проверочный эндпоинт для проверки работоспособности сервера."""
    return "Сервер робит!"


@app.route("/users", methods=["GET"])
def get_users():
    """Возвращает список всех пользователей в формате JSON."""
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()

    users_list = [dict(user) for user in users]
    return Response(
        json.dumps(users_list, ensure_ascii=False, indent=2),
        mimetype="application/json",
    )


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Возвращает пользователя по ID или 404, если не найден."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()

    if user is None:
        return Response(
            json.dumps(
                {"error": f"Пользователь с id {user_id} не найден"}, ensure_ascii=False
            ),
            status=404,
            mimetype="application/json",
        )

    return Response(
        json.dumps(dict(user), ensure_ascii=False, indent=2),
        status=200,
        mimetype="application/json",
    )


@app.route("/users", methods=["POST"])
def create_user():
    """Создаёт нового пользователя. Ожидает JSON с полями name и email."""
    try:
        data = json.loads(request.data)
    except json.JSONDecodeError:
        return Response(
            json.dumps({"error": "Неверный формат JSON"}, ensure_ascii=False),
            status=400,
            mimetype="application/json",
        )

    if "name" not in data or "email" not in data:
        return Response(
            json.dumps(
                {"error": "Поля 'name' и 'email' обязательны"}, ensure_ascii=False
            ),
            status=400,
            mimetype="application/json",
        )

    name = data["name"].strip()
    email = data["email"].strip().lower()

    # Строгая валидация email через регулярное выражение
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, email):
        return Response(
            json.dumps(
                {"error": "Некорректный формат email. Пример: user@example.com"},
                ensure_ascii=False,
            ),
            status=400,
            mimetype="application/json",
        )

    if not name:
        return Response(
            json.dumps({"error": "Имя не может быть пустым"}, ensure_ascii=False),
            status=400,
            mimetype="application/json",
        )

    try:
        conn = get_db_connection()
        cursor = conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)", (name, email)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return Response(
            json.dumps(
                {
                    "message": "Пользователь успешно создан",
                    "user": {"id": user_id, "name": name, "email": email},
                },
                ensure_ascii=False,
                indent=2,
            ),
            status=201,
            mimetype="application/json",
        )
    except sqlite3.IntegrityError:
        return Response(
            json.dumps(
                {"error": f"Пользователь с email '{email}' уже существует"},
                ensure_ascii=False,
            ),
            status=409,
            mimetype="application/json",
        )


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
