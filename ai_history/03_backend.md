### BLOQUE 2: Implementación de modelos

- Herramienta utilizada: OpenAI Codex CLI - (v0.136.0)
- Modelo: gpt-5.5 medium - Fecha: Junio 2026
- Etapa: Implementación de modelos

## Prompt:
Actúa como arquitecto backend senior.

Tengo este spec:
[SPEC]

Voy a implementar FastAPI + SQLAlchemy + SQLite.

Necesito una estructura de carpetas para una arquitectura por capas.

No generes código todavía.

Explica:

- carpetas
- responsabilidad
- dependencias entre capas

Mantén el diseño simple para una prueba técnica de 4 horas.


### Respuesta:

Primero hay que crear requirements.txt:e instalar las dependencias

  Dependencias incluidas:

  fastapi
  uvicorn[standard]
  sqlalchemy
  pydantic
  pydantic-settings
  pytest
  httpx

  Usa requirements.txt y no requerimientos.txt porque es el nombre estándar
  que consume pip install -r requirements.txt. No generé más código de
  aplicación.

  Estructura Recomendada

  Para un desarrollo de 4 horas, mantendría esta arquitectura por capas:

  src/backend/
    app/
      main.py
      database.py
      models/
        advisor.py
        client.py
        policy.py
        management_action.py
      schemas/
        client.py
        policy.py
        management_action.py
        summary.py
      repositories/
        client_repository.py
        policy_repository.py
        management_action_repository.py
      services/
        policy_service.py
        summary_service.py
      api/
        clients.py
        policies.py
        summary.py

  Responsabilidades

  main.py: crea la app FastAPI, registra routers y configuración global.

  database.py: define engine SQLite, sesión SQLAlchemy y Base.

  models/: contiene modelos SQLAlchemy, solo estructura persistente de BD.
  Aquí no debería vivir lógica de negocio como window_status.

  schemas/: contiene modelos Pydantic para requests/responses. Valida
  entradas y define respuestas limpias para la API.

  repositories/: acceso a datos. Consultas, inserts y updates. No decide
  reglas de negocio.

  services/: reglas del negocio. Aquí van el cálculo de ventana, orden de
  prioridad, renovación, validación de fecha y creación automática de
  gestión.

  api/: routers FastAPI. Recibe HTTP, llama servicios y devuelve schemas. No
  debería consultar directamente la base de datos.

  Dependencias Entre Capas

  Flujo recomendado:

  api -> services -> repositories -> models/database

  Los schemas se usan principalmente entre api y services.

  Regla práctica:

  - api depende de services y schemas.
  - services depende de repositories y reglas de dominio.
  - repositories depende de models y database.
  - models no depende de api, services ni schemas.

  Decisión Central

  window_status debe calcularse en services/policy_service.py, no en models
  ni en la base de datos. Eso sigue el spec y evita estados desactualizados.

  También dejaría /summary como servicio separado porque sus contadores
  dependen de la misma lógica de ventana que las pólizas, pero con una
  respuesta agregada.

  Nota: el repo tiene un cambio previo en ai_history/03_backend.md que no
  modifiqué.

## Prompt 2:

Actúa como desarrollador backend senior.

En base el diseño de carpetas y responsabilidades que definiste, implementa modelos
models/advisor.py
app/models/client.py
app/models/management_action.py
Demas necesarios para una prueba técnica de 4 horas, simple, en base al spec, y 02_implementacion.md.
usando SQLAlchemy 2.0 con tipado completo y relaciones correctas.

Usa:

- SQLAlchemy 2.0
- tipado completo
- relaciones correctas
- comentarios mínimos
- De acuerdo a requerimientos

Explica decisiones importantes.


#### Respuesta:

Implementé la capa de modelos SQLAlchemy 2.0 para el backend:

  - src/backend/app/database.py:1
  - src/backend/app/models/advisor.py:1
  - src/backend/app/models/client.py:1
  - src/backend/app/models/policy.py:1
  - src/backend/app/models/management_action.py:1
  - src/backend/app/models/__init__.py:1

  También agregué src/backend/app/__init__.py:1 para que app funcione como paquete Python.

  Decisiones importantes:

  - Usé SQLAlchemy 2.0 con Mapped y mapped_column para tipado completo.
  - Respeté el spec: advisors, clients, policies, management_actions con campos y nombres en inglés.
  - Dejé window_status fuera de la base de datos porque debe calcularse en servicios.
  - Usé relaciones correctas:
      - Advisor -> Client
      - Client -> Policy
      - Policy -> ManagementAction

  - Agregué ondelete="RESTRICT" para evitar borrados accidentales de datos con historial.
  - Agregué índices en FKs, expiration_date, status, action_type y created_at, porque serán usados para filtros, detalle, resumen y orden
    operativo.

  - database.py queda simple con SQLite, Base, engine, SessionLocal y get_db.

  Verifiqué que los modelos importan correctamente y registran las tablas:

  ['advisors', 'clients', 'management_actions', 'policies']


