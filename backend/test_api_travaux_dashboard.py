#!/usr/bin/env python
"""
Script de test de l'API Travaux et Dashboard GestiBat
Démontre l'utilisation de tous les endpoints
"""

import requests
import json
from typing import Optional
from datetime import date

API_BASE = "http://localhost:8000/api"

class GestiBatAPIClient:
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()

    def login(self, username: str, password: str) -> bool:
        """Authentifier et obtenir un token JWT"""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login/",              
                json={"username": username, "password": password}
            )
            response.raise_for_status()
            self.token = response.json()["access"]
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            print(f"✅ Connecté en tant que {username}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion: {e}")
            return False

    def get_travaux(self, statut: Optional[str] = None,
                   batiment: Optional[int] = None,
                   domaine_metier: Optional[str] = None):
        """Récupérer tous les travaux avec filtres"""
        params = {}
        if statut:
            params["statut"] = statut
        if batiment:
            params["batiment"] = batiment
        if domaine_metier:
            params["domaine_metier"] = domaine_metier
        
        response = self.session.get(f"{self.base_url}/travaux/travaux/", params=params)
        return response.json()

    def get_travaux_detail(self, travaux_id: int):
        """Détail d'un travaux"""
        response = self.session.get(f"{self.base_url}/travaux/travaux/{travaux_id}/")
        return response.json()

    def create_travaux(self, batiment_id: int, service_id: int, titre: str,
                      domaine: str = "Bâtiment", type_travaux: str = "Entretien",
                      priorite: str = "Moyenne", statut: str = "Proposé"):
        """Créer un travaux"""
        data = {
            "batiment": batiment_id,
            "service_demandeur": service_id,
            "domaine_metier": domaine,
            "titre_travaux": titre,
            "type_travaux": type_travaux,
            "priorite": priorite,
            "date_demande": str(date.today()),
            "statut": statut
        }
        response = self.session.post(f"{self.base_url}/travaux/travaux/", json=data)
        return response.json()

    def cloturer_travaux(self, travaux_id: int):
        """Clôturer un travaux"""
        response = self.session.post(f"{self.base_url}/travaux/travaux/{travaux_id}/cloturer/")
        return response.json()

    def get_investissements(self, statut: Optional[str] = None,
                           annee: Optional[int] = None):
        """Récupérer tous les investissements"""
        params = {}
        if statut:
            params["statut"] = statut
        if annee:
            params["annee_programmation"] = annee
        
        response = self.session.get(f"{self.base_url}/travaux/investissements/", params=params)
        return response.json()

    def get_investissement_detail(self, inv_id: int):
        """Détail d'un investissement"""
        response = self.session.get(f"{self.base_url}/travaux/investissements/{inv_id}/")
        return response.json()

    def get_dashboard(self):
        """Récupérer le dashboard"""
        response = self.session.get(f"{self.base_url}/dashboard/")
        return response.json()


