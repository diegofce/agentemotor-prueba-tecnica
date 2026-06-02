# Frontend

- Herramienta utilizada: OpenAI CODEX
- Modelo: 5.3
- Fecha: Junio 2026
- Etapa: Planeación y entendimiento del problema

# Promp:

Analiza el proyecto agentemotor-prueba.
Actua como Ingeniero Frontend Senior — Especialista en React.
Resultado: Código listo para producción.
Sin sobreingeniería. Una decisión = una razón.
Las restricciones son requisitos, no sugerencias.

BACKEND: FastAPI + SQLite.
Analiza todos los endpoints para que conectes el frontend correctamnte

// Después de cualquier mutación: volver a consultar

STACK: React  · Vite · TypeScript (estricto)
ESTADO: uso exclusivo de useState/useReducer — sin librerías externas
ESTILOS: CSS puro — sin Tailwind, sin CSS-in-JS
sin detalles innecesarios (no gold-plating)
ERRORES: prohibido el uso de 'any' — tipos explícitos en todas partes
COMPONENTES: solo funcionales + hooks, un archivo por componente

codigo limpio, buenas practicas, la estructura debe quedar en src/frontend

TIPOS: REVISA ES IMPORTANTE -- NO SALGAS DE CONTEXO
REQUISITOS DE INTERFAZ DE USUARIO (UI):

SECCIÓN DE RESUMEN — 4 tarjetas métricas desde GET /summary
· Por vencer · En ventana · Fuera de ventana · Renovadas

TABLA DE PÓLIZAS — desde GET /policies
Columnas: Cliente | Tipo | Vencimiento | Window status | Estado | Última gestión | Acciones
Acciones por fila:
[Registrar gestión] → ActionModal
[Renovar]           → RenewModal

ActionModal
· select: action_type (opciones desde el backend )
· textarea: notes
· POST /policies/{id}/actions → cerrar + volver a consultar todo (refetch)

RenewModal
· input type=date: new_expiry_date
· POST /policies/{id}/renew → cerrar + volver a consultar todo (refetch)

ESTADOS DE CARGA: mostrar por sección, no usar spinner de pantalla completa
ERRORES: mensaje integrado (inline) cerca de la sección afectada

REGLAS DE DISEÑO:
VARIABLES CSS en :root — definir la paleta una sola vez
COLORES: base neutra + 1 color de acento de marca (ej. #1a56db)
RESPONSIVO: CSS Grid / Flexbox — debe funcionar en ≥360px
MODALES: superposición con position: fixed — sin librerías de terceros
TIPOGRAFÍA: conjunto de fuentes del sistema (system-ui), máximo 3 tamaños
ESPACIADO: unidad base de 4px (8, 12, 16, 24, 32)
SIN animaciones / transiciones — mantenerlo ligero
INSIGNIAS DE ESTADO (BADGES): pastilla de color por cada valor de window_status

FORMATO DE SALIDA:
Para CADA archivo, exactamente este formato:

src/api/config.ts
TypeScript
// contenido completo del archivo
AL FINALIZAR TODOS LOS ARCHIVOS: 5 decisiones clave en viñetas, máximo 10 palabras cada una.
NADA MÁS. Sin preámbulos. Sin comentarios finales. Comienza directamente con el primer archivo.

## Respuesta:
Genere la parte del frontende completa, como quieres continuar ?

# Promp:
Revisa toda la implementación frontend.
Actúa como desarrollador fullstack senior.

Busca:

- errores TypeScript
- imports incorrectos
- rutas rotas
- llamadas API incorrectas
- problemas de compilación

Corrige todos los errores.

Objetivo:

npm install
npm run dev

debe funcionar sin modificaciones manuales.

No agregues funcionalidades nuevas.
Solo corrige problemas.

El frontend React corre en:

http://localhost:5173

El backend FastAPI corre en:

http://localhost:8000

Genera la configuración CORS correcta para FastAPI.

Debe permitir desarrollo local.

Explica

## Respuesta:
Ejecuté npm install, npm run build y npm run dev en src/frontend. No hay errores de TypeScript, imports rotos ni fallos de compilación. El frontend arranca en http://localhost:5173/.

Los avisos ECONNREFUSED 127.0.0.1:8000 en la consola de Vite son normales si el backend no está levantado; no indican un bug del código.

RenewModal.tsx (líneas 64-65) está correcto: value y min del input date usan el estado y todayIsoDate().

# Prompt:

Correccion de errores:

Analiza porque no cargan los datos de backend, en el frontend, cual es el problema, en que archivo, que lineas fallan, en network tengo esto:


## Respuesta:

Ejecute los comandos y la pantalla queda en blanco y corrigiendo la carga de datos del backend.

Qué pasaba
La pantalla podía verse “vacía” por dos motivos combinados:

Backend sin datos — Sin uvicorn en el puerto 8000, las peticiones fallan. Solo aparecían el título y mensajes de error pequeños; las tarjetas y la tabla no se mostraban si summary seguía en null o había error en pólizas.
Base sin seed — Si la SQLite estaba vacía, el resumen era todo en 0 y la tabla sin filas, aunque la API respondiera.
