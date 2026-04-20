from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
import time

app = Flask(__name__)
CORS(app)

def get_db_connection():
    """Attempt to connect to the MySQL database."""
    connection = None
    # Retry mechanism for DB connection
    for _ in range(5):
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'db'),
                user=os.getenv('DB_USER', 'user'),
                password=os.getenv('DB_PASSWORD', 'password'),
                database=os.getenv('DB_NAME', 'test_db')
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            time.sleep(2)
    return None

@app.route('/')
def home():
    return "Backend running"

@app.route('/db')
def db_status():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            
            # Fetch some sample data if table exists
            cursor.execute("SHOW TABLES LIKE 'users';")
            table_exists = cursor.fetchone()
            
            users = []
            if table_exists:
                cursor.execute("SELECT * FROM users;")
                users = cursor.fetchall()
                
            return jsonify({
                "status": "connected",
                "database": db_name['DATABASE()'],
                "users": users
            })
        except Error as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({"status": "error", "message": "Could not connect to database"}), 500

@app.route('/add', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    
    if not username or not email:
        return jsonify({"status": "error", "message": "Username and Email are required"}), 400
        
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
            conn.commit()
            return jsonify({"status": "success", "message": "User added successfully!"})
        except Error as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        finally:
            conn.close()
    else:
        return jsonify({"status": "error", "message": "Could not connect to database"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
