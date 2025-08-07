from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import List
from sqlalchemy.exc import IntegrityError

# ✅ Use relative import
from .database import SessionLocal, User, Task

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT config
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    description: str
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    description: str
    completed: bool
    user_id: int
    model_config = {
        "from_attributes": True
    }

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

# Signup
@app.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User created"}

# Login
@app.post("/login", response_model=TokenResponse)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# Create task
@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = Task(description=task.description, completed=task.completed, user_id=user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Get tasks
@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.user_id == user.id).all()

# Delete task
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

# Update task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.description = task.description
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return db_task
