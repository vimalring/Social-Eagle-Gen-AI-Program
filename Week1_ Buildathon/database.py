import sqlite3

conn = sqlite3.connect("employee.db")

cursor = conn.cursor()

# Employees Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT UNIQUE,
    name TEXT,
    email TEXT,
    department TEXT
)
""")

# Managers Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS managers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manager_id TEXT UNIQUE,
    name TEXT,
    email TEXT
)
""")

# Leave Requests Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    leave_type TEXT,
    start_date TEXT,
    end_date TEXT,
    reason TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

conn.commit()

conn.close()

print("All Tables Created Successfully")