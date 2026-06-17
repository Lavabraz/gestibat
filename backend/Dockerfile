FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer netcat-openbsd pour tester la connexion PostgreSQL
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Commande unique avec gestion des erreurs : si une etape echoue, le conteneur crash
CMD sh -c "  echo '⏳ Attente de PostgreSQL...' &&   while ! nc -z db 5432; do sleep 1; done &&   echo '✅ PostgreSQL est pret' &&   echo '📦 Application des migrations...' &&   python manage.py migrate || exit 1 &&   echo '🌱 Peuplement de la base...' &&   python manage.py seed_data || exit 1 &&   echo '🚀 Demarrage du backend sur 0.0.0.0:8000' &&   exec python manage.py runserver 0.0.0.0:8000"
