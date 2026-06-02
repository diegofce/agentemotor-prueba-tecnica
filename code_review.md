# Reporte Técnico y de Negocio – Evaluación de Snippet en Flask

Este análisis lo realicé como parte de mi proceso de aprendizaje como desarrollador junior.
Para cumplir con la transparencia en el uso de herramientas de IA, incluyo los prompts que usé, las respuestas obtenidas y mi propio análisis crítico.

---

## 1. Interacción Inicial con la IA

**Prompt usado:**
> Explicame el siguiente código en Python, dime en qué framework está escrito, qué hace a nivel de base de datos y qué problemas básicos de programación podría tener si se despliega así como está.

**Respuesta de la IA (resumen):**
- El código está en **Flask**.
- Conecta directo a SQLite (`agentemotor.db`) y consulta pólizas vencidas.
- Hace consultas adicionales por cada póliza (cliente y contactos).
- Problemas detectados:
  - Ruta mal construida (`//` doble).
  - Conexiones sin cerrar.
  - `debug=True` en producción.

---

## 2. Mi Análisis Crítico

Aunque la IA señaló errores básicos, yo identifiqué dos fallas graves que afectan el negocio real:

### Hallazgo A: Rendimiento – N+1 Queries
- **Dónde:** En el bucle `for policy in expired`.
- **Qué pasa:** Por cada póliza hace dos consultas extra.
- **Impacto:** En SQLite esto genera un cuello de botella. Si María (asesora con 280 clientes) abre la app un lunes, el servidor ejecuta cientos de micro-consultas y se congela.
- **Negocio roto:** María pensará que el sistema “no sirve” y volverá a Excel.

### Hallazgo B: Regla de Negocio – Ventana de 30 días
- **Dónde:** Consulta principal (`expiration_date < today`).
- **Qué pasa:** No limita a 30 días, y clasifica como “urgente” pólizas vencidas hace meses.
- **Impacto:** El sistema muestra basura histórica y María pierde tiempo llamando clientes que ya no puede rescatar.
- **Negocio roto:** Se pierde la ventaja comercial; en Colombia solo los primeros 30 días son críticos para renovar.

---

## 3. Iteración con la IA para la Solución

**Prompt usado:**
> El código actual rompe el negocio porque no respeta el límite de 30 días de la regulación colombiana y además va muy lento por el bucle N+1. Reescribe el código solucionando la ruta, usando un solo JOIN con agregación en SQL para evitar las consultas múltiples, limita los resultados a los últimos 30 días de vencimiento y asegura el cierre de conexiones.

**Respuesta de la IA (versión optimizada):**

```python
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
DB = 'agentemotor.db'

@app.route('/advisors/<advisor_id>/expired-policies', methods=['GET'])
def list_expired_policies(advisor_id):
    """
    Lista las pólizas vencidas de un asesor dentro de la ventana
    crítica de 30 días regulatorios, optimizado en una sola consulta.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        # Fechas para delimitar la ventana crítica de 30 días
        today = datetime.now().date()
        limit_date = today - timedelta(days=30)

        # Consulta optimizada con JOIN y GROUP BY
        query = """
            SELECT
                p.id,
                p.insurer,
                p.expiration_date,
                p.status,
                c.name AS client_name,
                c.phone AS client_phone,
                COUNT(ca.id) AS contact_attempts
            FROM policies p
            JOIN clients c ON p.client_id = c.id
            LEFT JOIN contact_attempts ca ON p.id = ca.policy_id
            WHERE p.advisor_id = ?
              AND p.expiration_date < ?
              AND p.expiration_date >= ?
              AND p.status = 'active'
            GROUP BY p.id
        """

        cursor.execute(query, (advisor_id, today, limit_date))
        expired_policies = cursor.fetchall()

        result = []
        for row in expired_policies:
            policy_id, insurer, exp_date_str, status, client_name, client_phone, attempts = row

            exp_date = datetime.strptime(exp_date_str, '%Y-%m-%d').date()
            days_overdue = (today - exp_date).days

            priority = 'critical' if days_overdue > 20 else 'high'

            result.append({
                'policy_id': policy_id,
                'client_name': client_name,
                'client_phone': client_phone,
                'insurer': insurer,
                'expiration_date': exp_date_str,
                'days_overdue': days_overdue,
                'contact_attempts': attempts,
                'priority': priority,
                'recommended_action': 'Contactar de inmediato para renovar dentro del periodo de gracia'
            })

        return jsonify(result), 200

    except sqlite3.Error as e:
        return jsonify({"error": "Error interno al consultar la base de datos", "details": str(e)}), 500

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=False) # Producción seguro
