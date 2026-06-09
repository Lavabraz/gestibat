# 🏗️ API REST Patrimoine - GestiBat

## 📋 État de l'implémentation

✅ **API Patrimoine complètement implémentée et testée**

### Endpoints disponibles

#### 1. **Sites** (`/api/patrimoine/sites/`)
- `GET /api/patrimoine/sites/` - Liste tous les sites avec annotation du nombre de bâtiments
- `GET /api/patrimoine/sites/?ville=Ambert` - Filtre par ville
- `GET /api/patrimoine/sites/?search=piscine` - Recherche par nom
- `GET /api/patrimoine/sites/{id}/` - Détail d'un site avec bâtiments imbriqués

#### 2. **Bâtiments** (`/api/patrimoine/batiments/`)
- `GET /api/patrimoine/batiments/` - Liste tous les bâtiments
- `GET /api/patrimoine/batiments/?site=1` - Filtre par site
- `GET /api/patrimoine/batiments/?type_usage=Administratif` - Filtre par type d'usage
- `GET /api/patrimoine/batiments/?ville=Ambert` - Filtre par ville
- `GET /api/patrimoine/batiments/?search=mairie` - Recherche par nom/code
- `GET /api/patrimoine/batiments/?ordering=nom_batiment` - Tri par nom
- `GET /api/patrimoine/batiments/?ordering=-surface_m2` - Tri par surface (décroissant)
- `GET /api/patrimoine/batiments/{id}/` - Détail complet avec:
  - Caractéristiques techniques
  - Services occupants
  - Compteurs associés
  - Derniers travaux (max 3)

#### 3. **Statistiques** (`/api/patrimoine/stats/`)
- `GET /api/patrimoine/stats/` - Stats globales (pas d'authentification requise)
  - Total bâtiments
  - Total sites
  - Surface totale
  - Distribution par type d'usage
  - Distribution par ville

---

## 🔐 Authentification & Permissions

### Utilisateurs de test disponibles
```
Username    | Password   | Rôle
------------|------------|------------------
admin       | admin123   | admin (écriture)
editeur     | edit123    | editeur (lecture)
lecteur     | lect123    | lecteur (lecture)
superadmin  | super123   | super_admin (full)
```

### Permissions par endpoint
- **Lecture (GET)**: `IsAuthenticated` (nécessite un token)
- **Écriture (POST/PUT/DELETE)**: `IsAdminUser` (admin ou super_admin)
- **Statistiques**: `AllowAny` (pas d'authentification requise)

---

## 🧪 Tests

### Option 1: Script Python (recommandé)
```bash
cd backend

# Lancer le serveur Django
python run_server.ps1  # Windows PowerShell
# ou
bash -c "source venv/bin/activate && python manage.py runserver 8000"  # Linux/Mac

# Dans un autre terminal, lancer les tests
python test_api_patrimoine.py
```

### Option 2: Postman/Insomnia
1. Importer la collection: `GestiBat_API_Patrimoine.postman_collection.json`
2. Définir l'environnement: `base_url` = `http://localhost:8000`
3. Exécuter les tests dans l'ordre:
   - Login Admin (pour générer le token)
   - Puis tester les endpoints

### Option 3: cURL
```bash
# Obtenir un token
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  http://localhost:8000/api/auth/login/ | jq -r '.access')

# Tester un endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/patrimoine/sites/

# Stats (pas d'auth)
curl http://localhost:8000/api/patrimoine/stats/
```

---

## 📊 Données disponibles

Après exécution du `seed_data`:

- **5 Sites** à Ambert
- **20 Bâtiments** avec codes patrimoine
- **30 Compteurs** (Eau, Électricité, Gaz)
- **60 Consommations** mensuelles
- **10 Travaux** avec statuts variés
- **5 Investissements**

---

## 📁 Fichiers

### Backend
- `patrimoine/views.py` - ViewSets (SiteViewSet, BatimentViewSet, PatrimoineStatsAPIView)
- `patrimoine/serializers.py` - Sérializers avec nested relations
- `patrimoine/urls.py` - Routes et router
- `patrimoine/models.py` - Modèles Django

### Tests & Documentation
- `test_api_patrimoine.py` - Script de test complet Python
- `run_server.ps1` - Script pour lancer le serveur (PowerShell)
- `run_server.bat` - Script pour lancer le serveur (CMD)
- `test_api.ps1` - Script pour lancer les tests (PowerShell)
- `GestiBat_API_Patrimoine.postman_collection.json` - Collection Postman

### Documentation
- `API_PATRIMOINE.md` - Documentation API complète
- `README.md` - Ce fichier

---

## 🚀 Démarrage rapide

### 1. Installation (première fois)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.ps1  # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
```

### 2. Lancer le serveur
```bash
cd backend
python manage.py runserver 8000
```

### 3. Tester l'API
```bash
# Via Python
python test_api_patrimoine.py

# Via Postman: Importer GestiBat_API_Patrimoine.postman_collection.json

# Via curl
curl http://localhost:8000/api/patrimoine/stats/
```

---

## 📚 Exemples d'utilisation

### JavaScript/TypeScript (Fetch API)
```javascript
// Obtenir un token
const loginResponse = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'admin123' })
});
const { access } = await loginResponse.json();

