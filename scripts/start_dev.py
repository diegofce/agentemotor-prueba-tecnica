"""
Arranca backend (uvicorn) y frontend (Vite) en una sola terminal.
Requisitos previos: pip install -r requirements.txt y npm install en src/frontend.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "src" / "backend"
FRONTEND_DIR = ROOT / "src" / "frontend"


def main() -> None:
    if not BACKEND_DIR.is_dir():
        print("No se encontró src/backend. Ejecuta este script desde la raíz del proyecto.")
        sys.exit(1)

    if not FRONTEND_DIR.is_dir():
        print("No se encontró src/frontend.")
        sys.exit(1)

    print("Iniciando API en http://127.0.0.1:8000")
    print("Iniciando frontend en http://localhost:5173")
    print("Ctrl+C para detener ambos procesos.\n")

    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
        cwd=BACKEND_DIR,
    )

    frontend = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=FRONTEND_DIR,
        shell=os.name == "nt",
    )

    try:
        backend.wait()
    except KeyboardInterrupt:
        pass
    finally:
        for proc in (frontend, backend):
            proc.terminate()
        for proc in (frontend, backend):
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()
