#!/bin/bash

# GestiBat - Script de démarrage complet
# Ce script lance le backend Django et le frontend Vite simultanément

echo "=========================================="
echo "  GestiBat - Démarrage de l'application"
echo "=========================================="
echo ""

# Vérifier si Docker est disponible
if command -v docker &> /dev/null; then
    echo "✅ Docker détecté"
    echo ""
    echo "Pour lancer avec Docker (recommandé), exécutez:"
    echo "  docker-compose up --build"
    echo ""
    read -p "Voulez-vous lancer manuellement sans Docker? (o/n) [n]: " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        LAUNCH_MANUAL=true
    else
        echo "Utilisez: docker-compose up --build"
        exit 0
    fi
else
    echo "⚠️  Docker non détecté - Lancement manuel"
    LAUNCH_MANUAL=true
fi

if [ "$LAUNCH_MANUAL" = true ]; then
    echo "Lancement manuel du backend et du frontend..."
    echo ""
    
    # Vérifier et installer les dépendances backend
    echo "🔍 Vérification du backend..."
    if [ -d "backend" ]; then
        cd backend
        
        # Vérifier l'environnement virtuel
        if [ ! -d "venv" ]; then
            echo "⚠️  Environnement virtuel non trouvé - création..."
            python -m venv venv
        fi
        
        # Activer l'environnement et installer les dépendances
        source venv/bin/activate
        if [ -f "requirements.txt" ]; then
            echo "📦 Installation des dépendances Python..."
            pip install -r requirements.txt > /dev/null 2>&1
        fi
        
        # Appliquer les migrations
        echo "📦 Application des migrations..."
        python manage.py migrate > /dev/null 2>&1
        
        # Peupler la base de données
        echo "🌱 Peuplement de la base de données..."
        python manage.py seed_data > /dev/null 2>&1
        
        # Lancer le backend en arrière-plan
        echo "🚀 Démarrage du backend sur http://localhost:8000"
        python manage.py runserver 8000 &
        BACKEND_PID=$!
        
        cd ..
    else
        echo "❌ Dossier backend non trouvé!"
        exit 1
    fi
    
    # Lancer le frontend
    echo "🔍 Vérification du frontend..."
    if [ -d "frontend" ]; then
        cd frontend
        
        # Installer les dépendances npm
        if [ -f "package.json" ]; then
            echo "📦 Installation des dépendances npm..."
            npm install > /dev/null 2>&1
        fi
        
        # Lancer le frontend en arrière-plan
        echo "🚀 Démarrage du frontend sur http://localhost:5173"
        npm run dev &
        FRONTEND_PID=$!
        
        cd ..
    else
        echo "❌ Dossier frontend non trouvé!"
        kill $BACKEND_PID 2> /dev/null
        exit 1
    fi
    
    echo ""
    echo "=========================================="
    echo "  ✅ Application démarrée!"
    echo "=========================================="
    echo ""
    echo "  Backend:  http://localhost:8000"
    echo "  Frontend: http://localhost:5173"
    echo ""
    echo "Appuyez sur Ctrl+C pour arrêter"
    echo ""
    
    # Attendre que l'utilisateur arrête
    wait
    
    # Nettoyer
    kill $BACKEND_PID 2> /dev/null
    kill $FRONTEND_PID 2> /dev/null
else
    echo "Utilisez Docker pour lancer l'application:"
    echo "  docker-compose up --build"
fi