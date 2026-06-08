from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.config import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user")
    org_id = Column(String, ForeignKey("organizations.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("OrganizationModel", back_populates="users")

class OrganizationModel(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    industry = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("UserModel", back_populates="organization")
    projects = relationship("ProjectModel", back_populates="organization")

class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    org_id = Column(String, ForeignKey("organizations.id"))
    name = Column(String)
    budget = Column(Float)
    status = Column(String, default="planning")
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("OrganizationModel", back_populates="projects")
    locations = relationship("LocationModel", back_populates="project")

class LocationModel(Base):
    __tablename__ = "locations"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    city = Column(String)
    state = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    rent_estimate = Column(Float, nullable=True)

    project = relationship("ProjectModel", back_populates="locations")

class SimulationModel(Base):
    __tablename__ = "simulations"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    query = Column(String)
    status = Column(String, default="completed")
    recommendation = Column(String)
    revenue_projection = Column(String) # Stored as JSON string
    risk_score = Column(String) # Stored as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("ProjectModel")
