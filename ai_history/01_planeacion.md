# Planeación

- Herramienta utilizada: Claude
- Fecha: Junio 2026
- Etapa: Planeación y entendimiento del problema

**Nota: Esta sección documenta el proceso de planeación y entendimiento del problema antes de escribir código. Incluye las consultas realizadas a Claude, las respuestas obtenidas y las decisiones tomadas a partir de esa información. en los siguientes archivos pegare las consultas y respuestas exactas.**

## 1. Consulta inicial: contexto del negocio

> **Consulta:** Explícame cómo funciona el negocio de seguros en Colombia, cómo la empresa Agentemotor hace el papel de intermediario entre aseguradoras y asesores y cuáles son sus actores principales.

### Motivo de la consulta

No tenía claridad sobre el flujo real entre aseguradoras, asesores y Agentemotor.

Antes de definir funcionalidades, hice una investigación rápida del dominio para entender mejor los actores del negocio y la relación entre aseguradoras, asesores y plataformas SaaS como Agentemotor.

### Respuesta resumida

El mercado de seguros en Colombia está regulado por la Superintendencia Financiera. El modelo se basa en transferir el riesgo de un tercero, el cliente, a una aseguradora a cambio del pago de una prima.

Aunque existen canales de venta directa, la mayoría de los seguros se comercializa a través de intermediarios como asesores, agencias y corredores. El cliente suele preferirlos porque actúan como consultores de confianza, ayudan a comparar opciones y dan acompañamiento si ocurre un siniestro como un accidente o un robo.

#### Rol de Agentemotor

Agentemotor no es una aseguradora ni vende seguros al público final. Su papel es el de un habilitador tecnológico o plataforma SaaS B2B.

#### Problema tradicional

Para cotizar un seguro de carro, un asesor independiente debía entrar manualmente a varias plataformas de aseguradoras, repetir los mismos datos muchas veces y descargar varias propuestas en PDF. Ese flujo consumía horas.

#### Solución de Agentemotor

Agentemotor funciona como un multicotizador centralizado. Mediante integraciones API, reúne a varias aseguradoras en una sola pantalla. El asesor ingresa los datos una vez, la plataforma consulta las compañías en tiempo real y devuelve tarifas y coberturas comparadas en pocos minutos. También puede facilitar la emisión directa de la póliza.

### Actores principales del ecosistema

- Aseguradoras.
- Agentemotor.
- Intermediarios: asesores, agencias y corredores.
- Cliente final.

### Decisiones tomadas a partir de esta información

- El sistema estará orientado a un asesor.
- No modelaré aseguradoras como usuarios.
- Priorizaré la gestión de renovaciones.

## 2. Consulta: qué está evaluando realmente Agentemotor

> **Consulta:** ¿Qué está evaluando realmente Agentemotor? No me hables de tecnologías todavía.
>
> Voy a presentar una prueba técnica. Antes de escribir código quiero entender el problema de negocio. Te paso el enunciado completo.
>
> [pegué el enunciado]
>
> Primera pregunta: ¿qué está evaluando realmente Agentemotor? No me hables de tecnologías todavía.

### Respuesta

Lo que más me llama la atención es esto: "No te vamos a decir exactamente qué funcionalidades incluir. Tú decides." Eso no es una prueba técnica estándar.
Es una prueba de criterio.
El dato técnico más importante del enunciado no es el stack — es la ventana de 30 días. Eso define toda la lógica del producto. Si tu sistema no diferencia entre una póliza vencida hace 15 días y una vencida hace 45 días, no resolviste el problema de María, aunque el CRUD funcione perfectamente.

### Decisiones tomadas a partir de esta información

- Voy a enfocarme en la lógica de negocio que resuelve el problema de María, no en CRUDs o integraciones.
- Voy a priorizar la ventana de 30 días para definir las funcionalidades mínimas.

## 3. Consulta: entidad central del sistema

> **Consulta:** ¿Cuál es la tabla más importante del sistema?

### Motivo de la consulta

Quiero entender cuál es la entidad central del sistema para diseñar una base de datos eficiente y enfocada en el problema de negocio.

### Respuesta

No es policies. Es management_actions.
El Excel de María tenía un problema de contexto, no de estructura. La columna X solo decía "gestionado o no". No guardaba qué pasó. La tabla de acciones de gestión, con tipo_accion y notas libres, es lo que hace esta app mejor que el Excel. Sin ella, construiste un Excel con mejor UI.

