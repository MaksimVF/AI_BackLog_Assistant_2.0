

"""
Database Models for AI Backlog Assistant

This module defines the SQLAlchemy ORM models for PostgreSQL database.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Task(Base):
    """Task model for storing backlog tasks"""
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(50), unique=True, index=True)
    input_data = Column(Text, nullable=False)
    task_metadata = Column(JSON, nullable=True)
    status = Column(String(50), default='pending')
    classification = Column(String(50), nullable=True)
    risk_score = Column(Float, nullable=True)
    impact_score = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    urgency_score = Column(Float, nullable=True)
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    files = relationship("TaskFile", back_populates="task")
    triggers = relationship("Trigger", back_populates="task")

class TaskFile(Base):
    """Task file model for storing file references"""
    __tablename__ = 'task_files'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(50), ForeignKey('tasks.task_id'), index=True)
    file_url = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=True)
    s3_key = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    task = relationship("Task", back_populates="files")

class Trigger(Base):
    """Trigger model for storing task triggers"""
    __tablename__ = 'triggers'

    id = Column(Integer, primary_key=True, index=True)
    trigger_id = Column(String(50), unique=True, index=True)
    task_id = Column(String(50), ForeignKey('tasks.task_id'), index=True)
    reason = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    task = relationship("Task", back_populates="triggers")
