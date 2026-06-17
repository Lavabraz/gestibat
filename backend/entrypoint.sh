#!/bin/sh

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente de PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ PostgreSQL est prêt"

# Appliquer les migrations
echo "📦 Application des migrations..."
python manage.py migrate

# Peupler la base de données
echo "🌱 Peuplement de la base..."
python manage.py seed_data

# Lancer le serveur
echo "🚀 Démarrage du backend sur 0.0.0.0:8000"
exec python manage.py runserver 0.0.0.0:8000