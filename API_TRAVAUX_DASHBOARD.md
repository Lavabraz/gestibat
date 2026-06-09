# 📊 API REST Travaux & Dashboard - GestiBat

## 🚀 Vue d'ensemble

API complète pour la gestion des travaux et investissements avec endpoint dashboard centralisant les KPIs.

### Configuration
- **Base URL**: `http://localhost:8000/api/travaux/`
- **Dashboard**: `http://localhost:8000/api/dashboard/`
- **Format**: JSON
- **Authentification**: JWT Token (obligatoire sauf stats)
- **Permissions**:
  - **Lecture (GET)**: `IsAuthenticated`
  - **Écriture (POST/PUT/DELETE)**: `IsAdminUser`

---

## 📍 Endpoints

### 1. TRAVAUX

#### List all travaux
```http
GET /api/travaux/travaux/
```

**Paramètres de requête**:
- `statut`: Filtrer par statut (ex: `?statut=En cours` ou `?statut=EnCours`)
- `batiment`: ID du bâtiment (ex: `?batiment=5`)
- `domaine_metier`: Domaine métier (ex: `?domaine_metier=Bâtiment`)

**Réponse** (200):
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "titre_travaux": "Travaux 1 - Route",
      "statut": "Suspendu",
      "priorite": "Basse",
      "batiment_nom": "Mairie Ambert - Batiment 01",
      "date_demande": "2025-10-20",
      "date_fin_previsionnelle": "2025-12-10",
      "type_travaux": "Entretien"
    },
    {
      "id": 2,
      "titre_travaux": "Travaux 2 - Rouge",
      "statut": "Validé",
      "priorite": "Moyenne",
      "batiment_nom": "Centre Culturel - Batiment 02",
      "date_demande": "2025-11-01",
      "date_fin_previsionnelle": null,
      "type_travaux": "Amélioration"
    }
  ]
}
```

**Exemples cURL**:
```bash
# Tous les travaux
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/travaux/travaux/

# Travaux en cours
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/travaux/travaux/?statut=En%20cours"

# Travaux du bâtiment 5
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/travaux/travaux/?batiment=5"

# Travaux domaine Bâtiment
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/travaux/travaux/?domaine_metier=Bâtiment"
```

---

#### Retrieve travaux details
```http
GET /api/travaux/travaux/{id}/
```

**Réponse** (200) - Détail complet:
```json
{
  "id_travaux": 1,
  "batiment": 1,
  "batiment_nom": "Mairie Ambert - Batiment 01",
  "service_demandeur": 1,
  "investissement": null,
  "investissement_detail": null,
  "domaine_metier": "Bâtiment",
  "titre_travaux": "Travaux 1 - Route",
  "type_travaux": "Entretien",
  "priorite": "Basse",
  "date_demande": "2025-10-20",
  "date_fin_previsionnelle": "2025-12-10",
  "date_fin_reelle": null,
  "responsable_interne": 1,
  "intervenant_externe": "Entreprise XYZ",
  "statut": "Suspendu"
}
```

Si un investissement est associé:
```json
{
  "investissement_detail": {
    "id_investissement": 1,
    "batiment": 1,
    "batiment_nom": "Mairie Ambert - Batiment 01",
    "service_pilote": 1,
    "service_pilote_nom": "Patrimoine Bati",
    "titre_projet": "Programme Corps 1",
    "type_investissement": "Rehabilitation",
    "annee_programmation": 2025,
    "budget_estime": "250000.00",
    "cout_reel": null,
    "statut": "Engagé",
    "priorite_strategique": "Strategique"
  }
}
```

**Exemple cURL**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/travaux/travaux/1/
```

---

#### Create travaux
```http
POST /api/travaux/travaux/
```

**Body**:
```json
{
  "batiment": 1,
  "service_demandeur": 1,
  "domaine_metier": "Bâtiment",
  "titre_travaux": "Nouveau travail",
  "type_travaux": "Entretien",
  "priorite": "Moyenne",
  "date_demande": "2026-06-04",
  "date_fin_previsionnelle": "2026-07-04",
  "statut": "Proposé"
}
```

---

#### Update travaux
```http
PUT /api/travaux/travaux/{id}/
```

**Body**: Voir Create (tous les champs)

---

#### Delete travaux
```http
DELETE /api/travaux/travaux/{id}/
```

**Réponse**: 204 No Content

---

#### Action personnalisée: Clôturer travaux
```http
POST /api/travaux/travaux/{id}/cloturer/
```

**Effet**:
- Passe `statut` à `"Terminé"`
- Renseigne `date_fin_reelle` = aujourd'hui

**Réponse** (200):
```json
{
  "id_travaux": 1,
  "titre_travaux": "Travaux 1 - Route",
  "statut": "Terminé",
  "date_fin_reelle": "2026-06-04",
  ...
}
```

**Exemple cURL**:
```bash
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/travaux/travaux/1/cloturer/
```

---

### 2. INVESTISSEMENTS

