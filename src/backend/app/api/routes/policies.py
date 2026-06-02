from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.management_action import (
    ManagementActionCreate,
    ManagementActionResponse,
)
from app.schemas.policy import PolicyCreate, PolicyRenewalRequest, PolicyResponse
from app.services.policy_service import (
    add_policy_action,
    create_new_policy,
    get_policy_detail,
    list_policies,
    renew_policy,
)

router = APIRouter(prefix="/policies", tags=["policies"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[PolicyResponse])
def get_policies(db: DbSession) -> list[PolicyResponse]:
    return list_policies(db)


@router.get("/{policy_id}", response_model=PolicyResponse)
def get_policy(policy_id: int, db: DbSession) -> PolicyResponse:
    try:
        return get_policy_detail(db, policy_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
def create_policy(policy_create: PolicyCreate, db: DbSession) -> PolicyResponse:
    return create_new_policy(db, policy_create)


@router.post(
    "/{policy_id}/actions",
    response_model=ManagementActionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_policy_action(
    policy_id: int,
    action_create: ManagementActionCreate,
    db: DbSession,
) -> ManagementActionResponse:
    try:
        return add_policy_action(db, policy_id, action_create)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/{policy_id}/renew", response_model=PolicyResponse)
def renew_existing_policy(
    policy_id: int,
    renewal_request: PolicyRenewalRequest,
    db: DbSession,
) -> PolicyResponse:
    try:
        return renew_policy(db, policy_id, renewal_request)
    except ValueError as exc:
        detail = str(exc)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if detail == "policy not found"
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=detail)