### Prompt 3:
Conexcion db
Actúa como desarrollador backend senior.

Genera:

app/db/session.py

Requisitos:

- SQLite
- SQLAlchemy 2.0
- SessionLocal
- engine
- configuración para FastAPI

Explica decisiones.

### Respuesta:
• Generé y verifiqué src/backend/app/db/session.py:1.

  También dejé src/backend/app/database.py:1 como re-export de
  compatibilidad, para que no existan dos Base ni dos conexiones distintas.

  Decisiones:

  - DATABASE_URL = "sqlite:///./insurance_portfolio.db": SQLite local,
    simple para MVP/prueba técnica.

  - connect_args={"check_same_thread": False}: necesario para usar SQLite
    correctamente con FastAPI, porque las requests pueden manejarse en
    distintos threads.

  - SessionLocal = sessionmaker(...): fábrica de sesiones por request.
  - Base(DeclarativeBase): base única para todos los modelos SQLAlchemy 2.0.
  - get_db(): dependencia estándar de FastAPI para abrir y cerrar sesión de
    base de datos por request.

  Verificación ejecutada correctamente:

  ['advisors', 'clients', 'management_actions', 'policies']
  sqlite


### Prompt 4:

Schemas Pydantic

Genera:

app/schemas/advisor.py
app/schemas/client.py
app/schemas/policy.py
app/schemas/management_action.py

Necesito:

- Create
- Response
- Y en Policy RenewalRequest

Usa Pydantic v2.

Seguir exactamente el spec.
Incluye validaciones relevantes.

### Respuesta:

Generé los schemas Pydantic v2:

  - src/backend/app/schemas/advisor.py:1
  - src/backend/app/schemas/client.py:1
  - src/backend/app/schemas/policy.py:1
  - src/backend/app/schemas/management_action.py:1
  - src/backend/app/schemas/__init__.py:1

  Incluí:

  - AdvisorCreate, AdvisorResponse
  - ClientCreate, ClientResponse
  - PolicyCreate, PolicyResponse, PolicyRenewalRequest
  - ManagementActionCreate, ManagementActionResponse

  Decisiones importantes:

  - Usé ConfigDict(from_attributes=True) para que los Response puedan
    construirse desde modelos SQLAlchemy.

  - Usé Literal para valores cerrados del spec:
      - policy_type: auto, hogar, vida
      - status: active, renewed, lost
      - action_type: call_no_answer, call_success, renewal_scheduled,
        renewed, lost, note

  - PolicyResponse incluye campos persistidos y campos enriquecidos
    opcionales del spec como window_status, days_overdue, last_action, etc.

  - PolicyRenewalRequest valida que new_expiration_date no sea anterior a
    hoy.

  - Para zona horaria de Colombia usé America/Bogota con fallback UTC-5,
    porque en Windows puede faltar tzdata.

  Verificación ejecutada:

  schemas ok

### Prompt 5:

Actúa como backend senior.

Tengo estos modelos:
[MODELOS]

Genera:

app/repositories/policy_repository.py

Responsabilidades:

- get_all
- get_by_id
- create
- update

No incluir reglas de negocio.

Solo acceso a datos.

Y

Genera:

app/repositories/management_action_repository.py

Solo persistencia.

Nada de lógica de negocio.

### Respuesta:


• Generé la capa de repositorios:

  - src/backend/app/repositories/policy_repository.py:1
  - src/backend/app/repositories/management_action_repository.py:1
  - src/backend/app/repositories/__init__.py:1

  Incluye:

  policy_repository.py:

  - get_all_policies
  - get_policy_by_id
  - create_policy
  - update_policy

  management_action_repository.py:

  - get_actions_by_policy_id
  - create_management_action

  Decisiones:

  - Los repositorios reciben Session, no crean sesiones. Eso mantiene la
    integración limpia con FastAPI vía get_db.

  - No hay reglas de negocio: no cálculo de window_status, no renovación, no
    priorización, no validación de fechas.

  - create hace add, commit, refresh y devuelve el modelo persistido.
  - update_policy recibe un modelo existente y un dict, actualiza solo
    atributos válidos y persiste.

  - Uso select(...) de SQLAlchemy 2.0 para consultas limpias y tipadas.

  Verificación ejecutada:

  repositories ok

### Prompt 6:

Actúa como arquitecto de software y de dominio.

Tengo esta regla:

- por vencer: 0-30 días
- en ventana: 1-30 días vencida
- fuera de ventana: más de 30 días

Genera:

app/services/window_service.py

Responsabilidades:

- calcular window_status
- calcular prioridad
- calcular días restantes

Toda la lógica de negocio debe vivir aquí.

