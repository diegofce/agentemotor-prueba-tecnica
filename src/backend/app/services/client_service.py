from sqlalchemy.orm import Session

from app.models.client import Client
from app.repositories.client_repository import (
    create_client,
    get_all_clients,
    get_client_by_id,
)
from app.schemas.client import ClientCreate


def list_clients(db: Session) -> list[Client]:
    return get_all_clients(db)


def get_client_detail(db: Session, client_id: int) -> Client:
    client = get_client_by_id(db, client_id)
    if client is None:
        raise ValueError("client not found")
    return client


def create_new_client(db: Session, client_create: ClientCreate) -> Client:
    return create_client(db, client_create)
