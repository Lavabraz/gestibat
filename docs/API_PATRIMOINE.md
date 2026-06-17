# 📡 API REST - Patrimoine GestiBat

## 🚀 Vue d'ensemble

L'API REST complète pour la gestion du patrimoine immobilier avec Django REST Framework.

### Configuration
- **Base URL**: `http://localhost:8000/api/patrimoine/`
- **Format**: JSON
- **Authentification**: JWT Token (optionnelle pour stats, obligatoire pour autres endpoints)
- **Permissions**: 
  - **Lecture (GET)**: `IsAuthenticated`
  - **Écriture (POST/PUT/DELETE)**: `IsAdminUser` (super_admin, admin)

---

## 📍 Endpoints

### 1. SITES

#### List all sites
```http
GET /api/patrimoine/sites/
```

**Paramètres de requête**:
- `ville`: Filtrer par ville (ex: `?ville=Ambert`)
- `search`: Chercher par nom (ex: `?search=piscine`)
- `page`: Pagination (ex: `?page=2`)
- `page_size`: Éléments par page (ex: `?page_size=20`)

**Réponse** (200):
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id_site": 1,
      "nom_site": "Mairie Ambert",
      "adresse": "Place Charles de Gaulle",
      "ville": "Ambert",
      "nombre_batiments": 4
    },
    {
      "id_site": 2,
      "nom_site": "Piscine Ambert Livradois Forez",
      "adresse": "Avenue des Sports",
      "ville": "Ambert",
      "nombre_batiments": 3
    }
  ]
}
```

**Exemple cURL**:
```bash
# Tous les sites
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/patrimoine/sites/

# Sites à Ambert
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/patrimoine/sites/?ville=Ambert"

# Rechercher "piscine"
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/patrimoine/sites/?search=piscine"
```

---

#### Retrieve site details
```http
GET /api/patrimoine/sites/{id}/
```

**Réponse** (200):
```json
{
  "id_site": 1,
  "nom_site": "Mairie Ambert",
  "adresse": "Place Charles de Gaulle",
  "ville": "Ambert",
  "batiments": [
    {
      "id_batiment": 1,
      "nom_batiment": "Mairie Ambert - Batiment 01",
      "code_patrimoine": "CALF-BAT-001",
      "surface_m2": "629.50",
      "annee_construction": 1987
    },
    {
      "id_batiment": 6,
      "nom_batiment": "Mairie Ambert - Batiment 06",
      "code_patrimoine": "CALF-BAT-006",
      "surface_m2": "1245.75",
      "annee_construction": 2005
    }
  ]
}
```

**Exemple cURL**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/patrimoine/sites/1/
```

---

### 2. BÂTIMENTS

#### List all buildings
```http
GET /api/patrimoine/batiments/
```

**Paramètres de requête**:
- `site`: ID du site (ex: `?site=1`)
- `type_usage`: Type d'usage (ex: `?type_usage=Administratif`)
- `ville`: Ville (ex: `?ville=Ambert`)
- `search`: Chercher par nom/code (ex: `?search=mairie`)
- `ordering`: Tri (ex: `?ordering=nom_batiment` ou `?ordering=-surface_m2`)

**Réponse** (200):
```json
{
  "count": 20,
  "next": null,
  "previous": null,
  "results": [
    {
      "id_batiment": 1,
      "nom_batiment": "Mairie Ambert - Batiment 01",
      "code_patrimoine": "CALF-BAT-001",
      "surface_m2": "629.50",
      "site": 1,
      "site_nom": "Mairie Ambert",
      "ville": "Ambert",
      "type_usage": "Administratif"
    },
    {
      "id_batiment": 2,
      "nom_batiment": "Centre Culturel - Batiment 02",
      "code_patrimoine": "CALF-BAT-002",
      "surface_m2": "572.50",
      "site": 2,
      "site_nom": "Centre Culturel",
      "ville": "Ambert",
      "type_usage": "Culturel"
    }
  ]
}
```

**Exemples cURL**:
```bash
# Tous les bâtiments
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/patrimoine/batiments/

# Bâtiments du site 1
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/patrimoine/batiments/?site=1"

# Bâtiments administratifs
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/patrimoine/batiments/?type_usage=Administratif"

# Rechercher "mairie", trié par surface
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/patrimoine/batiments/?search=mairie&ordering=-surface_m2"
```

---

#### Retrieve building details
```http
GET /api/patrimoine/batiments/{id}/
```

**Réponse** (200) - Détail complet:
```json
{
  "id_batiment": 1,
  "site": 1,
  "site_nom": "Mairie Ambert",
  "ville": "Ambert",
  "nom_batiment": "Mairie Ambert - Batiment 01",
  "code_patrimoine": "CALF-BAT-001",
  "surface_m2": "629.50",
  "annee_construction": 1987,
  "caracteristiques_tech": {
    "batiment": 1,
    "type_usage": "Administratif",
    "est_classe": false,
    "potentiel_photovoltaique": "Moyen",
    "zone_dangereuse": "Aucune",
    "reseau_chaleur": false,
    "etiquette_energetique": "C",
    "architecte": "Jean Dupont",
    "derniere_renovation_date": "2018-06-15"
  },
  "services_occupants": [
    {
      "service_id": 1,
      "service_nom": "Ressources Humaines",
      "pourcentage_occupation": "60.00"
    },
    {
      "service_id": 2,
      "service_nom": "Finances et Commande Publique",
      "pourcentage_occupation": "40.00"
    }
  ],
  "compteurs": [
    {
      "id_compteur": 1,
      "reference_fournisseur": "CPT-10001",
      "type_fluide": "Eau"
    },
    {
      "id_compteur": 2,
      "reference_fournisseur": "CPT-10002",
      "type_fluide": "Électricité"
    }
  ],
  "derniers_travaux": [
    {
      "id_travaux": 1,
      "titre_travaux": "Travaux 1 - Route",
      "statut": "Suspendu",
      "date_demande": "2025-10-20",
      "date_fin_previsionnelle": "2025-12-10",
      "date_fin_reelle": null
    }
  ]
}
```

