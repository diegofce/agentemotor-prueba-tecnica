### BLOQUE 2: Implementación de modelos


## 1. Estructura base

**Prompt**

Actúa como arquitecto backend senior. Quiero una estructura por capas para FastAPI + SQLAlchemy + SQLite, sin generar código todavía.

**Resumen de la respuesta**


```text
src/backend/
  app/
    main.py
    database.py
    models/
    schemas/
    repositories/
    services/
    api/
```

  - `main.py`: composición de la app y routers.
  - `database.py`: engine, sesión y `Base`.
  - `models/`: persistencia.
  - `schemas/`: entrada y salida.
  - `repositories/`: acceso a datos.
  - `services/`: reglas de negocio.
  - `api/`: routers delgados.

## 2. Modelos SQLAlchemy

**Prompt**

Implementar modelos SQLAlchemy 2.0 con tipado completo y relaciones correctas.

**Resumen de la respuesta**

  - `Advisor -> Client`
  - `Client -> Policy`

  Verificación ejecutada:

  ['/policies', '/clients', '/summary']

### Prompt 8:

Genera:

app/main.py

Requisitos:


Código limpio.

### Respuesta:

• Generé src/backend/app/main.py:1.

  Incluye:

  - FastAPI
  - routers de clients, policies y summary
  - endpoint /health
  - startup de base de datos con Base.metadata.create_all(bind=engine)
  - documentación OpenAPI automática en:
      - /docs
      - /redoc
      - /openapi.json

  Decisiones:

  - Usé lifespan en lugar de @app.on_event("startup") porque es el enfoque
    moderno de FastAPI.

  - Importé los modelos en main.py para asegurar que SQLAlchemy registre las
    tablas antes de create_all.

  - Para esta prueba técnica usé create_all; en producción real lo
    reemplazaría por migraciones con Alembic.

  - Mantengo los routers separados y main.py solo como composición de la
    app.

  /openapi.json
  /redoc

### Prompt 9:

Genera:

seed.py

Crear:


Los datos deben servir para demostrar la ventana de 30 días.


### Respuesta:


• Generé y ejecuté src/backend/seed.py:1.

  Crea datos demo idempotentes:

  - 1 advisor
  - 10 clientes
  - 10 pólizas
  - 7 acciones de historial

  Cubre la ventana de 30 días:

  hoy              -> expiring
  +5 días          -> expiring
  +30 días         -> expiring
  -1 día vencida   -> in_window
  -15 días vencida -> in_window
  -30 días vencida -> in_window
  Verificación ejecutada:

  {'advisors': 1, 'clients': 10, 'policies': 10, 'actions': 7}

  Para correrlo manualmente:

  cd src/backend
  ..\..\.venv\Scripts\python.exe seed.py