### Respuesta:
• Generé src/backend/app/services/window_service.py:1 y src/backend/app/
  services/__init__.py:1.

  Incluye:

  - calculate_window_status(expiration_date, today=None)
  - calculate_priority(expiration_date, today=None)
  - calculate_days_remaining_in_window(expiration_date, today=None)
  - get_business_today()

  Decisiones:

  - El servicio no depende de FastAPI, SQLAlchemy ni modelos. Es lógica pura
    de dominio.

  - Usa fecha de negocio Colombia (America/Bogota) con fallback UTC-5 para
    Windows.

  - Prioridad:
      - 1: in_window
      - 2: expiring
      - 3: out_of_window

  - window_status sigue exactamente la regla:
      - expiring: entre hoy y 30 días hacia adelante
      - in_window: vencida entre 1 y 30 días
      - out_of_window: más de 30 días vencida, o fuera del rango operativo

  - days_remaining_in_window devuelve:
      - 30 para pólizas no vencidas
      - 30 - días vencida para pólizas en ventana
      - None si ya está fuera de ventana

  Verificación de frontera ejecutada:

  hoy -> expiring
  +30 días -> expiring
  -1 día -> in_window
  -30 días -> in_window
  -31 días -> out_of_window

### Prompt 7:

Genera:

app/services/policy_service.py

Responsabilidades:

- renovar póliza
- validar renovación
- construir respuesta enriquecida
- ordenar por prioridad

app/services/summary_service.py
Responsabilidades:

- calcular contadores

Retornar:

- por vencer
- en ventana
- fuera de ventana
- renovadas
No acceder directamente a la base de datos.

Usar repositorios.


### Respuesta:

 Generé los servicios:

  - src/backend/app/services/policy_service.py:1
  - src/backend/app/services/summary_service.py:1
  - Actualicé src/backend/app/services/__init__.py:1

  policy_service.py incluye:

  - renew_policy
  - validate_renewal
  - build_policy_response
  - get_enriched_policies
  - sort_policies_by_priority

  summary_service.py incluye:

  - get_summary

  Decisiones importantes:

  - Los servicios no acceden directamente a la base de datos con queries.
    Usan repositorios.

  - La lógica de ventana sigue delegada a window_service.
  - renew_policy valida la fecha, actualiza la póliza a renewed, cambia
    expiration_date y crea automáticamente una gestión renewed.

  - build_policy_response construye la respuesta enriquecida del spec:
    cliente, teléfono, ventana, días vencidos, días restantes, última acción
    y total de acciones.

  - El resumen retorna:
      - por_vencer
      - en_ventana
      - fuera_de_ventana
      - renovadas

  - Las renovadas se cuentan por status == "renewed" y no entran en los
    contadores operativos de ventana.

  Verificación ejecutada:

  services ok


### Prompt 8:

Rutas: Policies
Genera:

app/api/routes/policies.py

Endpoints:

GET /policies

GET /policies/{id}

POST /policies

POST /policies/{id}/actions

POST /policies/{id}/renew

Usar dependency injection.

Mantener routers delgados.

Toda lógica debe vivir en services.

Clients:
Genera:

app/api/routes/clients.py

GET /clients

GET /clients/{id}

POST /clients

Summary:

Genera:

app/api/routes/summary.py

GET /summary

### Respuesta:

• Generé los routers solicitados:

  - src/backend/app/api/routes/policies.py:1
  - src/backend/app/api/routes/clients.py:1
  - src/backend/app/api/routes/summary.py:1

  También agregué lo necesario para mantener routers delgados:

  - src/backend/app/repositories/client_repository.py:1
  - src/backend/app/services/client_service.py:1
  - Extendí src/backend/app/services/policy_service.py:1
  - Agregué app/api/__init__.py y app/api/routes/__init__.py

  Endpoints implementados:

  GET  /policies
  GET  /policies/{id}
  POST /policies
  POST /policies/{id}/actions
  POST /policies/{id}/renew

  GET  /clients
  GET  /clients/{id}
  POST /clients

  GET  /summary

  Decisiones:

  - Las rutas usan Depends(get_db) para inyección de sesión.
  - Los routers no consultan repositorios directamente; llaman servicios.
  - Los repositorios siguen siendo solo persistencia.
  - Los errores de dominio (ValueError) se traducen en HTTPException dentro
    del router.

  - Para POST /policies/{id}/actions, el servicio valida que el policy_id
    del body coincida con el id de la ruta.

  - summary llama summary_service, que a su vez usa repositorios y
    window_service.

  Verificación ejecutada:

  ['/policies', '/clients', '/summary']

### Prompt 8:

Genera:

app/main.py

Requisitos:

- FastAPI
- incluir routers
- startup database
- documentación OpenAPI

Código limpio.

### Respuesta:


### Prompt 9:

Genera:

seed.py

Crear:

- 1 advisor
- 10 clientes
- pólizas en distintos estados
- historial de acciones

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
  -31 días vencida -> out_of_window
  -45 días vencida -> out_of_window
  renewed          -> status renewed
  lost             -> status lost

  Verificación ejecutada:

  {'advisors': 1, 'clients': 10, 'policies': 10, 'actions': 7}

  Para correrlo manualmente:

  cd src/backend
  ..\..\.venv\Scripts\python.exe seed.py
