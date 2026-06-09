# Script pour tester l'API en PowerShell
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
& ".\venv\Scripts\Activate.ps1"
Write-Host "Lancement des tests de l'API Patrimoine..." -ForegroundColor Green
Write-Host "Assurez-vous que le serveur Django est en cours d'exécution sur le port 8000" -ForegroundColor Yellow
python test_api_patrimoine.py
