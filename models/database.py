from sqlalchemy import Column, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os

Base = declarative_base()

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(String, primary_key=True)
    objective = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    status = Column(String, default="active")
    
    # Relationship to tasks
    tasks = relationship("Task", back_populates="campaign")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String, primary_key=True)
    campaign_id = Column(String, ForeignKey('campaigns.id'))
    assigned_to = Column(String)
    action = Column(String)
    status = Column(String, default="pending")
    result = Column(String, nullable=True)

    # Relationship back to campaign
    campaign = relationship("Campaign", back_populates="tasks")

def init_db():
    db_url = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/chimera")
    engine = create_engine(db_url)
    # This is where the magic happens - it creates the tables
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()