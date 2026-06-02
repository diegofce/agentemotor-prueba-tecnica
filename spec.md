Autor: Diego Fernando Chacon
Fecha: Junio de 2026
Tiempo dedicado: 50 min

# Spec del proyecto

## 1. Análisis de cómo entendí el problema

María es una asesora de seguros que administra aproximadamente 280 clientes activos. Hoy lleva el seguimiento en Excel, pero esa solución le hace perder contexto, se rompe con facilidad y no refleja la urgencia real del negocio. Como resultado, pierde entre 5 y 10 clientes al mes.

Según el enunciado, la pérdida de clientes parece estar relacionada con la dificultad para priorizar renovaciones y mantener contexto sobre las gestiones realizadas.

## 2. Datos clave del modelo del negocio

En Colombia, una póliza vencida puede renovarse por el mismo intermediario dentro de los 30 días siguientes al vencimiento. Después de ese plazo, María compite en igualdad de condiciones con cualquier otro asesor.

Eso significa que el tiempo no se maneja de forma lineal:

- Si una póliza venció hace 29 días, todavía queda 1 día de prioridad comercial.
- Si una póliza venció hace 31 días, ya salió de la ventana prioritaria.

El umbral operativo de 30 días se usa en ambos sentidos porque coincide con la ventana legal de renovación: permite anticipar el vencimiento con la misma lógica con la que se mide la pérdida de prioridad después de vencer. Evita tener dos reglas distintas para una sola decisión de negocio.

**Decisión de diseño:**
Se utiliza la misma ventana de 30 días antes y después del vencimiento para simplificar la priorización operativa.

### Estados de una póliza

Por vencer: faltan entre 0 y 30 días para el vencimiento.

En ventana: han pasado entre 1 y 30 días desde el vencimiento.

Fuera de ventana: han pasado más de 30 días desde el vencimiento.

Renovada: la póliza fue actualizada con una nueva fecha.

## 3. Objetivos (Lo que decidí construir y lo que no)

Construir una aplicación web sencilla, clara y escalable para que María reemplace su Excel con una herramienta enfocada en:

- organizar la cartera de pólizas;
- priorizar los vencimientos urgentes;
- registrar gestiones comerciales;
- reducir la pérdida de clientes por seguimiento tardío.

### Lo que sí debe hacer

- Mostrar una cartera ordenada por urgencia regulatoria.
- Permitir registrar acciones de gestión con notas libres.
- Permitir marcar una póliza como renovada con nueva fecha.
- Permitir filtrar por estado de ventana.
- Mostrar contadores resumidos en el encabezado.

### Lo que no voy a construir

- Login o autenticación.
- Multiusuario en esta primera versión.
- Cotización o emisión de pólizas.
- Funciones contables o financieras.
- Envío de correos o mensajes a clientes.
- Importación desde Excel.
- Notificaciones automáticas.

No implementé edición ni eliminación de clientes y pólizas porque el flujo principal del problema consiste en gestionar renovaciones y registrar acciones comerciales. Priorizo funcionalidades directamente relacionadas con la pérdida de clientes descrita en el enunciado. Pero es una mejora que se puede implementar a futuro sin afectar la arquitectura general.

## 4. Alcance funcional

### Casos principales

- Ver la cartera ordenada por urgencia.
- Registrar acciones de gestión por póliza.
- Marcar pólizas como renovadas.
- Filtrar por estado de ventana.
- Consultar el historial de gestiones.
- Ver contadores por estado en el encabezado.

### Fuera del alcance

- Autenticación.
- Roles de usuario.
- Integraciones con aseguradoras.
- Dashboard de analítica avanzada.
- Automatizaciones por correo o WhatsApp.

## 5. Supuestos

