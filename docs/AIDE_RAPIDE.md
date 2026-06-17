# ⚡ GestiBat - Aide rapide

## 🎯 Les 3 commandes essentielles

### 1. Démarrer
```bash
cd backend
python manage.py runserver 8000
```
✅ Serveur actif sur http://localhost:8000

### 2. Tester
```bash
cd backend
python test_api_travaux_dashboard.py
```
✅ 13 tests travaux/dashboard exécutés

### 3. Vérifier données
```bash
cd backend
python manage.py seed_data
```
✅ Base peuplée avec 95+ objets

---

## 📍 Endpoints clés (5 à retenir)

```
GET  /api/dashboard/                         Dashboard complet
GET  /api/patrimoine/batiments/              Bâtiments
GET  /api/travaux/travaux/                   Travaux
POST /api/travaux/travaux/{id}/cloturer/     Clôturer travaux
GET  /api/patrimoine/stats/                  Stats (no auth)
```

---

## 👥 Utilisateurs (credentials)

```
admin       / admin123       (write access)
lecteur     / lect123        (read only)
```

---

## 🧪 Tests rapides (cURL)

```bash
# Login
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  http://localhost:8000/api/auth/login/ | jq -r '.access')

# Dashboard
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/dashboard/ | jq

# Stats (no auth)
curl http://localhost:8000/api/patrimoine/stats/ | jq
```

---

## 📂 Fichiers de doc

| Fichier | Purpose |
|---------|---------|
| **QUICKSTART.md** | Démarrage 5 min |
| **INDEX.md** | Navigation |
| **API_COMPLETE.md** | Vue d'ensemble |
| **API_PATRIMOINE.md** | Patrimoine |
| **API_TRAVAUX_DASHBOARD.md** | Travaux |

---

## 🚨 Problèmes courants

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Database locked"
```bash
rm backend/db.sqlite3
python manage.py migrate
python manage.py seed_data
```

### "Connection refused"
```bash
# Vérifier serveur actif
python manage.py runserver 8000
```

---

## ✅ Checklist rapide

- [ ] Lire QUICKSTART.md
- [ ] Lancer serveur
- [ ] Exécuter tests
- [ ] Tester cURL/Postman
- [ ] Vérifier KPIs dashboard
- [ ] Vérifier alertes
- [ ] Créer travaux
- [ ] Clôturer travaux

---

## 🎉 C'est tout!

Besoin d'aide? Consultez [INDEX.md](INDEX.md)

---

**Dernier 11/09/2024**
