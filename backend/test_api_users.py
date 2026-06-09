"""
Tests pour l'API Utilisateurs & Rôles
Teste les endpoints de gestion des utilisateurs et audit logging
"""

import json
import requests
from time import sleep

BASE_URL = "http://localhost:8000"

# Utilisateurs de test
CREDENTIALS = {
    "admin": {"identifiant": "admin", "password": "admin123"},
    "editeur": {"identifiant": "editeur", "password": "edit123"},
    "lecteur": {"identifiant": "lecteur", "password": "lect123"},
    "superadmin": {"identifiant": "superadmin", "password": "super123"},
}


class GestiBatAPIClient:
    def __init__(self):
        self.tokens = {}
        self.session = requests.Session()
    
    def login(self, user_type="admin"):
        """Connexion et récupération du token"""
        creds = CREDENTIALS.get(user_type, CREDENTIALS["admin"])
        response = self.session.post(
            f"{BASE_URL}/api/auth/login/",
            json=creds
        )
        if response.status_code == 200:
            data = response.json()
            self.tokens[user_type] = data.get("access")
            print(f"✅ Connexion {user_type}: OK")
            return True
        print(f"❌ Connexion {user_type}: FAILED")
        return False
    
    def get_headers(self, user_type="admin"):
        """Retourne les headers avec le token"""
        token = self.tokens.get(user_type)
        return {"Authorization": f"Bearer {token}"} if token else {}
    
    def test_user_profile(self, user_type="admin"):
        """Test GET /api/users/me/"""
        headers = self.get_headers(user_type)
        response = self.session.get(f"{BASE_URL}/api/users/me/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Test {user_type} Profil: {data['username']} ({data['role']})")
            return True
        print(f"❌ Test {user_type} Profil: FAILED")
        return False
    
    def test_list_agents(self, user_type="admin"):
        """Test GET /api/users/agents/"""
        headers = self.get_headers(user_type)
        response = self.session.get(f"{BASE_URL}/api/users/agents/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Gérer les deux formats: pagination (dict) ou liste directe
            if isinstance(data, dict):
                count = data.get("count", len(data.get("results", [])))
            else:
                count = len(data)
            print(f"✅ Test List Agents: {count} agents trouvés")
            return True
        print(f"❌ Test List Agents: FAILED")
        return False
    
    def test_filter_agents_by_status(self):
        """Test GET /api/users/agents/?statut=Titulaire"""
        headers = self.get_headers("admin")
        response = self.session.get(
            f"{BASE_URL}/api/users/agents/?statut=Titulaire",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            print(f"✅ Test Filter Agents: {len(results)} agents Titulaire trouvés")
            return True
        print(f"❌ Test Filter Agents: FAILED")
        return False
    
    def test_search_agents(self):
        """Test GET /api/users/agents/?search=name"""
        headers = self.get_headers("admin")
        response = self.session.get(
            f"{BASE_URL}/api/users/agents/?search=jean",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            print(f"✅ Test Search Agents: {len(results)} agents trouvés")
            return True
        print(f"❌ Test Search Agents: FAILED")
        return False
    
    def test_agent_detail(self):
        """Test GET /api/users/agents/{id}/"""
        headers = self.get_headers("admin")
        # D'abord récupérer un agent
        response = self.session.get(f"{BASE_URL}/api/users/agents/", headers=headers)
        if response.status_code == 200:
            agents = response.json().get("results", [])
            if agents:
                agent_id = agents[0]["id_agent"]
                response = self.session.get(
                    f"{BASE_URL}/api/users/agents/{agent_id}/",
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Test Agent Detail: {data['nom_complet']}")
                    return True
        print(f"❌ Test Agent Detail: FAILED")
        return False
    
    def test_create_agent(self):
        """Test POST /api/users/agents/"""
        headers = self.get_headers("admin")
        new_agent = {
            "nom_complet": "Test Agent API",
            "email": f"test_api_{int(sleep(0))}@example.com",
            "statut": "Titulaire"
        }
        response = self.session.post(
            f"{BASE_URL}/api/users/agents/",
            headers=headers,
            json=new_agent
        )
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"✅ Test Create Agent: {data['nom_complet']} créé (ID: {data.get('id_agent')})")
            return True
        print(f"❌ Test Create Agent: FAILED")
        return False
    
    def test_audit_logs_list(self):
        """Test GET /api/users/audit-logs/"""
        headers = self.get_headers("admin")
        response = self.session.get(f"{BASE_URL}/api/users/audit-logs/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            count = data.get("count", 0)
            print(f"✅ Test Audit Logs: {count} logs trouvés")
            return True
        print(f"❌ Test Audit Logs: FAILED")
        return False
    
    def test_audit_logs_filter(self):
        """Test GET /api/users/audit-logs/?action=CREATE"""
        headers = self.get_headers("admin")
        response = self.session.get(
            f"{BASE_URL}/api/users/audit-logs/?action=CREATE",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            print(f"✅ Test Audit Logs Filter: {len(results)} CREATE logs trouvés")
            return True
        print(f"❌ Test Audit Logs Filter: FAILED")
        return False
    
    def test_audit_recent_activity(self):
        """Test GET /api/users/audit-logs/recent_activity/"""
        headers = self.get_headers("admin")
        response = self.session.get(
            f"{BASE_URL}/api/users/audit-logs/recent_activity/",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Test Recent Activity: {len(data)} logs (max 10)")
            return True
        print(f"❌ Test Recent Activity: FAILED")
        return False
    
    def test_permission_denied(self):
        """Test que lecteur ne peut pas créer"""
        headers = self.get_headers("lecteur")
        new_agent = {
            "nom_complet": "Should Fail",
            "email": "fail@example.com",
            "statut": "Titulaire"
        }
        response = self.session.post(
            f"{BASE_URL}/api/users/agents/",
            headers=headers,
            json=new_agent
        )
        if response.status_code == 403:
            print(f"✅ Test Permission Denied: lecteur ne peut pas créer (403)")
            return True
        print(f"❌ Test Permission Denied: Expected 403, got {response.status_code}")
        return False


def main():
    print("=" * 60)
    print("🧪 TESTS API UTILISATEURS & RÔLES")
    print("=" * 60)
    
    client = GestiBatAPIClient()
    
    # Test 1: Login tous les utilisateurs
    print("\n📝 Test 1: Connexion utilisateurs")
    for user in ["admin", "editeur", "lecteur", "superadmin"]:
        client.login(user)
    
    # Test 2: Profil utilisateur
    print("\n📝 Test 2: Profil utilisateur (/api/users/me/)")
    client.test_user_profile("admin")
    client.test_user_profile("editeur")
    client.test_user_profile("lecteur")
    
    # Test 3: List agents
    print("\n📝 Test 3: Lister les agents (/api/users/agents/)")
    client.test_list_agents("admin")
    
    # Test 4: Filter agents
    print("\n📝 Test 4: Filtrer les agents (/api/users/agents/?statut=...)")
    client.test_filter_agents_by_status()
    
    # Test 5: Search agents
    print("\n📝 Test 5: Rechercher les agents (/api/users/agents/?search=...)")
    client.test_search_agents()
    
    # Test 6: Detail agent
    print("\n📝 Test 6: Détail d'un agent (/api/users/agents/{id}/)")
    client.test_agent_detail()
    
    # Test 7: Create agent
    print("\n📝 Test 7: Créer un agent (POST /api/users/agents/)")
    client.test_create_agent()
    
    # Test 8: Audit logs list
    print("\n📝 Test 8: Lister les logs d'audit (/api/users/audit-logs/)")
    client.test_audit_logs_list()
    
    # Test 9: Audit logs filter
    print("\n📝 Test 9: Filtrer les logs d'audit (/api/users/audit-logs/?action=...)")
    client.test_audit_logs_filter()
    
    # Test 10: Recent activity
    print("\n📝 Test 10: Activité récente (/api/users/audit-logs/recent_activity/)")
    client.test_audit_recent_activity()
    
    # Test 11: Permission denied
    print("\n📝 Test 11: Vérifier les permissions")
    client.test_permission_denied()
    
    print("\n" + "=" * 60)
    print("✅ TOUS LES TESTS COMPLÉTÉS")
    print("=" * 60)


if __name__ == "__main__":
    main()
