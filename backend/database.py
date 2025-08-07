from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# Base class
class Base(DeclarativeBase):
    pass

# User model
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]

# Task model
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

# SQLite engine and session
engine = create_engine("sqlite:///tasks.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create tables
Base.metadata.create_all(bind=engine)
