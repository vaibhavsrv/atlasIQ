from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from src.infrastructure.database.config import Base, engine
from src.presentation.api.router import router as simulation_router
from src.presentation.api.projects import router as projects_router

# Create all tables (in a real app, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AtlasIQ API",
    description="Backend API for AtlasIQ Business Expansion Operating System",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation_router)
app.include_router(projects_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AtlasIQ API is running"}
