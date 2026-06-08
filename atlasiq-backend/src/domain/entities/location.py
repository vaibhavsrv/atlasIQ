from typing import Optional
from pydantic import BaseModel, Field
import uuid

class Location(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float
    rent_estimate: Optional[float] = None
