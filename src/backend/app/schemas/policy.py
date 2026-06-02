from datetime import date, datetime, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator

PolicyType = Literal["auto", "hogar", "vida"]
PolicyStatus = Literal["active", "renewed", "lost"]
WindowStatus = Literal["expiring", "in_window", "out_of_window"]


def colombia_today() -> date:
    try:
        colombia_tz = ZoneInfo("America/Bogota")
    except ZoneInfoNotFoundError:
        colombia_tz = timezone(timedelta(hours=-5))
    return datetime.now(colombia_tz).date()


class PolicyCreate(BaseModel):
    client_id: int = Field(..., gt=0)
    insurer: str = Field(..., min_length=1, max_length=100)
    policy_type: PolicyType
    policy_number: str | None = Field(default=None, max_length=100)
    expiration_date: date
    status: PolicyStatus = "active"


class PolicyRenewalRequest(BaseModel):
    new_expiration_date: date
    notes: str | None = None

    @field_validator("new_expiration_date")
    @classmethod
    def validate_new_expiration_date(cls, value: date) -> date:
        if value < colombia_today():
            raise ValueError("new_expiration_date cannot be before today")
        return value


class PolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    insurer: str
    policy_type: PolicyType
    policy_number: str | None
    expiration_date: date
    status: PolicyStatus
    created_at: datetime
    updated_at: datetime
    client_name: str | None = None
    client_phone: str | None = None
    window_status: WindowStatus | None = None
    days_overdue: int | None = None
    days_remaining_in_window: int | None = None
    last_action: str | None = None
    last_action_at: datetime | None = None
    total_actions: int | None = None