#### List all investissements
```http
GET /api/travaux/investissements/
```

**Paramètres de requête**:
- `statut`: Filtrer par statut (ex: `?statut=Validé`)
- `annee_programmation`: Filtrer par année (ex: `?annee_programmation=2026`)

**Réponse** (200):
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id_investissement": 1,
      "batiment": 1,
      "batiment_nom": "Mairie Ambert - Batiment 01",
      "service_pilote": 1,
      "service_pilote_nom": "Patrimoine Bati",
      "titre_projet": "Programme Corps 1",
      "type_investissement": "Rehabilitation",
      "annee_programmation": 2025,
      "budget_estime": "250000.00",
      "cout_reel": null,
      "statut": "Engagé",
      "priorite_strategique": "Strategique"
    }
  ]
}
```

**Exemples cURL**:
```bash
# Tous les investissements
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/travaux/investissements/

# Investissements validés
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/travaux/investissements/?statut=Validé"

# Investissements 2026
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/travaux/investissements/?annee_programmation=2026"
```

---

#### Retrieve investissement details
```http
GET /api/travaux/investissements/{id}/
```

---

#### Create investissement
```http
POST /api/travaux/investissements/
```

**Body**:
```json
{
  "batiment": 1,
  "service_pilote": 1,
  "titre_projet": "Nouveau projet",
  "type_investissement": "Renovation energetique",
  "annee_programmation": 2026,
  "budget_estime": "150000.00",
  "statut": "Proposition",
  "priorite_strategique": "Haute"
}
```

---

#### Update investissement
```http
PUT /api/travaux/investissements/{id}/
```

---

#### Delete investissement
```http
DELETE /api/travaux/investissements/{id}/
```

---

### 3. DASHBOARD

#### Get dashboard KPIs and alerts
```http
GET /api/dashboard/
```

**Authentification**: Requise (`IsAuthenticated`)

**Réponse** (200):
```json
{
  "kpis": {
    "total_batiments": 20,
    "total_agents_actifs": 11,
    "agents_remplacants": 3,
    "total_travaux_en_cours": 4,
    "total_investissements_valides": 2
  },
  "alertes": [
    {
      "type": "danger",
      "titre": "Travaux urgents sans date de fin",
      "detail": "2 travaux urgents n'ont pas de date de fin previsionnelle.",
      "date": "2026-06-04"
    },
    {
      "type": "warning",
      "titre": "Compteurs sans releve recent",
      "detail": "5 compteurs sans releve depuis plus de 30 jours.",
      "date": "2026-06-04"
    },
    {
      "type": "warning",
      "titre": "Investissements engages anciens",
      "detail": "1 investissements engages depuis plus d'un an sans cloture.",
      "date": "2026-06-04"
    }
  ],
  "activite_recente": [
    {
      "auteur": "Lucie Marie",
      "action": "Travaux 'Travaux 1 - Route' (Suspendu) sur Mairie Ambert - Batiment 01",
      "timestamp": "2025-10-20"
    },
    {
      "auteur": "Patrimoine Bati",
      "action": "Investissement 'Programme Corps 1' (Engagé)",
      "timestamp": "2025-01-01"
    }
  ]
}
```

**Exemple cURL**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/dashboard/
```

---

## 📊 Structure des données

### Travaux (List)
```json
{
  "id": 1,
  "titre_travaux": "string",
  "statut": "string",
  "priorite": "string",
  "batiment_nom": "string",
  "date_demande": "2026-06-04",
  "date_fin_previsionnelle": "2026-07-04",
  "type_travaux": "string"
}
```

### Travaux (Detail)
```json
{
  "id_travaux": 1,
  "batiment": 1,
  "batiment_nom": "string",
  "service_demandeur": 1,
  "investissement": 1,
  "investissement_detail": {},
  "domaine_metier": "string",
  "titre_travaux": "string",
  "type_travaux": "string",
  "priorite": "string",
  "date_demande": "2026-06-04",
  "date_fin_previsionnelle": "2026-07-04",
  "date_fin_reelle": null,
  "responsable_interne": 1,
  "intervenant_externe": "string",
  "statut": "string"
}
```

### Investissement
```json
{
  "id_investissement": 1,
  "batiment": 1,
  "batiment_nom": "string",
  "service_pilote": 1,
  "service_pilote_nom": "string",
  "titre_projet": "string",
  "type_investissement": "string",
  "annee_programmation": 2026,
  "budget_estime": "150000.00",
  "cout_reel": null,
  "statut": "string",
  "priorite_strategique": "string"
}
```

### Dashboard KPIs
```json
{
  "total_batiments": 20,
  "total_agents_actifs": 11,
  "agents_remplacants": 3,
  "total_travaux_en_cours": 4,
  "total_investissements_valides": 2
}
```

### Alerte
```json
{
  "type": "danger|warning|success",
  "titre": "string",
  "detail": "string",
  "date": "2026-06-04"
}
```

### Activité récente
```json
{
  "auteur": "string",
  "action": "string",
  "timestamp": "2026-06-04"
}
```

