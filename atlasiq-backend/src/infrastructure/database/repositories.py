from sqlalchemy.orm import Session
from src.infrastructure.database.models import ProjectModel, SimulationModel
import uuid
import json

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(ProjectModel).all()

    def get_by_id(self, project_id: str):
        return self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()

    def create(self, name: str, budget: float, org_id: str = "default-org"):
        db_project = ProjectModel(
            id=str(uuid.uuid4()),
            name=name,
            budget=budget,
            org_id=org_id
        )
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def update(self, project_id: str, name: str, budget: float, status: str):
        db_project = self.get_by_id(project_id)
        if db_project:
            db_project.name = name
            db_project.budget = budget
            db_project.status = status
            self.db.commit()
            self.db.refresh(db_project)
        return db_project

    def delete(self, project_id: str):
        db_project = self.get_by_id(project_id)
        if db_project:
            self.db.delete(db_project)
            self.db.commit()
            return True
        return False

class SimulationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(SimulationModel).order_by(SimulationModel.created_at.desc()).all()

    def get_by_id(self, simulation_id: str):
        return self.db.query(SimulationModel).filter(SimulationModel.id == simulation_id).first()

    def create(self, project_id: str, query: str, recommendation: str, revenue_projection: dict, risk_score: dict):
        db_sim = SimulationModel(
            id=str(uuid.uuid4()),
            project_id=project_id,
            query=query,
            recommendation=recommendation,
            revenue_projection=json.dumps(revenue_projection),
            risk_score=json.dumps(risk_score)
        )
        self.db.add(db_sim)
        self.db.commit()
        self.db.refresh(db_sim)
        return db_sim
