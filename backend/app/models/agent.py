"""
Database models for AI agents and related entities.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.core.database import Base


class Agent(Base):
    """AI Agent model."""
    
    __tablename__ = "agents"
    
    id = Column(String(36), primary_key=True, index=True)
    agent_type = Column(String(50), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    capabilities = Column(JSON, nullable=True)
    configuration = Column(JSON, nullable=True)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = relationship("AgentSession", back_populates="agent")
    tasks = relationship("AgentTask", back_populates="agent")
    memories = relationship("AgentMemory", back_populates="agent")


class AgentSession(Base):
    """Agent session model."""
    
    __tablename__ = "agent_sessions"
    
    id = Column(String(36), primary_key=True, index=True)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=False)
    user_id = Column(String(36), nullable=True, index=True)
    session_id = Column(String(36), nullable=False, index=True)
    domain = Column(String(50), nullable=True)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, nullable=True)
    task_count = Column(Integer, default=0)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="sessions")
    tasks = relationship("AgentTask", back_populates="session")


class AgentTask(Base):
    """Agent task model."""
    
    __tablename__ = "agent_tasks"
    
    id = Column(String(36), primary_key=True, index=True)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=False)
    session_id = Column(String(36), ForeignKey("agent_sessions.id"), nullable=False)
    task_type = Column(String(50), nullable=False)
    priority = Column(String(20), default="medium")
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    status = Column(String(20), default="pending")
    confidence = Column(Float, nullable=True)
    reasoning = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    processing_time = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="tasks")
    session = relationship("AgentSession", back_populates="tasks")


class AgentMemory(Base):
    """Agent memory model."""
    
    __tablename__ = "agent_memories"
    
    id = Column(String(36), primary_key=True, index=True)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=False)
    memory_type = Column(String(20), nullable=False)  # short_term, long_term, pattern
    key = Column(String(255), nullable=False)
    value = Column(JSON, nullable=True)
    access_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="memories")


class AgentPerformance(Base):
    """Agent performance metrics model."""
    
    __tablename__ = "agent_performance"
    
    id = Column(String(36), primary_key=True, index=True)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=False)
    metric_name = Column(String(50), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String(20), nullable=False)  # counter, gauge, histogram
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    agent = relationship("Agent")


class AgentKnowledge(Base):
    """Agent knowledge integration model."""
    
    __tablename__ = "agent_knowledge"
    
    id = Column(String(36), primary_key=True, index=True)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=False)
    knowledge_type = Column(String(50), nullable=False)  # fact, rule, pattern, relationship
    content = Column(JSON, nullable=False)
    source = Column(String(100), nullable=True)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    agent = relationship("Agent")


class AgentLearning(Base):
    """Agent learning and adaptation model."""
    
    __tablename__ = "agent_learning"
    
    id = Column(String(36), primary_key=True, index=True)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=False)
    learning_type = Column(String(50), nullable=False)  # pattern, behavior, strategy
    input_data = Column(JSON, nullable=True)
    feedback = Column(JSON, nullable=True)
    adaptation = Column(JSON, nullable=True)
    success_rate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    agent = relationship("Agent")
