# 👥 GestiBat - API Utilisateurs & Rôles

## 📋 Vue d'ensemble

L'API Utilisateurs fournit des endpoints pour:
- ✅ Gestion des agents (list, filter, detail)
- ✅ Profil utilisateur connecté
- ✅ Changement de rôle (super_admin only)
- ✅ Historique d'audit (AuditLog)
- ✅ Permissions granulaires par rôle

---

## 🔐 Système de rôles

### Hiérarchie des rôles

| Rôle | Lecture | Créer | Modifier | Supprimer | Admin | Changer rôles |
|------|---------|-------|----------|-----------|-------|---------------|
| **super_admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **editeur** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **lecteur** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Permissions par action

| Action | super_admin | admin | editeur | lecteur |
|--------|-------------|-------|---------|---------|
| GET /agents/ | ✅ | ✅ | ✅ | ✅ |
| GET /agents/{id}/ | ✅ | ✅ | ✅ | ✅ |
| POST /agents/ | ✅ | ✅ | ✅ | ❌ |
| PUT /agents/{id}/ | ✅ | ✅ | ✅ | ❌ |
| DELETE /agents/{id}/ | ✅ | ✅ | ❌ | ❌ |
| GET /me/ | ✅ | ✅ | ✅ | ✅ |
| POST /change-role/ | ✅ | ❌ | ❌ | ❌ |
| GET /audit-logs/ | ✅ | ✅ | ✅ | ✅ |

---

## 🔑 API Endpoints

### 1. AgentViewSet - `/api/users/agents/`

#### List agents avec filters et recherche
```
GET /api/users/agents/
```

**Paramètres query**:
- `search=nom` - Recherche par nom_complet ou email
- `statut=Titulaire` - Filtre par statut
- `ordering=nom_complet` - Tri

**Exemple**:
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/api/users/agents/?search=jean&statut=Titulaire&ordering=nom_complet"
```

**Réponse (200)**:
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id_agent": 1,
      "nom_complet": "Jean Dupont",
      "email": "jean.dupont@example.com",
      "statut": "Titulaire"
    }
  ]
}
```

#### Détail agent avec services
```
GET /api/users/agents/{id_agent}/
```

**Exemple**:
```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/users/agents/1/
```

**Réponse (200)**:
```json
{
  "id_agent": 1,
  "nom_complet": "Jean Dupont",
  "email": "jean.dupont@example.com",
  "statut": "Titulaire",
  "user_id": 5,
  "user_role": "editeur",
  "agent_services": [
    {
      "service_detail": {
        "id_service": 2,
        "nom_service": "Service Bâtiment",
        "pole_nom": "Pôle Bâtiments"
      },
      "role_dans_service": "Responsable"
    }
  ]
}
```

#### Créer un agent (admin+)
```
POST /api/users/agents/
```

**Body**:
```json
{
  "nom_complet": "Marie Martin",
  "email": "marie.martin@example.com",
  "statut": "Titulaire"
}
```

**Réponse (201)**:
```json
{
  "id_agent": 16,
  "nom_complet": "Marie Martin",
  "email": "marie.martin@example.com",
  "statut": "Titulaire"
}
```

#### Modifier un agent (admin+)
```
PUT /api/users/agents/{id_agent}/
```

**Body**:
```json
{
  "nom_complet": "Marie Martin Updated",
  "statut": "Remplaçant"
}
```

#### Supprimer un agent (admin only)
```
DELETE /api/users/agents/{id_agent}/
```

**Réponse (204)**: No content

---

### 2. User Profile - `/api/users/me/`

#### Obtenir son profil
```
GET /api/users/me/
```

**Authentification**: Requise (tous les rôles)

**Exemple**:
```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/users/me/
```

**Réponse (200)**:
```json
{
  "id": 5,
  "username": "jean.dupont",
  "email": "jean.dupont@example.com",
  "nom_complet": "Jean Dupont",
  "role": "editeur",
  "agent": {
    "id_agent": 1,
    "nom_complet": "Jean Dupont",
    "email": "jean.dupont@example.com",
    "statut": "Titulaire",
    "user_id": 5,
    "user_role": "editeur",
    "agent_services": [
      {
        "service_detail": {
          "id_service": 2,
          "nom_service": "Service Bâtiment",
          "pole_nom": "Pôle Bâtiments"
        },
        "role_dans_service": "Responsable"
      }
    ]
  }
}
```