def print_header(title: str):
    """Afficher un titre formaté"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_json(data, max_depth=None):
    """Afficher du JSON formaté"""
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def main():
    client = GestiBatAPIClient()

    # Test 1: Connexion
    print_header("TEST 1: Connexion utilisateur")
    if not client.login("admin", "admin123"):
        print("❌ Impossible de se connecter, arrêt des tests")
        return

    # Test 2: Dashboard
    print_header("TEST 2: Dashboard - KPIs et Alertes")
    dashboard = client.get_dashboard()
    print("🎯 KPIs:")
    for key, value in dashboard['kpis'].items():
        print(f"  • {key}: {value}")
    
    print("\n🚨 Alertes:")
    for alerte in dashboard['alertes']:
        print(f"  [{alerte['type'].upper()}] {alerte['titre']}")
        print(f"    → {alerte['detail']}")
    
    print("\n📊 Activité récente:")
    for activity in dashboard['activite_recente'][:3]:
        print(f"  • {activity['auteur']}: {activity['action']}")

    # Test 3: Liste des travaux
    print_header("TEST 3: Liste tous les travaux")
    travaux_response = client.get_travaux()
    print(f"Nombre total de travaux: {travaux_response['count']}")
    print("\nPremiers travaux:")
    for travaux in travaux_response['results'][:3]:
        print(f"  • [{travaux['statut']}] {travaux['titre_travaux']} - {travaux['priorite']}")

    # Test 4: Filtre par statut
    print_header("TEST 4: Filtrer travaux par statut")
    encours = client.get_travaux(statut="En cours")
    print(f"Travaux 'En cours': {encours['count']}")
    for travaux in encours['results']:
        print(f"  • {travaux['titre_travaux']} ({travaux['batiment_nom']})")

    # Test 5: Filtre par bâtiment
    print_header("TEST 5: Travaux du bâtiment 1")
    bat_travaux = client.get_travaux(batiment=1)
    print(f"Nombre de travaux: {bat_travaux['count']}")
    for travaux in bat_travaux['results']:
        print(f"  • {travaux['titre_travaux']} ({travaux['statut']})")

    # Test 6: Filtre par domaine métier
    print_header("TEST 6: Travaux domaine 'Bâtiment'")
    bat_domain = client.get_travaux(domaine_metier="Bâtiment")
    print(f"Nombre de travaux: {bat_domain['count']}")
    for travaux in bat_domain['results'][:3]:
        print(f"  • {travaux['titre_travaux']}")

    # Test 7: Détail d'un travaux
    print_header("TEST 7: Détail d'un travaux")
    if travaux_response['results']:
        travaux_id = travaux_response['results'][0]['id']
        travaux_detail = client.get_travaux_detail(travaux_id)
        print(f"ID: {travaux_detail['id_travaux']}")
        print(f"Titre: {travaux_detail['titre_travaux']}")
        print(f"Statut: {travaux_detail['statut']}")
        print(f"Bâtiment: {travaux_detail['batiment_nom']}")
        print(f"Type: {travaux_detail['type_travaux']}")
        print(f"Priorité: {travaux_detail['priorite']}")
        print(f"Date demande: {travaux_detail['date_demande']}")
        if travaux_detail.get('investissement_detail'):
            print(f"\n📊 Investissement associé:")
            print(f"  Titre: {travaux_detail['investissement_detail']['titre_projet']}")
            print(f"  Budget: {travaux_detail['investissement_detail']['budget_estime']}€")

    # Test 8: Créer un travaux
    print_header("TEST 8: Créer un nouveau travaux")
    nouveau_travaux = client.create_travaux(
        batiment_id=1,
        service_id=1,
        titre="Test API - Maintenance préventive",
        domaine="Bâtiment",
        type_travaux="Entretien",
        priorite="Haute",
        statut="Proposé"
    )
    if 'id_travaux' in nouveau_travaux:
        print(f"✅ Travaux créé avec ID: {nouveau_travaux['id_travaux']}")
        new_id = nouveau_travaux['id_travaux']
    else:
        print(f"❌ Erreur: {nouveau_travaux}")
        new_id = None

    # Test 9: Clôturer un travaux (optionnel)
    print_header("TEST 9: Clôturer un travaux")
    if new_id:
        travaux_clos = client.cloturer_travaux(new_id)
        print(f"✅ Travaux clôturé")
        print(f"  Nouveau statut: {travaux_clos['statut']}")
        print(f"  Date de fin réelle: {travaux_clos.get('date_fin_reelle', 'N/A')}")
    else:
        print("⏭️  Pas de travaux créé à clôturer")

    # Test 10: Liste des investissements
    print_header("TEST 10: Liste des investissements")
    invest_response = client.get_investissements()
    print(f"Nombre total: {invest_response['count']}")
    print("\nPremiers investissements:")
    for inv in invest_response['results'][:3]:
        print(f"  • [{inv['statut']}] {inv['titre_projet']} ({inv['annee_programmation']})")
        print(f"    Budget: {inv['budget_estime']}€")

    # Test 11: Filtre investissements par statut
    print_header("TEST 11: Investissements 'Validé'")
    valides = client.get_investissements(statut="Validé")
    print(f"Nombre: {valides['count']}")
    for inv in valides['results']:
        print(f"  • {inv['titre_projet']}")

    # Test 12: Filtre investissements par année
    print_header("TEST 12: Investissements 2026")
    annee_2026 = client.get_investissements(annee=2026)
    print(f"Nombre: {annee_2026['count']}")
    for inv in annee_2026['results']:
        print(f"  • {inv['titre_projet']} - {inv['service_pilote_nom']}")

    # Test 13: Détail investissement
    print_header("TEST 13: Détail d'un investissement")
    if invest_response['results']:
        inv_id = invest_response['results'][0]['id_investissement']
        inv_detail = client.get_investissement_detail(inv_id)
        print(f"Titre: {inv_detail['titre_projet']}")
        print(f"Bâtiment: {inv_detail['batiment_nom']}")
        print(f"Service pilote: {inv_detail['service_pilote_nom']}")
        print(f"Statut: {inv_detail['statut']}")
        print(f"Budget estimé: {inv_detail['budget_estime']}€")
        print(f"Type: {inv_detail['type_investissement']}")
        print(f"Priorité: {inv_detail['priorite_strategique']}")

    print_header("TOUS LES TESTS COMPLÉTÉS ✅")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrompus")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
