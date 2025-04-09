from flask import Flask, request, jsonify, render_template_string
import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# SQL connection string (using hardcoded values or env vars)
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=proj2-sql.privatelink.database.windows.net;'
    'DATABASE=proj2-db;'
    'UID=proj1_admin;'
    'PWD=Proj@123#12;'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
)

@app.route('/')
def home():
    html = """
    <html>
        <head>
            <title>Department Search</title>
        </head>
        <body style="text-align: center; padding-top: 100px; font-family: Arial;">
            <h2>🔍 Employee Lookup</h2>
            <form action="/search" method="post">
                <input type="text" name="department" placeholder="Enter department name" required />
                <button type="submit">Search</button>
            </form>
        </body>
    </html>
    """
    return html

@app.route('/search', methods=['POST'])
def search_employees():
    dept = request.form['department']
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM employees WHERE department = ?", (dept,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return f"<h3>No employees found in department: {dept}</h3>"

        result_html = f"<h3>Employees in '{dept}' department:</h3><ul>"
        for r in rows:
            result_html += f"<li>{r[0]} - {r[1]}</li>"
        result_html += "</ul><a href='/'>🔙 Go back</a>"

        return result_html
    except Exception as e:
        return f"<h3>Error: {e}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
