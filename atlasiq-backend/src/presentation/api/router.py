from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import json
from reportlab.pdfgen import canvas
import io
from src.infrastructure.ai.orchestrator import run_simulation
from src.infrastructure.database.config import get_db
from src.infrastructure.database.repositories import SimulationRepository

router = APIRouter(prefix="/api/v1/simulations", tags=["simulations"])

class SimulationRequest(BaseModel):
    project_id: str
    query: str

from src.infrastructure.database.models import ForecastModel

class SimulationResponse(BaseModel):
    id: str
    project_id: str
    query: str
    status: str
    recommendation: str
    revenue_projection: dict
    risk_score: dict
    forecast_data: list = []

@router.get("", response_model=List[SimulationResponse])
def get_simulations(db: Session = Depends(get_db)):
    repo = SimulationRepository(db)
    sims = repo.get_all()
    return [
        SimulationResponse(
            id=s.id, project_id=s.project_id, query=s.query, status=s.status,
            recommendation=s.recommendation,
            revenue_projection=json.loads(s.revenue_projection),
            risk_score=json.loads(s.risk_score)
        ) for s in sims
    ]

@router.get("/{id}", response_model=SimulationResponse)
def get_simulation(id: str, db: Session = Depends(get_db)):
    repo = SimulationRepository(db)
    s = repo.get_by_id(id)
    if not s:
        raise HTTPException(status_code=404, detail="Simulation not found")
        
    forecast_record = db.query(ForecastModel).filter(ForecastModel.simulation_id == id).first()
    forecast_data = json.loads(forecast_record.time_series_data) if forecast_record else []
    
    return SimulationResponse(
        id=s.id, project_id=s.project_id, query=s.query, status=s.status,
        recommendation=s.recommendation,
        revenue_projection=json.loads(s.revenue_projection),
        risk_score=json.loads(s.risk_score),
        forecast_data=forecast_data
    )

@router.post("/run", response_model=SimulationResponse)
def run_what_if_simulation(request: SimulationRequest, db: Session = Depends(get_db)):
    try:
        from src.infrastructure.database.repositories import ProjectRepository
        proj_repo = ProjectRepository(db)
        project = proj_repo.get_by_id(request.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        result = run_simulation(project_id=request.project_id, query=request.query, budget=project.budget)
        repo = SimulationRepository(db)
        s = repo.create(
            project_id=request.project_id,
            query=request.query,
            recommendation=result.get("final_strategy", ""),
            revenue_projection=result.get("revenue_projection", {}),
            risk_score=result.get("risk_score", {}),
            forecast_data=result.get("forecast_data", [])
        )
        return SimulationResponse(
            id=s.id, project_id=s.project_id, query=s.query, status=s.status,
            recommendation=s.recommendation,
            revenue_projection=json.loads(s.revenue_projection),
            risk_score=json.loads(s.risk_score),
            forecast_data=result.get("forecast_data", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}/export")
def export_simulation_pdf(id: str, db: Session = Depends(get_db)):
    repo = SimulationRepository(db)
    s = repo.get_by_id(id)
    if not s:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"AtlasIQ Simulation Report")
    p.drawString(100, 780, f"Scenario: {s.query}")
    p.drawString(100, 760, f"Recommendation: {s.recommendation[:50]}...")
    
    rev = json.loads(s.revenue_projection)
    if "year_1_roi" in rev:
        p.drawString(100, 740, f"Projected ROI: {rev['year_1_roi']}%")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=simulation_{id}.pdf"})