**Exemple cURL**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/patrimoine/batiments/1/
```

---

### 3. STATISTIQUES

#### Get patrimoine statistics
```http
GET /api/patrimoine/stats/
```

**Authentification**: Pas requise (AllowAny)

**Réponse** (200):
```json
{
  "total_batiments": 20,
  "total_sites": 5,
  "total_surface_m2": 15423.5,
  "batiments_par_type_usage": {
    "Administratif": 4,
    "Scolaire": 3,
    "Culturel": 2,
    "Sportif": 4,
    "Technique": 3,
    "Mixte": 4
  },
  "batiments_par_ville": {
    "Ambert": 20
  }
}
```

**Exemple cURL**:
```bash
# Pas d'authentification requise
curl http://localhost:8000/api/patrimoine/stats/
```

---

## 🔑 Authentification

### Obtenir un token JWT
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Réponse** (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Utiliser le token
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/patrimoine/sites/
```

---

## 📊 Cas d'usage

### 1. Afficher tous les bâtiments d'un site
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/patrimoine/sites/1/"
```

### 2. Chercher des bâtiments administratifs
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/patrimoine/batiments/?type_usage=Administratif&ordering=-surface_m2"
```

### 3. Obtenir les stats globales
```bash
curl http://localhost:8000/api/patrimoine/stats/ | python -m json.tool
```

### 4. Chercher par ville
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/patrimoine/batiments/?ville=Ambert"
```

### 5. Fiche technique complète d'un bâtiment
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/patrimoine/batiments/1/" | python -m json.tool
```

---

## 🔐 Permissions

### Rôles utilisateurs
| Rôle | Lecture | Écriture | Admin |
|------|---------|----------|-------|
| `lecteur` | ✅ | ❌ | ❌ |
| `editeur` | ✅ | ❌ | ❌ |
| `admin` | ✅ | ✅ | ✅ |
| `super_admin` | ✅ | ✅ | ✅ |

### Test d'authentification utilisateurs
```bash
# Admin user
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  http://localhost:8000/api/auth/login/

# Lecteur user
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"lecteur","password":"lect123"}' \
  http://localhost:8000/api/auth/login/
```

---

## 📋 Structures de données

### Site
```json
{
  "id_site": 1,
  "nom_site": "string",
  "adresse": "string",
  "ville": "string",
  "nombre_batiments": 0,
  "batiments": []
}
```

### Bâtiment (List)
```json
{
  "id_batiment": 1,
  "nom_batiment": "string",
  "code_patrimoine": "string",
  "surface_m2": "decimal",
  "site": 1,
  "site_nom": "string",
  "ville": "string",
  "type_usage": "string"
}
```

### Bâtiment (Detail)
```json
{
  "id_batiment": 1,
  "site": 1,
  "site_nom": "string",
  "ville": "string",
  "nom_batiment": "string",
  "code_patrimoine": "string",
  "surface_m2": "decimal",
  "annee_construction": 1987,
  "caracteristiques_tech": {},
  "services_occupants": [],
  "compteurs": [],
  "derniers_travaux": []
}
```

---

## 🧪 Tests rapides

### Avec Postman
1. Obtenir un token via `POST /api/auth/login/`
2. Ajouter le header `Authorization: Bearer {token}`
3. Tester les endpoints

### Avec curl
```bash
# Variables
API_BASE="http://localhost:8000/api/patrimoine"

# 1. Stats (pas d'auth requise)
curl $API_BASE/stats/

# 2. Login
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  http://localhost:8000/api/auth/login/ | jq -r '.access')

# 3. Liste des sites
curl -H "Authorization: Bearer $TOKEN" $API_BASE/sites/

# 4. Liste des bâtiments
curl -H "Authorization: Bearer $TOKEN" $API_BASE/batiments/

# 5. Détail d'un bâtiment
curl -H "Authorization: Bearer $TOKEN" $API_BASE/batiments/1/
```

---

## ✨ Fonctionnalités implémentées

✅ **SiteViewSet**
- List avec annotation `nombre_batiments`
- Retrieve avec bâtiments imbriqués
- Filtre par ville
- Recherche par nom

✅ **BatimentViewSet**
- List et Retrieve avec sérializers adaptés
- Filtres: site, type_usage, ville
- Recherche par nom/code
- Tri flexible

✅ **Sérializers**
- `BatimentListSerializer` (champs légers)
- `BatimentDetailSerializer` (données complètes + nested)
- `BatimentCaracteristiquesSerializer`
- Serializers imbriqués pour services, compteurs, travaux

✅ **Endpoint Stats**
- Totaux globaux
- Distribution par type d'usage
- Distribution par ville

✅ **Permissions**
- Lecture: `IsAuthenticated`
- Écriture: `IsAdminUser`
- Stats: `AllowAny`

---

## 🚀 Lancer le serveur

```bash
# Depuis le répertoire backend/
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate.ps1  # Windows PowerShell

python manage.py runserver 8000
```

L'API sera disponible à: `http://localhost:8000/api/patrimoine/`