---

### 3. Change Role - `/api/users/change-role/`

#### Changer le rôle d'un utilisateur (super_admin only)
```
POST /api/users/change-role/
```

**Authentification**: super_admin uniquement

**Body**:
```json
{
  "user_id": 6,
  "new_role": "admin"
}
```

**Valeurs acceptées pour new_role**:
- `super_admin`
- `admin`
- `editeur`
- `lecteur`

**Exemple cURL**:
```bash
curl -X POST \
  -H "Authorization: Bearer SUPER_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 6, "new_role": "admin"}' \
  http://localhost:8000/api/users/change-role/
```

**Réponse (200)**:
```json
{
  "detail": "Rôle de jean.dupont changé à admin",
  "user_id": 6,
  "old_role": "editeur",
  "new_role": "admin"
}
```

**Erreurs**:
- **400**: `{"user_id": ["L'utilisateur n'existe pas."]}`
- **403**: Non autorisé (seul super_admin)
- **404**: Utilisateur non trouvé

---

### 4. AuditLog - `/api/users/audit-logs/`

#### Lister les logs d'audit
```
GET /api/users/audit-logs/
```

**Authentification**: Requise

**Paramètres query**:
- `action=CREATE` - Filtre par action (CREATE, UPDATE, DELETE)
- `model_name=Batiment` - Filtre par modèle
- `user=5` - Filtre par utilisateur
- `ordering=-timestamp` - Tri (par défaut: -timestamp)

**Exemple**:
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/api/users/audit-logs/?action=UPDATE&model_name=Travaux&ordering=-timestamp"
```

**Réponse (200)**:
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/users/audit-logs/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user_id": 5,
      "user_username": "jean.dupont",
      "action": "CREATE",
      "model_name": "Batiment",
      "object_id": "7",
      "object_display": "Mairie de Ambert",
      "description": "Créé via API par jean.dupont",
      "timestamp": "2026-06-04T14:32:10Z"
    },
    {
      "id": 2,
      "user_id": 6,
      "user_username": "marie.martin",
      "action": "UPDATE",
      "model_name": "Travaux",
      "object_id": "15",
      "object_display": "Réparation toiture",
      "description": "Modifié: statut, priorite",
      "timestamp": "2026-06-04T14:31:45Z"
    }
  ]
}
```

#### Activité récente (pour le dashboard)
```
GET /api/users/audit-logs/recent_activity/
```

**Authentification**: Requise

**Réponse (200)**: Les 10 derniers logs

```json
[
  {
    "id": 1,
    "user_id": 5,
    "user_username": "jean.dupont",
    "action": "CREATE",
    "model_name": "Batiment",
    "object_id": "7",
    "object_display": "Mairie de Ambert",
    "description": "Créé via API par jean.dupont",
    "timestamp": "2026-06-04T14:32:10Z"
  }
]
```

#### Détail d'un log
```
GET /api/users/audit-logs/{id}/
```

**Exemple**:
```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/users/audit-logs/1/
```

---

## 📊 Model AuditLog

### Champs

| Champ | Type | Description |
|-------|------|-------------|
| `id` | Integer | ID unique |
| `user` | ForeignKey | L'utilisateur qui a fait l'action |
| `action` | CharField | CREATE, UPDATE, DELETE, READ, LOGIN |
| `model_name` | CharField | Nom du modèle (ex: "Batiment", "Travaux") |
| `object_id` | CharField | ID de l'objet modifié |
| `object_display` | CharField | Représentation lisible de l'objet |
| `description` | TextField | Description détaillée |
| `timestamp` | DateTimeField | Date/heure de l'action |

### Actions enregistrées

- **CREATE**: Création d'un nouvel objet
- **UPDATE**: Modification d'un objet
- **DELETE**: Suppression d'un objet
- **READ**: Lecture (lecture seule pour certains endpoints sensibles)
- **LOGIN**: Connexion utilisateur

---

## 🛠️ Utilisation pratique

### Cas d'usage 1: Vérifier mon profil
```bash
TOKEN="votre_token_ici"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/users/me/ | jq
```

### Cas d'usage 2: Lister les agents du service Bâtiment
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/users/agents/?search=bâtiment" | jq '.results'
```

### Cas d'usage 3: Voir l'historique des modifications
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/users/audit-logs/?action=UPDATE&ordering=-timestamp" | jq '.results[:5]'
```

