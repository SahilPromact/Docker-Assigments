from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Item

load_dotenv()

app = Flask(__name__)

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

# Create SQLAlchemy engine
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Use scoped_session for thread-safe sessions
db_session = scoped_session(SessionLocal)


def get_db():
    """Get a database session"""
    return db_session()


@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/db-check")
def db_check():
    db = get_db()
    try:
        result = db.execute(text("SELECT NOW();")).fetchone()
        return jsonify({"db_connection": "Db Connection Successful", "time": str(result[0])})
    except Exception as e:
        return jsonify({"db_connection": "failed", "error": str(e)})
    finally:
        db.close()

@app.route("/items", methods=["GET"])
def get_items():
    db = get_db()
    try:
        items = db.query(Item).order_by(Item.id.asc()).all()
        return jsonify({"items": [item.to_dict() for item in items]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@app.route("/add-item", methods=["POST"])
def add_item():
    db = get_db()
    try:
        new_item = Item(name="static item", source="static")
        db.add(new_item)
        db.commit()
        db.refresh(new_item)  # Refresh to get the generated id and created_at
        return jsonify({"status": "added", "item": new_item.to_dict()}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting Flask application...")
    with app.app_context():
        app.run(host="0.0.0.0", port=8000)
