# 🚀 GestiBat - Guide de démarrage express

## ⚡ 5 minutes pour tester l'API complète

### Étape 1: Vérifier l'environnement
```bash
cd backend

# Vérifier que les dépendances sont installées
python -c "import django; import rest_framework; print('✅ Django et DRF OK')"

# Vérifier la base de données
python manage.py migrate --check
```

### Étape 2: Démarrer le serveur
```bash
python manage.py runserver 8000
```

✅ Serveur prêt: http://localhost:8000

### Étape 3: Tester l'API

#### Option A: Script Python (RECOMMANDÉ)
```bash
# Terminal 2
python test_api_travaux_dashboard.py
```

Vous verrez:
- ✅ Tests du Dashboard (KPIs, Alertes, Activité)
- ✅ Tests des Travaux (list, filtre, clôture)
- ✅ Tests des Investissements
- ✅ Création de nouveaux travaux

#### Option B: Postman
1. Importer: `GestiBat_API_Travaux_Dashboard.postman_collection.json`
2. Cliquer sur "Login Admin"
3. Tester les endpoints

#### Option C: cURL en 10 secondes
```bash
# Obtenir un token
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  http://localhost:8000/api/auth/login/ | python -m json.tool | grep '"access"' | cut -d'"' -f4)

# 1. Dashboard
echo "=== DASHBOARD ===" 
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/dashboard/ | python -m json.tool | head -30

# 2. Travaux
echo -e "\n=== TRAVAUX ==="
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/travaux/travaux/ | python -m json.tool | head -20

# 3. Stats (pas d'auth)
echo -e "\n=== STATS ==="
curl -s http://localhost:8000/api/patrimoine/stats/ | python -m json.tool
```

---

## 📊 Endpoints clés

### Dashboard (vue globale)
```
GET /api/dashboard/
```
Retourne: KPIs + Alertes + Activité récente

### Travaux
```
GET    /api/travaux/travaux/                  Liste tous
GET    /api/travaux/travaux/?statut=En%20cours  Filtre par statut
GET    /api/travaux/travaux/{id}/             Détail
POST   /api/travaux/travaux/{id}/cloturer/    Clôturer
```

### Investissements
```
GET    /api/travaux/investissements/          Liste tous
GET    /api/travaux/investissements/?statut=Validé  Filtre
```

### Patrimoine
```
GET    /api/patrimoine/sites/                 Sites
GET    /api/patrimoine/batiments/             Bâtiments
GET    /api/patrimoine/stats/                 Stats (no auth)
```

---

## 👥 Utilisateurs test

| Username | Password | Usage |
|----------|----------|-------|
| `admin` | `admin123` | Tests écriture + Dashboard |
| `lecteur` | `lect123` | Tests lecture seule |
| `superadmin` | `super123` | Full access |

---

## 🧪 Tests rapides

### Test 1: Dashboard
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/dashboard/ | jq '.kpis'
```

### Test 2: Travaux urgents
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/travaux/travaux/?statut=En%20cours"
```

### Test 3: Clôturer travaux
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/travaux/travaux/1/cloturer/
```

### Test 4: Créer un travail
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "batiment": 1,
    "service_demandeur": 1,
    "domaine_metier": "Bâtiment",
    "titre_travaux": "Test API",
    "type_travaux": "Entretien",
    "priorite": "Moyenne",
    "date_demande": "2026-06-04",
    "statut": "Proposé"
  }' \
  http://localhost:8000/api/travaux/travaux/
```

---

## 🐍 Utiliser le script de test complet

Le script `test_api_travaux_dashboard.py` execute automatiquement:

✅ **13 tests complets**:
1. Connexion utilisateur
2. Dashboard KPIs
3. Dashboard Alertes
4. Dashboard Activité
5. Liste travaux
6. Filtre par statut
7. Filtre par bâtiment
8. Filtre par domaine
9. Détail travaux
10. Créer un travaux
11. Clôturer un travaux
12. Liste investissements
13. Détail investissements

**Lancer:**
```bash
python test_api_travaux_dashboard.py
```

---

## 📁 Fichiers importants

| Fichier | But |
|---------|-----|
| `test_api_travaux_dashboard.py` | Tests complets (13 tests) |
| `GestiBat_API_Travaux_Dashboard.postman_collection.json` | Collection Postman |
| `API_TRAVAUX_DASHBOARD.md` | Documentation détaillée |
| `API_COMPLETE.md` | Vue d'ensemble de toutes les APIs |

---

## 🔍 Vérifier l'installation

```bash
# Vérifier Django
python manage.py check

# Vérifier les migrations
python manage.py migrate --check

# Vérifier les données
python manage.py shell -c "from travaux.models import Travaux; print(f'Travaux: {Travaux.objects.count()}')"
```

---

## 📞 Besoin d'aide?

### Erreur: "Couldn't import Django"
```bash
source venv/bin/activate
```

### Erreur: "Connection refused"
```bash
python manage.py migrate
python manage.py seed_data
```

### Erreur: "Authentication failed"
```bash
# Vérifier que l'utilisateur existe
python manage.py shell -c "from users.models import CustomUser; print([u.username for u in CustomUser.objects.all()])"
```

### Erreur: "Permission denied" (403)
- Utilisez un user `admin` pour les écritures
- Les `lecteur` peuvent seulement lire

---

## 🎯 Checklist avant de livrer

✅ Base de données peuplée: `python manage.py seed_data`
✅ Serveur démarre: `python manage.py runserver 8000`
✅ Tests OK: `python test_api_travaux_dashboard.py`
✅ Dashboard accessible: `GET /api/dashboard/`
✅ Permissions OK: Admin peut créer, Lecteur peut lire
✅ Données cohérentes: KPIs, alertes, activité

---

## 🚀 Version de production

Pour déployer:

1. **Settings de production**
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

2. **BD PostgreSQL**
```bash
export DATABASE_URL=postgres://user:pass@host/dbname
```

3. **Collecte des statics**
```bash
python manage.py collectstatic
```

4. **Lancer avec Gunicorn**
```bash
gunicorn gestibat.wsgi:application --bind 0.0.0.0:8000
```

---

## 📊 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                  GestiBat API REST                          │
├──────────────────┬──────────────────┬──────────────────────┤
│   Patrimoine     │     Travaux      │     Dashboard        │
├──────────────────┼──────────────────┼──────────────────────┤
│ • Sites          │ • Travaux        │ • KPIs (5)           │
│ • Bâtiments      │ • Investissements│ • Alertes (3 types)  │
│ • Stats          │ • Actions custom │ • Activité (10)      │
│ • 3 filtres      │ • 3 filtres      │ • Auth requise       │
│ • Recherche      │ • Clôture action │ • Performance opti   │
└──────────────────┴──────────────────┴──────────────────────┘

Authentification: JWT Token (4 users test)
Permissions: IsAuthenticated (lecture) | IsAdminUser (écriture)
Performance: < 200ms par endpoint
Tests: 26 tests complets (Python + Postman)
```

---

## 🎉 Vous êtes prêt!

```bash
# Ready?
python manage.py runserver 8000

# Go!
python test_api_travaux_dashboard.py
```

**Bienvenue dans GestiBat! 🏗️**