### Cas d'usage 4: Promouvoir un utilisateur (super_admin)
```bash
SUPER_TOKEN="super_admin_token"
curl -X POST \
  -H "Authorization: Bearer $SUPER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 6, "new_role": "admin"}' \
  http://localhost:8000/api/users/change-role/ | jq
```

### Cas d'usage 5: Créer un nouvel agent (admin+)
```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nom_complet": "Nouveau Agent",
    "email": "nouveau@example.com",
    "statut": "Titulaire"
  }' \
  http://localhost:8000/api/users/agents/ | jq
```

---

## 📈 Audit Logging Automatique

### Comment ça marche

Chaque action POST/PUT/DELETE sur les modèles principaux crée automatiquement un log dans la table `AuditLog`:

1. **POST** (Création) → `action="CREATE"`
2. **PUT/PATCH** (Modification) → `action="UPDATE"`
3. **DELETE** (Suppression) → `action="DELETE"`

### Exemple de flux

```
1. Admin crée un bâtiment
   POST /api/patrimoine/batiments/
   → AuditLog crée avec action="CREATE"

2. Editeur modifie le travaux
   PUT /api/travaux/travaux/5/
   → AuditLog crée avec action="UPDATE"

3. Admin supprime un investissement
   DELETE /api/travaux/investissements/3/
   → AuditLog crée avec action="DELETE"

4. Dashboard affiche l'activité
   GET /api/users/audit-logs/recent_activity/
   → Retourne les 10 derniers logs
```

---

## 🔒 Sécurité

### Authentification
- ✅ JWT Token requis (sauf login/logout)
- ✅ Token expiration: par défaut 1 jour (configurable)

### Autorisation
- ✅ Permissions granulaires par rôle
- ✅ Les utilisateurs ne peuvent voir que les données publiques
- ✅ Les super_admin peuvent tout faire

### Protection

- ✅ Aucun utilisateur ne peut voir les mots de passe
- ✅ Aucun utilisateur ne peut modifier le rôle d'un autre (sauf super_admin)
- ✅ Tous les changements sont loggés dans AuditLog

---

## 💡 Tips & Tricks

### 1. Obtenir un token
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"identifiant":"admin","password":"admin123"}' \
  http://localhost:8000/api/auth/login/ | jq '.access'
```

### 2. Utiliser jq pour formater JSON
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/users/me/ | jq '.agent.agent_services'
```

### 3. Piper TOKEN dans curl
```bash
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"identifiant":"admin","password":"admin123"}' \
  http://localhost:8000/api/auth/login/ | jq -r '.access')

curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/users/me/ | jq
```

---

## 🚨 Erreurs courantes

### 401 Unauthorized
```json
{"detail": "Les credentials d'authentification n'ont pas été fourni(e)s."}
```
→ Manque le header `Authorization: Bearer TOKEN`

### 403 Forbidden
```json
{"detail": "Vous n'avez pas la permission d'accéder à cette ressource."}
```
→ Rôle insuffisant pour cette action

### 404 Not Found
```json
{"detail": "Non trouvé."}
```
→ L'objet (agent, utilisateur) n'existe pas

### 400 Bad Request
```json
{"user_id": ["L'utilisateur n'existe pas."]}
```
→ Données invalides dans le body

---

## 📚 Statuts HTTP

| Code | Signification |
|------|---------------|
| 200 | OK - Succès |
| 201 | Created - Création réussie |
| 204 | No Content - Suppression réussie |
| 400 | Bad Request - Données invalides |
| 401 | Unauthorized - Non authentifié |
| 403 | Forbidden - Non autorisé |
| 404 | Not Found - Ressource non trouvée |
| 500 | Internal Error - Erreur serveur |

---

## 🔄 Intégration avec le Dashboard

Le Dashboard utilise:

```json
GET /api/users/audit-logs/recent_activity/
```

Pour afficher "Activité récente":
```python
{
  "activite_recente": [
    {
      "auteur": "jean.dupont",
      "action": "CREATE",
      "timestamp": "2026-06-04T14:32:10Z",
      ...
    }
  ]
}
```

---

**Version**: 1.0  
**Date**: 2026-06-04  
**Status**: ✅ Documentation complète
