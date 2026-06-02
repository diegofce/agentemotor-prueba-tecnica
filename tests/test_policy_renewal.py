import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "src" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.session import Base
from app.models import Advisor, Client, ManagementAction, Policy
from app.schemas.policy import PolicyRenewalRequest
from app.services.policy_service import renew_policy

FIXED_TODAY = date(2026, 6, 2)


@pytest.fixture()
def db_session() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    testing_session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=engine)

    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def _create_policy(
    db: Session,
    expiration_date: date,
    policy_number: str = "POL-001",
) -> Policy:
    advisor = Advisor(full_name="María Seguros", email="maria@example.com")
    db.add(advisor)
    db.flush()

    client = Client(
        advisor_id=advisor.id,
        full_name="Carlos Ramírez",
        phone="3001234567",
        email="carlos@example.com",
    )
    db.add(client)
    db.flush()

    policy = Policy(
        client_id=client.id,
        insurer="Sura",
        policy_type="auto",
        policy_number=policy_number,
        expiration_date=expiration_date,
        status="active",
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def test_renovacion_valida(db_session: Session) -> None:
    policy = _create_policy(db_session, FIXED_TODAY - timedelta(days=5))
    request = PolicyRenewalRequest(
        new_expiration_date=FIXED_TODAY + timedelta(days=365),
        notes="Cliente confirmó renovación",
    )

    response = renew_policy(db_session, policy.id, request)

    assert response.status == "renewed"
    assert response.expiration_date == FIXED_TODAY + timedelta(days=365)
    assert response.last_action == "renewed"
    assert response.total_actions == 1

    refreshed_policy = db_session.get(Policy, policy.id)
    assert refreshed_policy is not None
    assert refreshed_policy.status == "renewed"
    assert refreshed_policy.expiration_date == FIXED_TODAY + timedelta(days=365)


def test_renovacion_invalida(db_session: Session) -> None:
    policy = _create_policy(
        db_session,
        FIXED_TODAY - timedelta(days=5),
        policy_number="POL-002",
    )
    original_expiration = policy.expiration_date

    invalid_request = PolicyRenewalRequest.model_construct(
        new_expiration_date=FIXED_TODAY - timedelta(days=1),
        notes="Intento con fecha pasada",
    )

    with pytest.raises(ValueError, match="new_expiration_date cannot be before today"):
        renew_policy(db_session, policy.id, invalid_request)

    refreshed_policy = db_session.get(Policy, policy.id)
    assert refreshed_policy is not None
    assert refreshed_policy.status == "active"
    assert refreshed_policy.expiration_date == original_expiration

    actions = list(
        db_session.scalars(
            select(ManagementAction).where(
                ManagementAction.policy_id == policy.id,
            ),
        ),
    )
    assert actions == []


def test_renovacion_crea_gestion_automatica(db_session: Session) -> None:
    policy = _create_policy(
        db_session,
        FIXED_TODAY - timedelta(days=5),
        policy_number="POL-003",
    )
    request = PolicyRenewalRequest(
        new_expiration_date=FIXED_TODAY + timedelta(days=365),
        notes="Renovación confirmada por el cliente",
    )

    renew_policy(db_session, policy.id, request)

    actions = list(
        db_session.scalars(
            select(ManagementAction).where(
                ManagementAction.policy_id == policy.id,
            ),
        ),
    )

    assert len(actions) == 1
    assert actions[0].action_type == "renewed"
    assert actions[0].notes == "Renovación confirmada por el cliente"
    assert actions[0].policy_id == policy.id
