from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Task(BaseModel):
    subject: str
    description: str
    due_date: str
    assignee: str

def get_db():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           subject TEXT,
           description TEXT,
           due_date TEXT,
           assignee TEXT
        )"""
    )
    conn.commit()
    try:
        yield conn
    finally:
        conn.close()

@app.post("/create_task/")
def create_task(task: Task, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    query = "INSERT INTO tasks (subject, description, due_date, assignee) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (task.subject, task.description, task.due_date, task.assignee))
    conn.commit()
    return {"message": "Task created successfully"}

@app.get("/read_tasks/")
def read_tasks(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    task_list = []
    for task in tasks:
        task_dict = {
            "id": task[0],
            "subject": task[1],
            "description": task[2],
            "due_date": task[3],
            "assignee": task[4]
        }
        task_list.append(task_dict)
    return task_list

@app.put("/update_task/{task_id}")
def update_task(task_id: int, updated_task: Task, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    query = "UPDATE tasks SET subject=?, description=?, due_date=?, assignee=? WHERE id=?"
    cursor.execute(query, (updated_task.subject, updated_task.description, updated_task.due_date, updated_task.assignee, task_id))
    conn.commit()
    return {"message": f"Task {task_id} updated successfully"}

@app.delete("/delete_task/{task_id}")
def delete_task(task_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    query = "DELETE FROM tasks WHERE id=?"
    cursor.execute(query, (task_id,))
    conn.commit()
    return {"message": f"Task {task_id} deleted successfully"}