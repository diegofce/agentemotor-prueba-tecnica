from datetime import timedelta

from sqlalchemy import select

from app.db.session import Base, SessionLocal, engine
from app.models import Advisor, Client, ManagementAction, Policy
from app.services.window_service import get_business_today

ADVISOR_EMAIL = "maria.seguros@example.com"


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    today = get_business_today()

    with SessionLocal() as db:
        advisor = db.scalar(select(Advisor).where(Advisor.email == ADVISOR_EMAIL))
        if advisor is None:
            advisor = Advisor(
                full_name="María Fernanda Seguros",
                email=ADVISOR_EMAIL,
            )
            db.add(advisor)
            db.commit()
            db.refresh(advisor)

        clients = _create_clients(db, advisor)
        policies_data = [
            (clients[0], "Sura", "auto", "DEMO-AUTO-001", today, "active"),
            (clients[1], "Bolívar", "hogar", "DEMO-HOGAR-002", today + timedelta(days=5), "active"),
            (clients[2], "Mapfre", "vida", "DEMO-VIDA-003", today + timedelta(days=30), "active"),
            (clients[3], "Allianz", "auto", "DEMO-AUTO-004", today - timedelta(days=1), "active"),
            (clients[4], "Sura", "hogar", "DEMO-HOGAR-005", today - timedelta(days=15), "active"),
            (clients[5], "Bolívar", "vida", "DEMO-VIDA-006", today - timedelta(days=30), "active"),
            (clients[6], "Mapfre", "auto", "DEMO-AUTO-007", today - timedelta(days=31), "active"),
            (clients[7], "Allianz", "hogar", "DEMO-HOGAR-008", today - timedelta(days=45), "lost"),
            (clients[8], "Sura", "vida", "DEMO-VIDA-009", today + timedelta(days=365), "renewed"),
            (clients[9], "Bolívar", "auto", "DEMO-AUTO-010", today + timedelta(days=90), "active"),
        ]

        policies = []
        for client, insurer, policy_type, number, expiration_date, status in policies_data:
            policy = db.scalar(select(Policy).where(Policy.policy_number == number))
            if policy is None:
                policy = Policy(
                    client_id=client.id,
                    insurer=insurer,
                    policy_type=policy_type,
                    policy_number=number,
                    expiration_date=expiration_date,
                    status=status,
                )
                db.add(policy)
                db.commit()
                db.refresh(policy)
            policies.append(policy)

        _create_actions(db, policies)
        print("Seed data ready.")


def _create_clients(db, advisor: Advisor) -> list[Client]:
    clients = []
    names = [
        "Carlos Ramírez",
        "Ana Gómez",
        "Luis Martínez",
        "Paula Torres",
        "Jorge Herrera",
        "Diana Rojas",
        "Andrés Castro",
        "Camila Vargas",
        "Felipe Moreno",
        "Laura Sánchez",
    ]

    for index, name in enumerate(names, start=1):
        email = f"cliente{index:02d}@example.com"
        client = db.scalar(select(Client).where(Client.email == email))
        if client is None:
            client = Client(
                advisor_id=advisor.id,
                full_name=name,
                phone=f"30012345{index:02d}",
                email=email,
            )
            db.add(client)
            db.commit()
            db.refresh(client)
        clients.append(client)

    return clients


def _create_actions(db, policies: list[Policy]) -> None:
    actions_data = [
        (policies[0], "note", "Revisión inicial antes del vencimiento."),
        (policies[1], "call_success", "Cliente interesado en renovar."),
        (policies[3], "call_no_answer", "No contestó primera llamada."),
        (policies[4], "renewal_scheduled", "Renovación agendada para esta semana."),
        (policies[5], "call_success", "Cliente pidió nueva cotización."),
        (policies[7], "lost", "Cliente renovó con otro intermediario."),
        (policies[8], "renewed", "Póliza renovada correctamente."),
    ]

    for policy, action_type, notes in actions_data:
        existing_action = db.scalar(
            select(ManagementAction).where(
                ManagementAction.policy_id == policy.id,
                ManagementAction.action_type == action_type,
                ManagementAction.notes == notes,
            ),
        )
        if existing_action is not None:
            continue

        db.add(
            ManagementAction(
                policy_id=policy.id,
                action_type=action_type,
                notes=notes,
            ),
        )

    db.commit()


if __name__ == "__main__":
    seed()
