from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ActionType = Literal[
    "call_no_answer",
    "call_success",
    "renewal_scheduled",
    "renewed",
    "lost",
    "note",
]


class ManagementActionCreate(BaseModel):
    policy_id: int = Field(..., gt=0)
    action_type: ActionType
    notes: str | None = Field(default=None)


class ManagementActionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    policy_id: int
    action_type: ActionType
    notes: str | None
    created_at: datetime
