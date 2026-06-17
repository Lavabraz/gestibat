FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer netcat pour tester la connexion PostgreSQL
RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Rendre entrypoint.sh exécutable
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Utiliser entrypoint.sh comme point d'entrée
ENTRYPOINT ["./entrypoint.sh"]