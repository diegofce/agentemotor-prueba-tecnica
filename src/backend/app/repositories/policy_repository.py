from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.policy import Policy
from app.schemas.policy import PolicyCreate


def get_all_policies(db: Session) -> list[Policy]:
    statement = select(Policy)
    return list(db.scalars(statement).all())


def get_policy_by_id(db: Session, policy_id: int) -> Policy | None:
    return db.get(Policy, policy_id)


def create_policy(db: Session, policy_create: PolicyCreate) -> Policy:
    policy = Policy(**policy_create.model_dump())
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def update_policy(
    db: Session,
    policy: Policy,
    values: dict[str, Any],
) -> Policy:
    for field, value in values.items():
        if hasattr(policy, field):
            setattr(policy, field, value)

    db.commit()
    db.refresh(policy)
    return policy
