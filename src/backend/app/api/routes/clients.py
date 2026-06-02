from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.client import ClientCreate, ClientResponse
from app.services.client_service import (
    create_new_client,
    get_client_detail,
    list_clients,
)

router = APIRouter(prefix="/clients", tags=["clients"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[ClientResponse])
def get_clients(db: DbSession) -> list[ClientResponse]:
    return list_clients(db)


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: DbSession) -> ClientResponse:
    try:
        return get_client_detail(db, client_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client_create: ClientCreate, db: DbSession) -> ClientResponse:
    return create_new_client(db, client_create)
