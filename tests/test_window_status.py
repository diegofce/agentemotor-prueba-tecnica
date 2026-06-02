import sys
from datetime import date, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "src" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services.window_service import calculate_window_status

FIXED_TODAY = date(2026, 6, 2)


def test_window_status_por_vencer() -> None:
    expiration_date = FIXED_TODAY + timedelta(days=10)

    assert calculate_window_status(expiration_date, FIXED_TODAY) == "expiring"


def test_window_status_en_ventana() -> None:
    expiration_date = FIXED_TODAY - timedelta(days=10)

    assert calculate_window_status(expiration_date, FIXED_TODAY) == "in_window"


def test_window_status_fuera_de_ventana() -> None:
    expiration_date = FIXED_TODAY - timedelta(days=31)

    assert calculate_window_status(expiration_date, FIXED_TODAY) == "out_of_window"
