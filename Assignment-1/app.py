from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return f"Hello, Docker! ENV: {os.getenv('APP_ENV', 'development')}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
