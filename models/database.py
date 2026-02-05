"""Database models for Project Chimera."""
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Task(Base):
    """Task table for audit logging."""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String, unique=True, nullable=False)
    agent_id = Column(String)  # Which agent created/processed
    action = Column(String)    # create, execute, evaluate, etc.
    status = Column(String)    # pending, in_progress, completed, failed
    confidence = Column(Float) # 0.0-1.0
    spec = Column(JSON)        # Task specification
    result = Column(JSON)      # Execution result
    error = Column(JSON)       # Error details if failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HITLReview(Base):
    """Human-in-the-Loop review queue."""
    __tablename__ = 'hitl_reviews'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String, unique=True, nullable=False)
    reason = Column(String)     # Why HITL required
    priority = Column(String)   # low, medium, high, critical
    status = Column(String)     # pending, reviewed, approved, rejected
    reviewer = Column(String)   # Human reviewer ID
    reviewed_at = Column(DateTime)
    decision = Column(JSON)     # Human decision
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
def init_db(db_url="postgresql://user:pass@localhost/chimera"):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
