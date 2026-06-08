from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid

class Organization(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    industry: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
