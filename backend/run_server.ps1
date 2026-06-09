# Script pour lancer le serveur Django en PowerShell
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
& ".\venv\Scripts\Activate.ps1"
python manage.py runserver 8000
