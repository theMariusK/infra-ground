from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Task
from crud import get_tasks, get_task_by_id, create_task, update_task, delete_task
from datetime import date, timedelta

from prometheus_fastapi_instrumentator import Instrumentator

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI()
instrumentator = Instrumentator().instrument(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.on_event("startup")
async def startup():
    instrumentator.expose(app, endpoint='/metrics', tags=['metrics'])

@app.get("/tasks/")
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = get_tasks(db)
    return tasks

@app.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks/")
def create_task_endpoint(title: str, description: str, user_id: int, db: Session = Depends(get_db)):
    task = Task(title=title, description=description, due_date=(date.today() + timedelta(7)), user_id=user_id)
    return create_task(db, task)

@app.put("/tasks/{task_id}")
def update_user_endpoint(task_id: int, new_data: dict, db: Session = Depends(get_db)):
    task = update_task(db, task_id, new_data)
    return task

@app.delete("/tasks/{task_id}")
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task_user(db, task_id)
    return {"message": "Task deleted"}


#### CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
####
