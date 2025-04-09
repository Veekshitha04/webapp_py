from flask import Flask, request
import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# DB connection string
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=proj2-sql.database.windows.net;'
    'DATABASE=proj2-db;'
    'UID=proj1_admin;'
    'PWD=Proj@123#12;'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ''
    if request.method == 'POST':
        dept = request.form.get('dept')
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, department FROM employees WHERE department = ?", dept)
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                result = f"<p>No employees found in department: <b>{dept}</b></p>"
            else:
                result = f"<h3>Employees in department: <b>{dept}</b></h3><ul>"
                for r in rows:
                    result += f"<li>{r[0]} - {r[1]}</li>"
                result += "</ul>"
        except Exception as e:
            result = f"<p>Error: {str(e)}</p>"

    return f"""
    <html>
        <head><title>Department Employee Lookup</title></head>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h1>🎉 Welcome to the Flask Web App 🎉</h1>
            <p>Connected to Azure SQL Database</p>
            <form method="POST">
                <label>Enter Department: </label>
                <input type="text" name="dept" required>
                <button type="submit">Submit</button>
            </form>
            <div style="margin-top: 30px;">{result}</div>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
