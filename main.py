import psycopg2
import contextlib
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select
from pydantic import BaseModel
import uvicorn


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str

class TaskCreate(BaseModel):

    title: str
    description: str
  

app = FastAPI()

engine = create_engine("postgresql://ghulamshabbir1234567:ZwecNslv1id3@ep-long-rice-78270144.us-east-2.aws.neon.tech/fastapitodo?sslmode=require")

@contextlib.asynccontextmanager
async def lifespan(app):
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all(engine))


@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    db_task = Task(**task.__dict__) 
    with Session(engine) as session:
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        db_task.title = task.title
        db_task.description = task.description
        session.commit()
        session.refresh(db_task)
        return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(db_task)
        session.commit()
        return {"message": "Task deleted"}
    

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)