- Solo existe una asesora en la primera versión: María.
- Más adelante se podría habilitar multiusuario sin rediseñar todo el modelo.
- La tabla advisors existe en el modelo para facilitar la extensión multi-asesor sin rediseñar el esquema.
- No se implementa autenticación en esta versión.
- Todas las fechas se manejan en zona horaria de Colombia.
- Una póliza pertenece a un único cliente.
- Un cliente puede tener varias pólizas.
- No se consideran cancelaciones parciales.
- No hay integración con aseguradoras reales.

## 6. Flujos principales

### Flujo principal de trabajo

```text
1. María entra a la aplicación.
2. El encabezado muestra los contadores: por vencer, en ventana y fuera de ventana.
3. La tabla aparece ordenada automáticamente por urgencia.
4. Filtra "en ventana" y ve solo las pólizas críticas.
5. Abre una póliza y revisa cliente, fecha de vencimiento e historial.
6. Registra una gestión con notas.
7. Continúa con la siguiente póliza prioritaria.
```

### Flujo de renovación

```text
1. María abre el detalle de una póliza en ventana.
2. El cliente confirma la renovación.
3. María marca la póliza como renovada.
4. Ingresa la nueva fecha de vencimiento.
5. El sistema valida la fecha y crea automáticamente la gestión de renovación.
6. La póliza cambia de estado y desaparece de la vista activa.
7. El contador de la ventana prioritaria disminuye.
```

### Flujo automático al cruzar el día 30

```text
1. María consulta la cartera sin ejecutar un job nocturno.
2. El sistema recalcula el estado de ventana en ese momento.
3. Si la póliza cumple 30 días desde el vencimiento, sale automáticamente de la ventana prioritaria.
4. La vista refleja el cambio sin tareas programadas en segundo plano.
```

### Cálculo automático del estado

```text
1. No existe un job nocturno para recalcular estados.
2. El sistema calcula el estado de ventana en cada consulta.
3. Cuando una póliza cruza el día 30, cambia de estado automáticamente.
4. María siempre ve la situación real sin depender de tareas programadas.
```

## 7. Reglas del negocio

- Una póliza vencida hace más de 30 días sale de la ventana prioritaria.
- Una póliza renovada debe registrar automáticamente una gestión de tipo renovada.
- No se puede registrar una fecha de renovación anterior a la fecha actual.
- Las pólizas se ordenan por urgencia regulatoria.
- Toda gestión debe quedar asociada a una póliza.
- Las pólizas dentro de la ventana de renovación tienen mayor prioridad que las próximas a vencer.

## 8. Modelo de datos

La base de datos usará nombres de tablas y campos en inglés para mantener consistencia técnica.

### Tablas principales

```text
### advisors
- id: INTEGER, PK
- full_name: VARCHAR(200), NOT NULL
- email: VARCHAR(200), UNIQUE
- created_at: DATETIME, NOT NULL

### clients
- id: INTEGER, PK
- advisor_id: FK → advisors.id, NOT NULL
- full_name: VARCHAR(200), NOT NULL
- phone: VARCHAR(20)
- email: VARCHAR(200)
- created_at: DATETIME, NOT NULL

### policies
- id: INTEGER, PK
- client_id: FK → clients.id, NOT NULL
- insurer: VARCHAR(100), NOT NULL
- policy_type: VARCHAR(20), NOT NULL *(auto | hogar | vida)*
- policy_number: VARCHAR(100), UNIQUE
- expiration_date: DATE, NOT NULL
- status: VARCHAR(20), NOT NULL, DEFAULT 'active' *(active | renewed | lost)*
- created_at: DATETIME, NOT NULL
- updated_at: DATETIME, NOT NULL

### management_actions
- id: INTEGER, PK
- policy_id: FK → policies.id, NOT NULL
- action_type: VARCHAR(40), NOT NULL
  *(call_no_answer | call_success | renewal_scheduled | renewed | lost | note)*
- notes: TEXT, NULL
- created_at: DATETIME, NOT NULL

```

### Por qué `window_status` no se guarda como columna

El estado de ventana depende de la fecha actual y de la fecha de vencimiento. Si se almacenara en la base de datos, habría que mantenerlo sincronizado con procesos programados. Calcularlo en cada consulta evita inconsistencias y garantiza que María siempre vea el estado real.

