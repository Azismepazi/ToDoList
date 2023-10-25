from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()
# Create a SQLite database and connect to it
conn = sqlite3.connect("todo.db") #:-- This line establishes a connection to a SQLite database file named "todo.db."
#If the file doesn't exist, it will be created. If it does exist, the code connects to it. 
#The conn variable is an SQLite database connection object that you can use to interact with the database.
cursor = conn.cursor() # --The cursor is a control structure used to execute SQL statements
#and fetch data from the database. It allows you to interact with the database by executing SQL commands.
# *Create a table to store the tasks*       
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

class Task(BaseModel):
    subject: str
    description: str
    due_date: str
    assignee: str

# CREATE: Add a new todo item to the DB
@app.post("/create_task/")
def create_task(task: Task):
    query = "INSERT INTO tasks (subject, description, due_date, assignee) VALUES (?, ?, ?, ?)"
    #This line defines an SQL query that inserts a new row into the "tasks" table of your SQLite database.
    # It specifies the columns to insert data into and uses placeholders (?) for the values.
    cursor.execute(query, (task.subject, task.description, task.due_date, task.assignee))
    conn.commit()
    return {"message": "Task created successfully"}

# READ: Read all todo items from the DB
@app.get("/read_tasks/")
def read_tasks():
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

# UPDATE: Update an existing todo item by ID
@app.put("/update_task/{task_id}")
def update_task(task_id: int, updated_task: Task):
    query = "UPDATE tasks SET subject=?, description=?, due_date=?, assignee=? WHERE id=?"
    cursor.execute(query, (updated_task.subject, updated_task.description, updated_task.due_date, updated_task.assignee, task_id))
    conn.commit()
    return {"message": f"Task {task_id} updated successfully"}

# DELETE: Delete an existing todo item by ID
@app.delete("/delete_task/{task_id}")
def delete_task(task_id: int):
    query = "DELETE FROM tasks WHERE id=?"
    cursor.execute(query, (task_id,))
    conn.commit()
    return {"message": f"Task {task_id} deleted successfully"}