from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from typing import Optional

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(50), default='investigator')
    department = Column(String(100))
    rank = Column(String(50))
    phone = Column(String(15))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    audit_logs = relationship('AuditLog', back_populates='user')
    assigned_cases = relationship('Case', back_populates='assigned_investigator')

class Case(Base):
    __tablename__ = 'cases'
    
    id = Column(Integer, primary_key=True)
    case_number = Column(String(20), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    fir_number = Column(String(50))
    police_station = Column(String(100))
    district = Column(String(50))
    state = Column(String(50))
    date_registered = Column(DateTime)
    status = Column(String(20), default='active')
    priority = Column(String(20), default='medium')
    assigned_to = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assigned_investigator = relationship('User', back_populates='assigned_cases')
    entities = relationship('Entity', back_populates='case')
    reports = relationship('Report', back_populates='case')

class Entity(Base):
    __tablename__ = 'entities'
    
    id = Column(Integer, primary_key=True)
    entity_id = Column(String(50), unique=True, nullable=False)
    entity_type = Column(String(30), nullable=False)
    case_id = Column(Integer, ForeignKey('cases.id'))
    name = Column(String(200))
    aliases = Column(Text)  # JSON array
    description = Column(Text)
    properties = Column(Text)  # JSON object
    confidence = Column(Float, default=0.5)
    priority_score = Column(Float, default=0)
    priority_level = Column(String(20), default='low')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    case = relationship('Case', back_populates='entities')
    relationships = relationship('Relationship', back_populates='source_entity', 
                                foreign_keys='Relationship.source_id')
    reverse_relationships = relationship('Relationship', back_populates='target_entity',
                                        foreign_keys='Relationship.target_id')

class Relationship(Base):
    __tablename__ = 'relationships'
    
    id = Column(Integer, primary_key=True)
    source_id = Column(String(50), ForeignKey('entities.entity_id'), nullable=False)
    target_id = Column(String(50), ForeignKey('entities.entity_id'), nullable=False)
    relationship_type = Column(String(50), nullable=False)
    properties = Column(Text)  # JSON object
    confidence = Column(Float, default=0.5)
    evidence_sources = Column(Text)  # JSON array
    timestamp = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    source_entity = relationship('Entity', foreign_keys=[source_id], back_populates='relationships')
    target_entity = relationship('Entity', foreign_keys=[target_id], back_populates='reverse_relationships')

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    report_id = Column(String(50), unique=True, nullable=False)
    case_id = Column(Integer, ForeignKey('cases.id'))
    report_type = Column(String(50))
    title = Column(String(200))
    content = Column(Text)
    source = Column(String(100))
    date_reported = Column(DateTime)
    priority = Column(String(20))
    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    case = relationship('Case', back_populates='reports')

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(50), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(50))
    details = Column(Text)  # JSON
    ip_address = Column(String(45))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='audit_logs')

class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    related_entity_id = Column(String(50))
    related_case_id = Column(String(50))
    generated_by = Column(String(50))
    status = Column(String(20), default='new')
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    resolved_by = Column(Integer, ForeignKey('users.id'))

# Database initialization
def init_database(db_url: str = "sqlite:///nexus.db"):
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()