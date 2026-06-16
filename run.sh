#!/bin/bash

# GestiBat - Script de lancement complet (Backend + Frontend)
# Utilisation: ./run.sh [start|stop|dev|help]

set -e

cmd_start() {
    echo "[GestiBat] Demarrage avec Docker..."
    
    if ! command -v docker &> /dev/null; then
        echo "[ERROR] Docker non trouve. Utilise la commande 'dev' pour le mode developpement."
        cmd_dev
        return
    fi
    
    if ! (command -v docker-compose &> /dev/null || docker compose version &> /dev/null); then
        echo "[ERROR] docker-compose non trouve."
        return
    fi
    
    echo "[GestiBat] Construction des images..."
    docker-compose build
    
    echo "[GestiBat] Lancement des conteneurs..."
    docker-compose up -d
    
    echo "[GestiBat] Attente du demarrage (10s)..."
    sleep 10
    
    if docker-compose ps | grep -q "Up"; then
        echo "[OK] GestiBat est en cours d'execution!"
        echo ""
        echo "  Backend:  http://localhost:8000"
        echo "  Frontend: http://localhost:5173"
        echo ""
        echo "[GestiBat] Logs en temps reel (Ctrl+C pour arreter):"
        docker-compose logs -f
    else
        echo "[ERROR] Echec du demarrage"
        exit 1
    fi
}

cmd_dev() {
    echo "[GestiBat] Mode developpement - Ouvre 2 terminaux:"
    echo ""
    echo "=========================================="
    echo "TERMINAL 1 (Backend):"
    echo "=========================================="
    echo "  cd backend"
    echo "  python manage.py runserver 8000"
    echo ""
    echo "=========================================="
    echo "TERMINAL 2 (Frontend):"
    echo "=========================================="
    echo "  cd frontend"
    echo "  npm install  # (si premiere fois)"
    echo "  npm run dev"
    echo ""
}

cmd_stop() {
    echo "[GestiBat] Arret de l'application..."
    if command -v docker &> /dev/null && (command -v docker-compose &> /dev/null || docker compose version &> /dev/null); then
        docker-compose down
        echo "[OK] Conteneurs arretes"
    else
        echo "[INFO] Arrete manuellement le backend et frontend (Ctrl+C)"
    fi
}

cmd_help() {
    echo ""
    echo "Usage: ./run.sh [command]"
    echo ""
    echo "Commandes disponibles:"
    echo "  start  - Demarrer avec Docker (recommande)"
    echo "  dev    - Afficher les instructions pour le mode developpement"
    echo "  stop   - Arreter l'application"
    echo "  help   - Afficher cette aide"
    echo ""
}

# Main
case "$1" in
    start)
        cmd_start
        ;;
    dev)
        cmd_dev
        ;;
    stop)
        cmd_stop
        ;;
    help|--help|-h|"")
        cmd_help
        ;;
    *)
        echo "[ERROR] Commande inconnue: $1"
        echo ""
        cmd_help
        exit 1
        ;;
esac