### Decisiones tomadas a partir de esta información

- Voy a diseñar la base de datos con management_actions como tabla central.
- Me aseguraré de que cada acción de gestión tenga un tipo y notas detalladas para capturar el contexto completo de cada interacción con el cliente.

## 4. Consulta: estado de vencimiento

> **Consulta:** ¿Debería almacenar en la base de datos la ventana de estado de cada póliza? Es decir, si está vencida hace 15 días o 45 días, o debería calcularlo en tiempo real? ¿Cuál es mejor práctica?

### Motivo de la consulta

Quiero entender la mejor práctica para manejar estados temporales en una base de datos, especialmente en un sistema que depende de ventanas de tiempo para su lógica de negocio.

### Respuesta

Calcularlo siempre. Si lo almacenas necesitas un job nocturno que lo actualice.
Si ese job falla, María toma decisiones el lunes con datos incorrectos — puede ignorar una póliza crítica o llamar a alguien que ya se perdió.

Al calcularlo en el servicio en cada petición, siempre refleja la realidad. El costo es mínimo: una resta de fechas por póliza.

Esta es probablemente la decisión más importante de toda la arquitectura para el negocio de María.

### Decisiones tomadas a partir de esta información

- No almacenaré el estado de vencimiento en la base de datos.
- Implementaré la lógica para calcular el estado de cada póliza en tiempo real cada vez que se consulte la información, asegurando que María siempre tenga datos precisos para tomar decisiones informadas.

## 5. Consulta:

> **Consulta:** ¿Qué funcionalidades mínimas debería tener la primera versión para resolver el problema de María?

### Motivo de la consulta

Quiero definir un MVP claro y enfocado en resolver el problema principal de María, sin agregar funcionalidades innecesarias que puedan complicar el desarrollo inicial.

### Respuesta

El MVP para resolver el problema de María debería incluir:

1. Una interfaz sencilla para visualizar las pólizas y su estado de vencimiento.
2. La capacidad de filtrar pólizas por su estado, por ejemplo, vencidas en los últimos 30 días.
3. La posibilidad de agregar notas y acciones de gestión a cada póliza.

### Decisiones tomadas a partir de esta información

Decidí enfocarme en:

- listado de pólizas
- historial de gestión
- renovación
- filtros

y dejar fuera autenticación, notificaciones e integraciones.

## 6. Consulta: visibilidad de pólizas renovadas

> **Consulta:** ¿Tiene sentido que una póliza renovada siga apareciendo en la lista principal?

### Motivo de la consulta

Quiero entender cómo manejar el ciclo de vida de una póliza en la interfaz de usuario, especialmente después de que ha sido renovada, para asegurarme de que la experiencia del usuario sea intuitiva y eficiente.

### Respuesta

No, no tiene sentido. Si una póliza ya fue renovada, no debería aparecer en la lista principal de pólizas vencidas o por vencer. Debería moverse a una sección de "Pólizas renovadas" o simplemente desaparecer de la vista principal para evitar confusión y permitir que María se enfoque en las pólizas que realmente necesitan atención.

### Decisiones tomadas a partir de esta información

Decidí que las pólizas renovadas salgan de la vista operativa principal porque ya no representan trabajo pendiente.

## 7. Consulta: qué probar en los tests

> **Consulta:** ¿Qué debería probar en los tests?

### Motivo de la consulta

Quiero asegurarme de que los tests cubran las funcionalidades críticas del sistema, especialmente aquellas relacionadas con la lógica de negocio que resuelve el problema de María, para garantizar que el sistema funcione correctamente y sea confiable.

### Respuesta

Deberías probar:

- El cálculo correcto de la ventana de vencimiento para diferentes fechas de vencimiento.
- La correcta visualización de las pólizas según su estado: vencida, por vencer o renovada.
- La funcionalidad de agregar notas y acciones de gestión a las pólizas.

### Decisiones tomadas a partir de esta información

Identifiqué que el cálculo de ventana es la regla más crítica del negocio.

Los tests se enfocarán en:

- póliza dentro de ventana
- póliza fuera de ventana
- renovación


## Resultado final de la etapa

**Después de las consultas realizadas se decidió:**

- FastAPI
- React
- SQLite
- Estado calculado
- Gestión como funcionalidad principal
- Sin autenticación
