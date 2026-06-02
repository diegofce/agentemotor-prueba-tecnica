from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AdvisorCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    email: str | None = Field(default=None, max_length=200)


class AdvisorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str | None
    created_at: datetime
