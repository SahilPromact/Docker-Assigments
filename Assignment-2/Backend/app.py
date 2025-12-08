from flask import Flask
import os
from dotenv import load_dotenv
from api.routes import api_bp
from db import db_session

load_dotenv()

app = Flask(__name__)

# Register API blueprint
app.register_blueprint(api_bp)

# Clean up scoped sessions after each request
@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove scoped session after each request"""
    db_session.remove()

if __name__ == "__main__":
    print("🚀 Starting Flask application...")
    with app.app_context():
        app.run(host="0.0.0.0", port=8000)
