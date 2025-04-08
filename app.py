from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Get connection details from environment variables
DB_SERVER = os.environ.get("DB_SERVER")  # e.g. proj2-sql.database.windows.net
DB_NAME = os.environ.get("DB_NAME")      # e.g. proj2-db
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# SQL Server connection string
conn_str = f"Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{DB_SERVER},1433;Database={DB_NAME};Uid={DB_USERNAME};Pwd={DB_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

@app.route('/')
def home():
    return "Welcome to the Flask Web App connected to Azure SQL Database!"

@app.route('/employees')
def get_employees():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, department FROM employees")
        rows = cursor.fetchall()
        result = [{"id": r[0], "name": r[1], "department": r[2]} for r in rows]
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
