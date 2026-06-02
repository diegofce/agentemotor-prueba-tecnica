from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.client import ClientCreate


def get_all_clients(db: Session) -> list[Client]:
    statement = select(Client)
    return list(db.scalars(statement).all())


def get_client_by_id(db: Session, client_id: int) -> Client | None:
    return db.get(Client, client_id)


def create_client(db: Session, client_create: ClientCreate) -> Client:
    client = Client(**client_create.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
