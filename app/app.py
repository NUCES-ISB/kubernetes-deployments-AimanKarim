from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Get database credentials from environment variables
DB_URL = os.getenv("DATABASE_URL")

def connect_db():
    try:
        conn = psycopg2.connect(DB_URL)
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

@app.route("/")
def home():
    return jsonify({"message": "Flask App Running in Kubernetes!"})

@app.route("/db-test")
def db_test():
    conn = connect_db()
    if conn:
        return jsonify({"message": "Database Connected Successfully!"})
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
