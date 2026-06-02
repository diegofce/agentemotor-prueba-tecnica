# Arranca backend y frontend (Windows PowerShell)
$Root = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $Root "src\backend"
$Frontend = Join-Path $Root "src\frontend"

Write-Host "Iniciando API en http://127.0.0.1:8000"
Write-Host "Iniciando frontend en http://localhost:5173"
Write-Host "Cierra esta ventana o Ctrl+C en cada job para detener.`n"

$apiJob = Start-Job -ScriptBlock {
    Set-Location $using:Backend
    python -m uvicorn app.main:app --reload
}

$webJob = Start-Job -ScriptBlock {
    Set-Location $using:Frontend
    npm run dev
}

Receive-Job -Job $apiJob, $webJob -Wait
