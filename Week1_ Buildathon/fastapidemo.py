from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()


# Employee Model
class Employee(BaseModel):
    employee_id: str
    name: str
    email: str
    department: str

class LeaveRequest(BaseModel):
    employee_id: str
    leave_type: str
    start_date: str
    end_date: str
    reason: str

# GET - All Employees
@app.get("/employees")
def get_employees():

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT employee_id, name, email, department
    FROM employees
    """)

    rows = cursor.fetchall()

    conn.close()

    employees = []

    for row in rows:
        employees.append({
            "employee_id": row[0],
            "name": row[1],
            "email": row[2],
            "department": row[3]
        })

    return employees


# POST - Add Employee
@app.post("/employees")
def add_employee(employee: Employee):

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO employees
    (employee_id, name, email, department)
    VALUES (?, ?, ?, ?)
    """,
    (
        employee.employee_id,
        employee.name,
        employee.email,
        employee.department
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Employee Added Successfully"
    }


# PUT - Update Employee
@app.put("/employees/{employee_id}")
def update_employee(employee_id: str, employee: Employee):

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE employees
    SET name = ?, email = ?, department = ?
    WHERE employee_id = ?
    """,
    (
        employee.name,
        employee.email,
        employee.department,
        employee_id
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Employee Updated Successfully"
    }


# DELETE - Delete Employee
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM employees
    WHERE employee_id = ?
    """,
    (employee_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Employee Deleted Successfully"
    }
    
    
@app.post("/leave")
def apply_leave(leave: LeaveRequest):

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO leave_requests
    (
        employee_id,
        leave_type,
        start_date,
        end_date,
        reason
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        leave.employee_id,
        leave.leave_type,
        leave.start_date,
        leave.end_date,
        leave.reason
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Leave Applied Successfully"
    }
    
@app.get("/leave-history/{employee_id}")
def leave_history(employee_id: str):

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        employee_id,
        leave_type,
        start_date,
        end_date,
        reason,
        status
    FROM leave_requests
    WHERE employee_id = ?
    """,
    (employee_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    leaves = []

    for row in rows:
        leaves.append({
            "id": row[0],
            "employee_id": row[1],
            "leave_type": row[2],
            "start_date": row[3],
            "end_date": row[4],
            "reason": row[5],
            "status": row[6]
        })

    return leaves

@app.get("/pending-leaves")
def pending_leaves():

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        employee_id,
        leave_type,
        start_date,
        end_date,
        reason,
        status
    FROM leave_requests
    WHERE status = 'Pending'
    """)

    rows = cursor.fetchall()

    conn.close()

    leaves = []

    for row in rows:
        leaves.append({
            "id": row[0],
            "employee_id": row[1],
            "leave_type": row[2],
            "start_date": row[3],
            "end_date": row[4],
            "reason": row[5],
            "status": row[6]
        })

    return leaves

@app.put("/approve-leave/{leave_id}")
def approve_leave(leave_id: int):

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE leave_requests
    SET status = 'Approved'
    WHERE id = ?
    """,
    (leave_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Leave Approved Successfully"
    }
    
@app.put("/reject-leave/{leave_id}")
def reject_leave(leave_id: int):

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE leave_requests
    SET status = 'Rejected'
    WHERE id = ?
    """,
    (leave_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Leave Rejected Successfully"
    }
    
@app.get("/dashboard-stats")
def dashboard_stats():
        
    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    # Total Employees
    cursor.execute("""
    SELECT COUNT(*) FROM employees
    """)
    total_employees = cursor.fetchone()[0]

    # Total Leave Requests
    cursor.execute("""
    SELECT COUNT(*) FROM leave_requests
    """)
    total_leave_requests = cursor.fetchone()[0]

    # Pending Leave Requests
    cursor.execute("""
    SELECT COUNT(*) FROM leave_requests WHERE status = 'Pending'
    """)
    pending_leave_requests = cursor.fetchone()[0]

    conn.close()

    return {
        "total_employees": total_employees,
        "total_leave_requests": total_leave_requests,
        "pending_leave_requests": pending_leave_requests
    }   