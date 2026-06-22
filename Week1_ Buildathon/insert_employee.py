import sqlite3

conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO employees
(employee_id, name, email, department)
VALUES
('EMP001', 'Vimal', 'vimal@gmail.com', 'UX')
""")

conn.commit()
conn.close()

print("Employee Added")