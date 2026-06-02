from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.management_action import ManagementAction
from app.schemas.management_action import ManagementActionCreate


def get_actions_by_policy_id(
    db: Session,
    policy_id: int,
) -> list[ManagementAction]:
    statement = select(ManagementAction).where(
        ManagementAction.policy_id == policy_id,
    )
    return list(db.scalars(statement).all())


def create_management_action(
    db: Session,
    action_create: ManagementActionCreate,
) -> ManagementAction:
    action = ManagementAction(**action_create.model_dump())
    db.add(action)
    db.commit()
    db.refresh(action)
    return action
