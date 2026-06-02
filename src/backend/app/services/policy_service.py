from datetime import date

from sqlalchemy.orm import Session

from app.models.management_action import ManagementAction
from app.models.policy import Policy
from app.repositories.management_action_repository import (
    create_management_action,
    get_actions_by_policy_id,
)
from app.repositories.policy_repository import (
    get_all_policies,
    get_policy_by_id,
    update_policy,
)
from app.schemas.management_action import ManagementActionCreate
from app.schemas.policy import PolicyRenewalRequest, PolicyResponse
from app.services.window_service import (
    calculate_days_remaining_in_window,
    calculate_priority,
    calculate_window_status,
    get_business_today,
)


def validate_renewal(request: PolicyRenewalRequest, today: date | None = None) -> None:
    business_today = today or get_business_today()
    if request.new_expiration_date < business_today:
        raise ValueError("new_expiration_date cannot be before today")


def renew_policy(
    db: Session,
    policy_id: int,
    request: PolicyRenewalRequest,
) -> PolicyResponse:
    policy = get_policy_by_id(db, policy_id)
    if policy is None:
        raise ValueError("policy not found")

    validate_renewal(request)
    updated_policy = update_policy(
        db,
        policy,
        {
            "expiration_date": request.new_expiration_date,
            "status": "renewed",
        },
    )
    create_management_action(
        db,
        ManagementActionCreate(
            policy_id=updated_policy.id,
            action_type="renewed",
            notes=request.notes,
        ),
    )

    return build_policy_response(db, updated_policy)


def build_policy_response(db: Session, policy: Policy) -> PolicyResponse:
    actions = get_actions_by_policy_id(db, policy.id)
    last_action = _get_last_action(actions)
    today = get_business_today()
    days_overdue = max((today - policy.expiration_date).days, 0)

    return PolicyResponse(
        id=policy.id,
        client_id=policy.client_id,
        insurer=policy.insurer,
        policy_type=policy.policy_type,
        policy_number=policy.policy_number,
        expiration_date=policy.expiration_date,
        status=policy.status,
        created_at=policy.created_at,
        updated_at=policy.updated_at,
        client_name=policy.client.full_name if policy.client else None,
        client_phone=policy.client.phone if policy.client else None,
        window_status=calculate_window_status(policy.expiration_date, today),
        days_overdue=days_overdue,
        days_remaining_in_window=calculate_days_remaining_in_window(
            policy.expiration_date,
            today,
        ),
        last_action=last_action.action_type if last_action else None,
        last_action_at=last_action.created_at if last_action else None,
        total_actions=len(actions),
    )


def get_enriched_policies(db: Session) -> list[PolicyResponse]:
    policies = get_all_policies(db)
    sorted_policies = sort_policies_by_priority(policies)
    return [build_policy_response(db, policy) for policy in sorted_policies]


def sort_policies_by_priority(policies: list[Policy]) -> list[Policy]:
    today = get_business_today()

    return sorted(
        policies,
        key=lambda policy: (
            4 if policy.status == "renewed" else calculate_priority(
                policy.expiration_date,
                today,
            ),
            policy.expiration_date,
            policy.id,
        ),
    )


def _get_last_action(actions: list[ManagementAction]) -> ManagementAction | None:
    if not actions:
        return None
    return max(actions, key=lambda action: action.created_at)
