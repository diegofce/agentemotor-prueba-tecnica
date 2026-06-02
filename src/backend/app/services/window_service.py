from datetime import date, datetime, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

WindowStatus = Literal["expiring", "in_window", "out_of_window"]

WINDOW_DAYS = 30


def get_business_today() -> date:
    try:
        colombia_tz = ZoneInfo("America/Bogota")
    except ZoneInfoNotFoundError:
        colombia_tz = timezone(timedelta(hours=-5))
    return datetime.now(colombia_tz).date()


def calculate_window_status(
    expiration_date: date,
    today: date | None = None,
) -> WindowStatus:
    business_today = today or get_business_today()
    days_until_expiration = (expiration_date - business_today).days

    if 0 <= days_until_expiration <= WINDOW_DAYS:
        return "expiring"

    days_overdue = (business_today - expiration_date).days
    if 1 <= days_overdue <= WINDOW_DAYS:
        return "in_window"

    return "out_of_window"


def calculate_priority(
    expiration_date: date,
    today: date | None = None,
) -> int:
    window_status = calculate_window_status(expiration_date, today)
    priorities: dict[WindowStatus, int] = {
        "in_window": 1,
        "expiring": 2,
        "out_of_window": 3,
    }
    return priorities[window_status]


def calculate_days_remaining_in_window(
    expiration_date: date,
    today: date | None = None,
) -> int | None:
    business_today = today or get_business_today()
    days_overdue = (business_today - expiration_date).days

    if 1 <= days_overdue <= WINDOW_DAYS:
        return WINDOW_DAYS - days_overdue

    if expiration_date >= business_today:
        return WINDOW_DAYS

    return None
