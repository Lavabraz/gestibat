@echo off
REM GestiBat - Script de démarrage complet pour Windows
REM Ce script lance le backend Django et le frontend Vite

echo ==========================================
echo   GestiBat - Démarrage de l'application
echo ==========================================
echo.

REM Vérifier si Docker est disponible
where docker >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Docker détecté
    echo.
    echo Pour lancer avec Docker (recommandé), exécutez:
    echo   docker-compose up --build
    echo.
    set /p choice=Voulez-vous lancer manuellement sans Docker? (o/n) [n]:
    if /i "%choice%"=="o" (
        set LAUNCH_MANUAL=true
    ) else (
        echo Utilisez: docker-compose up --build
        exit /b 0
    )
) else (
    echo ⚠️  Docker non détecté - Lancement manuel
    set LAUNCH_MANUAL=true
)

if "%LAUNCH_MANUAL%"=="true" (
    echo Lancement manuel du backend et du frontend...
    echo.
    
    REM Vérifier et installer les dépendances backend
    echo 🔍 Vérification du backend...
    if exist "backend" (
        cd backend
        
        REM Vérifier l'environnement virtuel
        if not exist "venv" (
            echo ⚠️  Environnement virtuel non trouvé - création...
            python -m venv venv
        )
        
        REM Activer l'environnement et installer les dépendances
        call venvScriptsactivate
        if exist "requirements.txt" (
            echo 📦 Installation des dépendances Python...
            pip install -r requirements.txt >nul 2>&1
        )
        
        REM Appliquer les migrations
        echo 📦 Application des migrations...
        python manage.py migrate >nul 2>&1
        
        REM Peupler la base de données
        echo 🌱 Peuplement de la base de données...
        python manage.py seed_data >nul 2>&1
        
        REM Lancer le backend dans une nouvelle fenêtre
        echo 🚀 Démarrage du backend sur http://localhost:8000
        start "Backend" cmd /k "cd backend && venvScriptsactivate && python manage.py runserver 8000"
        
        cd ..
    ) else (
        echo ❌ Dossier backend non trouvé!
        exit /b 1
    )
    
    REM Lancer le frontend
    echo 🔍 Vérification du frontend...
    if exist "frontend" (
        cd frontend
        
        REM Installer les dépendances npm
        if exist "package.json" (
            echo 📦 Installation des dépendances npm...
            npm install >nul 2>&1
        )
        
        REM Lancer le frontend dans une nouvelle fenêtre
        echo 🚀 Démarrage du frontend sur http://localhost:5173
        start "Frontend" cmd /k "cd frontend && npm run dev"
        
        cd ..
    ) else (
        echo ❌ Dossier frontend non trouvé!
        exit /b 1
    )
    
    echo.
    echo ==========================================
    echo   ✅ Application démarrée!
    echo ==========================================
    echo.
    echo   Backend:  http://localhost:8000
    echo   Frontend: http://localhost:5173
    echo.
    echo Appuyez sur une touche pour fermer
    echo.
    pause
) else (
    echo Utilisez Docker pour lancer l'application:
    echo   docker-compose up --build
)