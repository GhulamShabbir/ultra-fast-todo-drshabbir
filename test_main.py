from fastapi.testclient import TestClient
from main import app, Task, TaskCreate, engine
from sqlmodel import Session, select

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert "id" in data

def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200

def test_read_task():
    with Session(engine) as session:
        task = session.exec(select(Task)).first()
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200

def test_update_task():
    with Session(engine) as session:
        task = session.exec(select(Task)).first()
    response = client.put(f"/tasks/{task.id}", json={"title": "Updated Task", "description": "This is an updated task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "This is an updated task"

def test_delete_task():
    with Session(engine) as session:
        task = session.exec(select(Task)).first()
    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 200



def test_read_task_not_found():
    # Try to read a task that doesn't exist
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_update_task_not_found():
    # Try to update a task that doesn't exist
    response = client.put("/tasks/9999", json={"title": "Nonexistent Task", "description": "This task doesn't exist"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_task_not_found():
    # Try to delete a task that doesn't exist
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}