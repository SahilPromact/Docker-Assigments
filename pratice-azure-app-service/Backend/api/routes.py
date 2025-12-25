from flask import Blueprint, jsonify, request
from sqlalchemy import text
from models import Item
from db import get_db

api_bp = Blueprint('api', __name__)

@api_bp.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@api_bp.route("/db-check")
def db_check():
    db = get_db()
    try:
        result = db.execute(text("SELECT NOW();")).fetchone()
        return jsonify({"db_connection": "Db Connection Successful", "time": str(result[0])})
    except Exception as e:
        return jsonify({"db_connection": "failed", "error": str(e)})
    finally:
        db.close()

@api_bp.route("/items", methods=["GET"])
def get_items():
    db = get_db()
    try:
        items = db.query(Item).order_by(Item.id.asc()).all()
        return jsonify({"items": [item.to_dict() for item in items]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@api_bp.route("/add-item", methods=["POST"])
def add_item():
    db = get_db()
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get("name")
        source = data.get("source")
        
        if not name or not source:
            return jsonify({"error": "Both 'name' and 'source' are required"}), 400
        
        new_item = Item(name=name, source=source)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return jsonify({"status": "added", "item": new_item.to_dict()}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