---

## 📋 Types de données

### Statuts Travaux
- `Proposé`
- `Validé`
- `En cours`
- `Planifié`
- `Terminé`
- `Suspendu`

### Types Travaux
- `Entretien`
- `Amélioration`
- `Urgence`

### Domaines Métier
- `Bâtiment`
- `Espaces Verts`
- `Voirie`
- `DSI`

### Statuts Investissements
- `Proposition`
- `Validé`
- `Engagé`
- `Terminé`

---

## 🧪 Cas d'usage

### 1. Lister les travaux urgents en cours
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/travaux/travaux/?statut=En%20cours&domaine_metier=Bâtiment"
```

### 2. Clôturer un travail
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/travaux/travaux/1/cloturer/
```

### 3. Créer un nouveau travail
```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "batiment": 1,
    "service_demandeur": 1,
    "domaine_metier": "Bâtiment",
    "titre_travaux": "Remplacement fenêtres",
    "type_travaux": "Amélioration",
    "priorite": "Moyenne",
    "date_demande": "2026-06-04",
    "statut": "Proposé"
  }' \
  http://localhost:8000/api/travaux/travaux/
```

### 4. Consulter le dashboard
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/dashboard/
```

### 5. Lister les investissements 2026
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/travaux/investissements/?annee_programmation=2026"
```

---

## ⚡ Alertes du Dashboard

### Types d'alertes générées automatiquement

#### 🔴 Danger (urgence)
- Travaux de type `URGENCE` sans `date_fin_previsionnelle`

#### ⚠️ Warning (attention)
- Compteurs sans relevé depuis plus de **30 jours**
- Investissements `ENGAGÉ` depuis plus de **1 an** (année_programmation ≤ année_actuelle - 1)

#### ✅ Success (OK)
- Affiché si aucune alerte d'attention ou urgence

---

## 🔐 Permissions

### Rôles utilisateurs
| Rôle | Lecture | Écriture | Clôturer | Action |
|------|---------|----------|----------|--------|
| `lecteur` | ✅ | ❌ | ❌ | N/A |
| `editeur` | ✅ | ❌ | ❌ | N/A |
| `admin` | ✅ | ✅ | ✅ | ✅ |
| `super_admin` | ✅ | ✅ | ✅ | ✅ |

---

## 📊 Dashboard vs Endpoints individuels

| Information | Dashboard | Endpoints |
|-------------|-----------|-----------|
| KPIs rapides | ✅ Une requête | ❌ Plusieurs requêtes |
| Alertes synthétiques | ✅ Aggrégées | ❌ Filtrer manuellement |
| Activité récente | ✅ Oui | ❌ Non |
| Détails complets | ❌ Non | ✅ Oui |
| Performance | ✅ Optimisé | ✅ Optimisé |

**Recommandation**: Utiliser le dashboard pour un aperçu rapide, puis les endpoints individuels pour les détails.

---

## 🚀 Tests

### Python
```bash
# Lancer le serveur
python manage.py runserver 8000

# Dans un autre terminal
python -c "
import requests
import json

# Login
r = requests.post('http://localhost:8000/api/auth/login/', 
  json={'username': 'admin', 'password': 'admin123'})
token = r.json()['access']
headers = {'Authorization': f'Bearer {token}'}

# Dashboard
dashboard = requests.get('http://localhost:8000/api/dashboard/', headers=headers).json()
print(json.dumps(dashboard, indent=2, ensure_ascii=False))

# Travaux
travaux = requests.get('http://localhost:8000/api/travaux/travaux/', headers=headers).json()
print(f'\\nTotal travaux: {travaux[\"count\"]}')

# Clôturer un travail
cloturer = requests.post('http://localhost:8000/api/travaux/travaux/1/cloturer/', 
  headers=headers).json()
print(f'Statut après clôture: {cloturer[\"statut\"]}')
"
```

### Postman
1. Importer la collection fournie
2. Définir le token via l'endpoint Login
3. Tester les endpoints

---

## ✨ Fonctionnalités implémentées

✅ TravauxViewSet
- CRUD complet
- Filtres par statut, bâtiment, domaine_métier
- Liste avec champs légers
- Détail avec investissement imbriqué
- Action `@action cloturer(pk)`

✅ InvestissementViewSet
- CRUD complet
- Filtres par statut et année
- Sérializer avec noms résolus

✅ DashboardAPIView
- 5 KPIs clés
- Alertes aggrégées automatiquement
  - Travaux urgents sans fin
  - Compteurs obsolètes (> 30j)
  - Investissements anciens (> 1 an)
- Activité récente (travaux + investissements)
- Performance optimisée

---

## 📝 Notes

- Les dates sont en format ISO 8601 (`YYYY-MM-DD`)
- Les montants sont en décimal (ex: `"150000.00"`)
- Les alertes sont triées par sévérité (danger > warning > success)
- L'activité récente est limitée à 10 entrées
- Les filtres sont case-insensitive
