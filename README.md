# Agentemotor — Cartera de pólizas

Prueba técnica Full-Stack. Herramienta para que una asesora (María) deje el Excel y gestione renovaciones con prioridad por la ventana regulatoria de 30 días en Colombia.

Autor: Diego Fernando Chacón
3187601685
dyewoc@gmail.com
---

## 1. Cómo correrlo (máximo 3 comandos)

**Requisitos:** Python 3.11+, Node.js 18+ y npm.

Desde la **raíz del proyecto**:

```bash
pip install -r requirements.txt
```

```bash
cd src/frontend && npm install && cd ../..
```

```bash
python scripts/start_dev.py
```

Abre **http://localhost:5173**. El frontend habla con la API por proxy de Vite (`/summary`, `/policies`, `/openapi.json` → puerto 8000).

Al arrancar, el backend crea SQLite y carga datos de demostración (`seed` automático).

### Alternativa manual (dos terminales)

Si prefieres ver logs separados:

```bash
# Terminal 1
cd src/backend
uvicorn app.main:app --reload
```

```bash
# Terminal 2
cd src/frontend
npm run dev
```

### Tests

```bash
pip install -r requirements.txt
pytest
```

---

## 2. Decisiones de diseño (y por qué)

**FastAPI + SQLite en el backend.** Validación con Pydantic, OpenAPI gratis y SQLite para correr local sin instalar nada más. La lógica sensible (ventana de 30 días, orden de prioridad, renovación) vive en servicios, no en las rutas.

**React + Vite + TypeScript en el frontend.** Una sola pantalla: resumen arriba, tabla abajo, modales para gestionar y renovar. Sin librerías de estado externas (`useState` / `useReducer` solamente) y CSS puro, como pedía el alcance.

**`window_status` calculado, no guardado en BD.** Así María siempre ve la urgencia real del día sin jobs nocturnos. Es la misma regla antes y después del vencimiento (30 días).

**Seed al iniciar la API.** Quien clone el repo y levante el backend ve datos de ejemplo sin pasos extra.

**Proxy de Vite en desarrollo.** El navegador pide todo a `:5173` y Vite reenvía al API; evita pelear con CORS en local. También dejé CORS en FastAPI por si alguien usa `VITE_API_BASE_URL` apuntando directo a `:8000`.

### Cómo pensé el “dashboard” (pantalla principal)

No hay gráficos ni varias rutas: es un **panel operativo** para el día a día de María.

| Zona | Qué muestra | Para qué sirve |
|------|-------------|----------------|
| **Encabezado — 4 tarjetas** | Contadores: por vencer, en ventana, fuera de ventana, renovadas | Vista rápida del tamaño de cada “cola” de trabajo (como filtrar el Excel por estado) |
| **Tabla de pólizas** | Cliente, tipo, vencimiento, badge de ventana, estado, última gestión | Lista priorizada (en ventana primero, luego por vencer, etc.) |
| **Acciones por fila** | Registrar gestión / Renovar | Reemplaza marcar la X en Excel y actualizar la fecha a mano |

**Supuestos que asumí en la UI:** una sola asesora, sin login, español en etiquetas, y que “última gestión” en la tabla es suficiente para decidir si llamar de nuevo (historial completo quedó para mejora continua).

---

## 3. Qué dejé fuera (a propósito)

Lo que **no** está en esta entrega porque prioricé el flujo que más duele en el enunciado (perder clientes por seguimiento tardío):

- Autenticación y multiusuario.
- Cotización / emisión con aseguradoras.
- Importar desde Excel.
- Notificaciones por correo o WhatsApp.
- Edición o borrado de clientes y pólizas desde la UI.

Está documentado con más detalle en `spec.md`.

---

## 4. Mejora continua (lo del spec que aún no está en código)

Cosas que **sí describí en `spec.md`** pero **no alcancé a implementar** en esta versión. Las dejo explícitas para una siguiente iteración:

| Funcionalidad pendiente | Estado actual |
|-------------------------|---------------|
| Filtrar pólizas por `window` (`expiring`, `in_window`, `out_of_window`) | La API lista todo; no hay filtros en query ni botones en la UI |
| Filtrar por `status` (`active`, `renewed`, `lost`) | Igual que arriba |
| Ver **historial completo** de gestiones por póliza | Solo se muestra última gestión y total en la tabla |
| Detalle de póliza con listado de todas las acciones | Existe `GET /policies/{id}` enriquecido, pero sin array de historial ni pantalla dedicada |
| Dashboard con más métricas (tendencias, % renovación, etc.) | Solo contadores + tabla operativa |

Nada de esto bloquea el MVP del PDF (“ver qué gestionar y registrar acciones”); es deuda alineada con mi propio spec.

---

## 5. Si esto fuera a producción mañana, qué le falta

- Autenticación y que cada asesora vea solo su cartera.
- PostgreSQL (o similar) en lugar de SQLite para concurrencia real.
- Variables de entorno documentadas (`.env.example`) y secretos fuera del repo.
- Filtros e historial completo (ver sección anterior).
- Monitoreo, backups y despliegue automatizado (CI/CD).
- Tests de integración HTTP además de los unitarios de reglas de negocio.
- Revisión de zona horaria Colombia en todos los entornos (hoy está en el servicio de ventana).

---

## 6. Tiempo invertido

Aproximadamente **5 horas** de trabajo real, repartidas en:

- Entender el negocio y escribir `spec.md`
- Backend (modelo, API, seed, CORS)
- Frontend (pantalla, modales, conexión al API)
- Tests de ventana, renovación y prioridad
- `code_review.md`
---

## 7. Qué mejoraría de esta prueba técnica

Sugeriría que el enunciado incluya un **porcentaje orientativo de evaluación** (por ejemplo: 40 % backend, 30 % frontend, 20 % documentación, 10 % tests) o una rúbrica breve. Ayudaría mucho a priorizar sin adivinar si conviene invertir más en filtros del spec o en pulir el video y la entrega.

También sumaría **un párrafo o wireframe mínimo del dashboard esperado** .
---

## 8. Video

**Link al video (máx. 3 min):**
`[]`


---

## 9. Estructura del repositorio

```text
├── spec.md           # Análisis y decisiones antes de codear
├── README.md         # Este archivo
├── code_review.md    # Review del snippet Flask (no está en ai_history/)
├── ai_history/       # Historial de conversaciones con IA
├── src/
│   ├── backend/      # FastAPI + SQLite
│   └── frontend/     # React + Vite
├── tests/            # pytest
├── scripts/          # start_dev.py para levantar todo
└── requirements.txt
```


## 10. Problemas frecuentes al arrancar

**Puerto 8000 ocupado** — Otra instancia de uvicorn ya corre. Usa la app en http://localhost:5173 o cierra el proceso anterior.

**Puerto 5173 ocupado** — Otra instancia de Vite ya corre. Abre http://localhost:5173 o detén el proceso y vuelve a ejecutar `npm run dev`. Vite puede usar 5174 si 5173 está libre; revisa la URL en la terminal.

**Pantalla sin datos** — El backend debe estar en marcha. Sin API, verás ceros y tabla vacía con mensaje de conexión.

---