// Utiliser le token
const headers = {
  'Authorization': `Bearer ${access}`,
  'Content-Type': 'application/json'
};

// Obtenir les sites
const sitesResponse = await fetch('http://localhost:8000/api/patrimoine/sites/', { headers });
const sites = await sitesResponse.json();
console.log(sites);
```

### Python (requests)
```python
import requests

BASE_URL = 'http://localhost:8000/api'

# Login
response = requests.post(f'{BASE_URL}/auth/login/', 
  json={'username': 'admin', 'password': 'admin123'})
token = response.json()['access']

# Headers avec token
headers = {'Authorization': f'Bearer {token}'}

# Récupérer les sites
sites = requests.get(f'{BASE_URL}/patrimoine/sites/', headers=headers).json()
print(sites)

# Filtrer par ville
sites_ambert = requests.get(
  f'{BASE_URL}/patrimoine/sites/?ville=Ambert', 
  headers=headers
).json()
```

---

## ✅ Checklist d'implémentation

- ✅ SiteViewSet avec list et retrieve
- ✅ Annotation `nombre_batiments` sur les sites
- ✅ Filtre par ville sur sites
- ✅ Recherche par nom sur sites
- ✅ BatimentViewSet avec list et retrieve
- ✅ Champs légers en list (site_nom, surface_m2, code_patrimoine, ville)
- ✅ Détail complet avec nested relations
- ✅ Filtres: site, type_usage, ville
- ✅ Recherche par nom/code
- ✅ Tri flexible (nom, surface, année, code)
- ✅ BatimentListSerializer
- ✅ BatimentDetailSerializer avec nested
- ✅ BatimentCaracteristiquesSerializer
- ✅ Endpoint stats avec distribution par type et ville
- ✅ Permissions: IsAuthenticated pour lecture
- ✅ Permissions: IsAdminUser pour écriture
- ✅ Permissions: AllowAny pour stats
- ✅ Sérializers imbriqués (services, compteurs, travaux)
- ✅ Derniers travaux (max 3) dans le détail

---

## 🐛 Troubleshooting

### Erreur: "Couldn't import Django"
```bash
# Vérifier l'environnement
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.ps1  # Windows

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur: "Connection refused" sur la base de données
```bash
# Vérifier que la migration est faite
python manage.py migrate

# Ou utiliser SQLite (déjà configuré)
# Vérifier le fichier .env
cat .env
```

### Erreur: "Authentication credentials were not provided"
Ajouter le header `Authorization: Bearer TOKEN` à votre requête

---

## 📞 Support

Pour plus d'informations:
- Voir `API_PATRIMOINE.md` pour la documentation détaillée
- Consulter `test_api_patrimoine.py` pour des exemples
- Utiliser la collection Postman pour tester interactivement

---

**Version**: 1.0  
**Dernière mise à jour**: 2026-06-04  
**Statut**: ✅ Production-ready
