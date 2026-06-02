from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ClientCreate(BaseModel):
    advisor_id: int = Field(..., gt=0)
    full_name: str = Field(..., min_length=1, max_length=200)
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=200)


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    advisor_id: int
    full_name: str
    phone: str | None
    email: str | None
    created_at: datetime
