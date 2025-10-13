from flask import Flask, jsonify
import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )


def initialize_database():
    """Create target database and items table if they do not exist."""
    try:
        # 1️⃣ Connect to the default 'postgres' database
        conn = psycopg2.connect(
            host=DB_HOST,
            database="postgres",
            user=DB_USER,
            password=DB_PASS
        )
        conn.autocommit = True
        cur = conn.cursor()

        # 2️⃣ Check if the target DB exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
        exists = cur.fetchone()

        # 3️⃣ Create it if not exists
        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cur.close()
        conn.close()

        # 4️⃣ Now connect to the target DB and create tables
        conn = get_db_connection()
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                source TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        cur.close()
        conn.close()
        print("Table 'items' ensured successfully.")

    except Exception as e:
        print("Error initializing database:", e)

@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/db-check")
def db_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        conn.close()
        return jsonify({"db_connection": "Db Connection Successful", "time": str(result)})
    except Exception as e:
        return jsonify({"db_connection": "failed", "error": str(e)})

@app.route("/items", methods=["GET"])
def get_items():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id, name, source, created_at FROM items ORDER BY id ASC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"items": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/add-item", methods=["POST"])
def add_item():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO items (name, source) VALUES (%s, %s) RETURNING id, name, source, created_at;",
            ("static item", "static"),
        )
        new_row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "added", "item": new_row}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Starting Flask application...")
    print(f"📊 Database config: Host={DB_HOST}, DB={DB_NAME}, User={DB_USER}")
    with app.app_context():
        initialize_database()
    app.run(host="0.0.0.0", port=8000)
