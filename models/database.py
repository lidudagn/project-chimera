"""Database models for Project Chimera."""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Task(Base):
    """Task table for audit logging."""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String, unique=True, nullable=False)
    agent_id = Column(String)
    action = Column(String)
    status = Column(String)
    confidence = Column(Float)
    spec = Column(JSON)
    result = Column(JSON)
    error = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db(db_url=None):
    if db_url is None:
        if os.getenv("CHIMERA_ENV") == "testing":
            db_url = "sqlite:///:memory:"
        else:
            db_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/chimera")

    connect_args = {}
    if db_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    engine = create_engine(db_url, connect_args=connect_args)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
