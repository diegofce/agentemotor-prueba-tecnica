import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "src" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.session import Base
from app.models import Advisor, Client, Policy
from app.services.policy_service import sort_policies_by_priority

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
    policy_number: str,
    expiration_date: date,
    status: str = "active",
) -> Policy:
    advisor = db.query(Advisor).filter_by(email="maria@example.com").first()
    if advisor is None:
        advisor = Advisor(full_name="María Seguros", email="maria@example.com")
        db.add(advisor)
        db.flush()

    client = Client(
        advisor_id=advisor.id,
        full_name=f"Cliente {policy_number}",
        phone="3001234567",
        email=f"{policy_number}@example.com",
    )
    db.add(client)
    db.flush()

    policy = Policy(
        client_id=client.id,
        insurer="Sura",
        policy_type="auto",
        policy_number=policy_number,
        expiration_date=expiration_date,
        status=status,
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def _policy_numbers(policies: list[Policy]) -> list[str]:
    return [p.policy_number for p in policies]


def test_in_window_antes_de_expiring(db_session: Session) -> None:
    expiring = _create_policy(db_session, "P-EXP", FIXED_TODAY + timedelta(days=10))
    in_window = _create_policy(db_session, "P-WIN", FIXED_TODAY - timedelta(days=10))

    ordered = sort_policies_by_priority([expiring, in_window])

    assert _policy_numbers(ordered) == ["P-WIN", "P-EXP"]


def test_expiring_antes_de_fuera_de_ventana(db_session: Session) -> None:
    out_of_window = _create_policy(
        db_session,
        "P-OUT",
        FIXED_TODAY - timedelta(days=45),
    )
    expiring = _create_policy(
        db_session,
        "P-EXP",
        FIXED_TODAY + timedelta(days=5),
    )

    ordered = sort_policies_by_priority([expiring, out_of_window])

    assert _policy_numbers(ordered) == ["P-EXP", "P-OUT"]


def test_fuera_de_ventana_antes_de_renovadas(db_session: Session) -> None:
    renewed = _create_policy(
        db_session,
        "P-REN",
        FIXED_TODAY + timedelta(days=365),
        status="renewed",
    )
    out_of_window = _create_policy(
        db_session,
        "P-OUT",
        FIXED_TODAY - timedelta(days=60),
    )

    ordered = sort_policies_by_priority([renewed, out_of_window])

    assert _policy_numbers(ordered) == ["P-OUT", "P-REN"]


def test_orden_dentro_de_in_window_por_antiguedad(db_session: Session) -> None:
    more_overdue = _create_policy(
        db_session,
        "P-WIN-OLD",
        FIXED_TODAY - timedelta(days=25),
    )
    less_overdue = _create_policy(
        db_session,
        "P-WIN-NEW",
        FIXED_TODAY - timedelta(days=3),
    )

    ordered = sort_policies_by_priority([less_overdue, more_overdue])

    assert _policy_numbers(ordered) == ["P-WIN-OLD", "P-WIN-NEW"]


def test_orden_dentro_de_expiring_por_proximidad(db_session: Session) -> None:
    soonest = _create_policy(
        db_session,
        "P-EXP-SOON",
        FIXED_TODAY + timedelta(days=1),
    )
    later = _create_policy(
        db_session,
        "P-EXP-LATER",
        FIXED_TODAY + timedelta(days=29),
    )

    ordered = sort_policies_by_priority([later, soonest])

    assert _policy_numbers(ordered) == ["P-EXP-SOON", "P-EXP-LATER"]


def test_orden_completo_de_cartera(db_session: Session) -> None:
    renewed = _create_policy(
        db_session,
        "P-REN",
        FIXED_TODAY + timedelta(days=365),
        status="renewed",
    )
    out_of_window = _create_policy(
        db_session,
        "P-OUT",
        FIXED_TODAY - timedelta(days=45),
    )
    expiring_later = _create_policy(
        db_session,
        "P-EXP-LATER",
        FIXED_TODAY + timedelta(days=20),
    )
    expiring_soon = _create_policy(
        db_session,
        "P-EXP-SOON",
        FIXED_TODAY + timedelta(days=5),
    )
    in_window_new = _create_policy(
        db_session,
        "P-WIN-NEW",
        FIXED_TODAY - timedelta(days=2),
    )
    in_window_old = _create_policy(
        db_session,
        "P-WIN-OLD",
        FIXED_TODAY - timedelta(days=28),
    )

    unordered = [
        expiring_later,
        renewed,
        in_window_new,
        out_of_window,
        expiring_soon,
        in_window_old,
    ]

    ordered = sort_policies_by_priority(unordered)

    assert _policy_numbers(ordered) == [
        "P-WIN-OLD",
        "P-WIN-NEW",
        "P-EXP-SOON",
        "P-EXP-LATER",
        "P-OUT",
        "P-REN",
    ]
