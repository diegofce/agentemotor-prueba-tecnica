from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.summary_service import get_summary

router = APIRouter(prefix="/summary", tags=["summary"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("")
def read_summary(db: DbSession) -> dict[str, int]:
    return get_summary(db)
