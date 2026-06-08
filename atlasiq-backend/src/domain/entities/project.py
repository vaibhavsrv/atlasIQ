from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid

class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    org_id: str
    name: str
    budget: float
    status: str = "planning"
    created_at: datetime = Field(default_factory=datetime.utcnow)