## 9. API REST - Endpoints expuestos

La API usa rutas simples y predecibles.

### Clients

Los métodos disponibles para la ruta /clients son los siguientes:

- GET /clients: devuelve la lista de clientes.

- POST /clients: crea un nuevo cliente.

- GET /clients/{id}: obtiene el detalle de un cliente específico según su identificador.

### Policies

- GET /policies?status=...: devuelve la lista de pólizas según el estado real de la póliza.

- GET /policies?window=...: devuelve la lista de pólizas según la ventana calculada.

- POST /policies: crea una nueva póliza.

- GET /policies/{id}: obtiene el detalle de una póliza y su historial completo.

- POST /policies/{id}/actions: registra una gestión sobre la póliza.

- POST /policies/{id}/renew: marca la póliza como renovada con una nueva fecha.

### Summary

- GET /summary: devuelve los contadores que se muestran en el encabezado.

### Parámetros útiles de consulta

- `status=active`
- `status=renewed`
- `status=lost`
- `window=expiring`
- `window=in_window`
- `window=out_of_window`

### Respuesta enriquecida de `GET /policies`

```json
{
  "id": 1,
  "client_id": 10,
  "client_name": "Carlos Ramírez",
  "client_phone": "3001234567",
  "insurer": "Sura",
  "policy_type": "auto",
  "expiration_date": "2026-05-01",
  "status": "active",
  "window_status": "in_window",
  "days_overdue": 24,
  "days_remaining_in_window": 6,
  "last_action": "call_success",
  "last_action_at": "2026-05-20T10:30:00",
  "total_actions": 2
}
```

## 10. Arquitectura

La solución está organizada en **tres capas principales**, pensadas para que el sistema sea fácil de mantener hoy y pueda escalar mañana:

1. **Interfaz de usuario (UI)**
   - Construida con **React + Vite**.
2. **Backend (API)**
   - Implementado en **FastAPI**.
   - Incluye **Schemas Pydantic** para validar datos y dar respuestas confiables.

3. **Servicios y repositorios**
   - **Servicios (SVC):** contienen las reglas de negocio, como calcular el `window_status` en cada consulta.
   - **Repositorios (REP):** gestionan el acceso a datos.
   - **Base de datos (DB):** actualmente **SQLite**, pero preparada para migrar a motores más robustos.

### Decisiones técnicas

- **Frontend:** React con Vite, porque permite una interfaz rápida, interactiva y simple para este alcance. La interfaz mostrará textos y acciones en español.
- **Backend:** FastAPI, porque ofrece validación automática, OpenAPI y una estructura clara para APIs REST.
- **Base de datos:** SQLite, porque es suficiente para una sola asesora y facilita correr la app localmente.

## 11. Trade-offs

### Estado de ventana: calculado vs almacenado

- **Calculado:** siempre refleja la realidad actual.
- **Almacenado:** exige sincronización y puede quedar desactualizado si falla un proceso programado.
- **Decisión:** calcular siempre el estado de ventana en cada consulta.

### Modal vs rutas separadas

- **Modal:** mantiene el contexto de la lista activa y acelera el flujo de trabajo.
- **Rutas separadas:** agregan fricción para una aplicación tan pequeña.
- **Decisión:** usar modal para ver detalle y registrar gestiones.

### SQLite vs PostgreSQL

- **SQLite:** suficiente para el MVP y muy fácil de ejecutar.
- **PostgreSQL:** será una evolución natural cuando crezca la necesidad.
- **Decisión:** arrancar con SQLite y dejar el acceso desacoplado para migrar después con poco cambio.

## 12. Prioridad operativa

La interfaz debe ordenar la cartera con esta lógica general:

1. Pólizas en ventana prioritaria.
2. Pólizas por vencer.
3. Pólizas fuera de ventana.
4. Pólizas renovadas.
