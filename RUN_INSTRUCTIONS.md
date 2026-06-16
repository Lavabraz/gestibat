# Instructions pour lancer GestiBat

## Methode 1 : Avec Docker (RECOMMANDE)

Le moyen le plus simple de lancer l application complete (backend + frontend + base de donnees) :

```bash
# A la racine du projet
docker-compose up --build
```

Ce que ca lance :
- Base de donnees PostgreSQL (port 5432)
- Backend Django (port 8000)
- Frontend Vite (port 5173)

Acces :
- Backend API : http://localhost:8000
- Frontend (interface graphique) : http://localhost:5173

---

## Methode 2 : Avec les scripts de demarrage

### Sur Linux/Mac

```bash
# Donner les permissions d execution
chmod +x start.sh

# Lancer l application
./start.sh
```

### Sur Windows

Double-cliquez sur start.bat

---

## Methode 3 : Lancement manuel

### 1. Lancer le backend Django

```bash
cd backend

# Creer et activer l environnement virtuel (si pas deja fait)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dependances
pip install -r requirements.txt

# Appliquer les migrations et peupler la BDD
python manage.py migrate
python manage.py seed_data

# Demarrer le serveur
python manage.py runserver 8000
```

Backend disponible sur : http://localhost:8000

### 2. Lancer le frontend Vite

Dans un nouveau terminal :

```bash
cd frontend

# Installer les dependances
npm install

# Demarrer l application
npm run dev
```

Frontend disponible sur : http://localhost:5173

---

## Resume des URLs

| Service | URL | Description |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | API REST Django |
| Frontend | http://localhost:5173 | Interface graphique |
| Base de donnees | localhost:5432 | PostgreSQL (Docker uniquement) |

---

## Identifiants de test

| Utilisateur | Mot de passe | Role |
|-------------|--------------|------|
| admin | admin123 | Administrateur (acces complet) |
| superadmin | super123 | Super administrateur |
| lecteur | lect123 | Lecture seule |

---

## Navigation dans l application

Une fois connecte, vous avez acces a :

- Tableau de bord (/dashboard) - Vue d ensemble avec KPIs et alertes
- Travaux (/travaux) - Liste et gestion des travaux
- Investissements (/travaux/investissements) - Liste des investissements
- Patrimoine (/patrimoine/batiments) - Gestion des batiments et sites
- Utilisateurs (/users/agents) - Gestion des agents

---

## Resolution des problemes

### Probleme : Le frontend ne se connecte pas au backend

Solution : Verifiez que le backend est bien lance sur http://localhost:8000
Dans le frontend, verifiez le fichier .env :
VITE_API_URL=http://localhost:8000/api

### Probleme : Les donnees ne s affichent pas

Solution : Executez le script de peuplement de la base de donnees :
cd backend
python manage.py seed_data

### Probleme : Erreur de migration

Solution : Appliquez les migrations :
cd backend
python manage.py migrate

---

## Conseils

- Pour le developpement : Utilisez Docker pour une experience coherente
- Pour tester l API : Utilisez Postman avec les collections fournies
