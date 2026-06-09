@echo off
REM Script pour lancer le serveur Django
cd /d "%~dp0"
call venv\Scripts\activate.bat
python manage.py runserver 8000
