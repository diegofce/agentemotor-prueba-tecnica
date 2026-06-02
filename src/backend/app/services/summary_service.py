from sqlalchemy.orm import Session

from app.repositories.policy_repository import get_all_policies
from app.services.window_service import calculate_window_status, get_business_today


def get_summary(db: Session) -> dict[str, int]:
    policies = get_all_policies(db)
    today = get_business_today()
    summary = {
        "por_vencer": 0,
        "en_ventana": 0,
        "fuera_de_ventana": 0,
        "renovadas": 0,
    }

    for policy in policies:
        if policy.status == "renewed":
            summary["renovadas"] += 1
            continue

        window_status = calculate_window_status(policy.expiration_date, today)
        if window_status == "expiring":
            summary["por_vencer"] += 1
        elif window_status == "in_window":
            summary["en_ventana"] += 1
        else:
            summary["fuera_de_ventana"] += 1

    return summary
