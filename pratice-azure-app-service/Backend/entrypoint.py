import os
import sys
import time
import subprocess
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

def wait_for_postgres():
    """Wait for Postgres to become available"""
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")

    print(f"Waiting for postgres at {host}:{port}...")
    
    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.close()
            print("Postgres is up - executing command")
            break
        except psycopg2.OperationalError:
            print("Postgres is unavailable - sleeping")
            time.sleep(1)

def run_migrations():
    """Run Alembic migrations"""
    print("Running database migrations...")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Migrations completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e}")
        sys.exit(1)

def start_app():
    """Start the Flask application"""
    print("Starting Flask application...")
    # Using subprocess to run Flask app with the current Python interpreter
    # This keeps the entrypoint process alive
    subprocess.run([sys.executable, "app.py"], check=True)

if __name__ == "__main__":
    wait_for_postgres()
    run_migrations()
    start_app()
