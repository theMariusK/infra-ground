from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, User
from crud import get_users, get_user_by_id, create_user, update_user, delete_user

from prometheus_fastapi_instrumentator import Instrumentator

# Logging
import logging
import logging_loki

handler = logging_loki.LokiHandler(
        url="http://172.21.0.8:3100/loki/api/v1/push", 
    tags={"application": "user-app"},
    version="1",
)

logger = logging.getLogger("tm-logger")
logger.addHandler(handler)
#

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

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info("Users have been read")
    users = get_users(db)
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/")
def create_user_endpoint(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    return create_user(db, user)

@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, new_data: dict, db: Session = Depends(get_db)):
    user = update_user(db, user_id, new_data)
    return user

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return {"message": "User deleted"}


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
