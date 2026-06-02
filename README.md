# Agentemotor — Cartera de pólizas

## Cómo ejecutar (3 comandos)

Desde la raíz del proyecto:

```bash
pip install -r requirements.txt
```

**Terminal 1 — API** (desde `src/backend`):

```bash
cd src/backend
uvicorn app.main:app --reload
```

**Terminal 2 — Frontend** (desde `src/frontend`):

```bash
cd src/frontend
npm install
npm run dev
```

Abrir http://localhost:5173 (el proxy de Vite reenvía `/summary`, `/policies` y `/openapi.json` al puerto 8000).

Al arrancar, el backend crea la base SQLite y carga datos de demostración automáticamente.

### Error `WinError 10013` al iniciar uvicorn

Significa que el **puerto 8000 ya está en uso** (otra instancia de uvicorn u otra app).

1. Ver qué proceso lo usa:
   ```powershell
   netstat -ano | findstr ":8000"
   ```
2. Si ya es tu API, **no vuelvas a ejecutar uvicorn**: abre solo el frontend en http://localhost:5173
3. Si quieres reiniciar el backend, cierra el proceso anterior (reemplaza `PID` por el número de la columna final):
   ```powershell
   taskkill /PID PID /F
   ```
4. Luego vuelve a ejecutar `uvicorn app.main:app --reload`

Alternativa: otro puerto y actualizar el proxy en `src/frontend/vite.config.ts`:
```bash
uvicorn app.main:app --reload --port 8001
```

### Error `Port 5173 is already in use` al ejecutar `npm run dev`

Otra instancia de Vite ya está corriendo (a menudo de una terminal anterior).

1. **Opción rápida:** abre en el navegador http://localhost:5173 — puede que la app ya esté disponible.
2. Ver el proceso:
   ```powershell
   netstat -ano | findstr ":5173"
   ```
3. Cerrar la instancia anterior (reemplaza `PID`):
   ```powershell
   taskkill /PID PID /F
   ```
4. Vuelve a ejecutar `npm run dev`.

Si 5173 sigue ocupado, Vite usará automáticamente el siguiente puerto libre (por ejemplo 5174); revisa en la terminal la URL que indique.
