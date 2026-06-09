from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.config import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String)
    is_verified = Column(String, default="false")
    role = Column(String, default="user")
    org_id = Column(String, ForeignKey("organizations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("OrganizationModel", back_populates="users")

class OtpModel(Base):
    __tablename__ = "otps"
    
    id = Column(String, primary_key=True, index=True)
    identifier = Column(String, index=True) # Email or Phone
    otp_code = Column(String)
    expires_at = Column(DateTime)
    is_used = Column(String, default="false")
    created_at = Column(DateTime, default=datetime.utcnow)

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

class ForecastModel(Base):
    __tablename__ = "forecasts"
    id = Column(String, primary_key=True, index=True)
    simulation_id = Column(String, ForeignKey("simulations.id"))
    time_series_data = Column(String) # JSON string of Prophet arrays
    created_at = Column(DateTime, default=datetime.utcnow)

class CompetitorModel(Base):
    __tablename__ = "competitors"
    id = Column(String, primary_key=True, index=True)
    location_id = Column(String, ForeignKey("locations.id"))
    name = Column(String)
    distance = Column(Float)
    threat_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class DocumentModel(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    filename = Column(String)
    content_type = Column(String)
    vector_id = Column(String) # Ref to Qdrant
    created_at = Column(DateTime, default=datetime.utcnow)

class IndustryBenchmarkModel(Base):
    __tablename__ = "industry_benchmarks"
    id = Column(String, primary_key=True, index=True)
    industry_name = Column(String, unique=True, index=True)
    avg_revenue = Column(Float)
    avg_rent = Column(Float)
    avg_cac = Column(Float)
    avg_margins = Column(Float)
    risk_multiplier = Column(Float)
    growth_rate = Column(Float)

class KnowledgeGraphModel(Base):
    __tablename__ = "knowledge_graph"
    id = Column(String, primary_key=True, index=True)
    entity_id = Column(String, index=True)
    node_type = Column(String)
    relations = Column(String) # JSON
    created_at = Column(DateTime, default=datetime.utcnow)

class NotificationModel(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    message = Column(String)
    is_read = Column(String, default="false")
    created_at = Column(DateTime, default=datetime.utcnow)

class ReportModel(Base):
    __tablename__ = "reports"
    id = Column(String, primary_key=True, index=True)
    simulation_id = Column(String, ForeignKey("simulations.id"))
    pdf_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
