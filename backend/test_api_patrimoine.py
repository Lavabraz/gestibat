#!/usr/bin/env python
"""
Script de test de l'API Patrimoine GestiBat
Démontre l'utilisation de tous les endpoints
"""

import requests
import json
from typing import Optional

API_BASE = "http://localhost:8000/api"
PATRIMOINE_API = f"{API_BASE}/patrimoine"

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

    def get_sites(self, ville: Optional[str] = None, search: Optional[str] = None):
        """Récupérer tous les sites"""
        params = {}
        if ville:
            params["ville"] = ville
        if search:
            params["search"] = search
        
        response = self.session.get(f"{PATRIMOINE_API}/sites/", params=params)
        return response.json()

    def get_site_detail(self, site_id: int):
        """Détail d'un site avec ses bâtiments"""
        response = self.session.get(f"{PATRIMOINE_API}/sites/{site_id}/")
        return response.json()

    def get_batiments(self, site_id: Optional[int] = None, 
                     type_usage: Optional[str] = None,
                     ville: Optional[str] = None,
                     search: Optional[str] = None,
                     ordering: Optional[str] = None):
        """Récupérer tous les bâtiments avec filtres"""
        params = {}
        if site_id:
            params["site"] = site_id
        if type_usage:
            params["type_usage"] = type_usage
        if ville:
            params["ville"] = ville
        if search:
            params["search"] = search
        if ordering:
            params["ordering"] = ordering
        
        response = self.session.get(f"{PATRIMOINE_API}/batiments/", params=params)
        return response.json()

    def get_batiment_detail(self, batiment_id: int):
        """Détail complet d'un bâtiment"""
        response = self.session.get(f"{PATRIMOINE_API}/batiments/{batiment_id}/")
        return response.json()

    def get_stats(self):
        """Statistiques du patrimoine (pas d'auth requise)"""
        response = requests.get(f"{PATRIMOINE_API}/stats/")
        return response.json()


def print_header(title: str):
    """Afficher un titre formaté"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def main():
    # Initialiser le client
    client = GestiBatAPIClient()

    # Test 1: Statistiques (pas d'authentification requise)
    print_header("TEST 1: Statistiques (AllowAny)")
    stats = client.get_stats()
    print(f"Total bâtiments: {stats['total_batiments']}")
    print(f"Total sites: {stats['total_sites']}")
    print(f"Total surface: {stats['total_surface_m2']} m²")
    print(f"Par type d'usage:")
    for usage, count in stats['batiments_par_type_usage'].items():
        print(f"  - {usage}: {count}")

    # Test 2: Connexion
    print_header("TEST 2: Connexion utilisateur")
    if not client.login("admin", "admin123"):
        print("❌ Impossible de se connecter, arrêt des tests")
        return

    # Test 3: Liste des sites
    print_header("TEST 3: Liste tous les sites")
    sites_response = client.get_sites()
    print(f"Nombre de sites: {sites_response['count']}")
    for site in sites_response['results'][:3]:
        print(f"  • {site['nom_site']} ({site['nombre_batiments']} bâtiments)")

    # Test 4: Filtre par ville
    print_header("TEST 4: Filtre par ville (Ambert)")
    ambert_sites = client.get_sites(ville="Ambert")
    print(f"Sites à Ambert: {ambert_sites['count']}")
    for site in ambert_sites['results']:
        print(f"  • {site['nom_site']}")

    # Test 5: Recherche de sites
    print_header("TEST 5: Recherche (piscine)")
    search_results = client.get_sites(search="piscine")
    print(f"Résultats: {search_results['count']}")
    for site in search_results['results']:
        print(f"  • {site['nom_site']} - {site['adresse']}")

    # Test 6: Détail d'un site
    print_header("TEST 6: Détail d'un site (ID=1)")
    site_detail = client.get_site_detail(1)
    print(f"Nom: {site_detail['nom_site']}")
    print(f"Adresse: {site_detail['adresse']}")
    print(f"Ville: {site_detail['ville']}")
    print(f"\nBâtiments du site:")
    for bat in site_detail['batiments']:
        print(f"  • {bat['nom_batiment']} ({bat['surface_m2']} m²)")

    # Test 7: Liste des bâtiments
    print_header("TEST 7: Liste tous les bâtiments")
    batiments_response = client.get_batiments()
    print(f"Nombre de bâtiments: {batiments_response['count']}")
    for bat in batiments_response['results'][:5]:
        print(f"  • {bat['code_patrimoine']}: {bat['nom_batiment']} ({bat['surface_m2']} m²)")

    # Test 8: Filtre par site
    print_header("TEST 8: Bâtiments du site 1")
    site1_batiments = client.get_batiments(site_id=1)
    print(f"Nombre de bâtiments: {site1_batiments['count']}")
    for bat in site1_batiments['results']:
        print(f"  • {bat['code_patrimoine']}: {bat['nom_batiment']}")

    # Test 9: Filtre par type d'usage
    print_header("TEST 9: Bâtiments administratifs")
    admin_batiments = client.get_batiments(type_usage="Administratif")
    print(f"Nombre de bâtiments administratifs: {admin_batiments['count']}")
    for bat in admin_batiments['results']:
        print(f"  • {bat['nom_batiment']}")

    # Test 10: Tri par surface (décroissant)
    print_header("TEST 10: Bâtiments triés par surface (décroissant)")
    sorted_batiments = client.get_batiments(ordering="-surface_m2")
    print("Top 5 plus grands bâtiments:")
    for bat in sorted_batiments['results'][:5]:
        print(f"  • {bat['nom_batiment']}: {bat['surface_m2']} m²")

    # Test 11: Recherche de bâtiments
    print_header("TEST 11: Recherche (mairie)")
    search_bat = client.get_batiments(search="mairie")
    print(f"Résultats trouvés: {search_bat['count']}")
    for bat in search_bat['results']:
        print(f"  • {bat['code_patrimoine']}: {bat['nom_batiment']}")

    # Test 12: Détail complet d'un bâtiment
    print_header("TEST 12: Détail complet d'un bâtiment (ID=1)")
    bat_detail = client.get_batiment_detail(1)
    print(f"Code: {bat_detail['code_patrimoine']}")
    print(f"Nom: {bat_detail['nom_batiment']}")
    print(f"Surface: {bat_detail['surface_m2']} m²")
    print(f"Année construction: {bat_detail['annee_construction']}")
    print(f"Ville: {bat_detail['ville']}")
    
    print(f"\nCaractéristiques techniques:")
    if bat_detail['caracteristiques_tech']:
        ct = bat_detail['caracteristiques_tech']
        print(f"  • Type d'usage: {ct['type_usage']}")
        print(f"  • Étiquette énergétique: {ct['etiquette_energetique']}")
        print(f"  • Potentiel PV: {ct['potentiel_photovoltaique']}")
    
    print(f"\nServices occupants:")
    for service in bat_detail['services_occupants']:
        print(f"  • {service['service_nom']}: {service['pourcentage_occupation']}%")
    
    print(f"\nCompteurs:")
    for compteur in bat_detail['compteurs']:
        print(f"  • {compteur['reference_fournisseur']} ({compteur['type_fluide']})")
    
    print(f"\nDerniers travaux:")
    if bat_detail['derniers_travaux']:
        for travail in bat_detail['derniers_travaux']:
            print(f"  • {travail['titre_travaux']} - {travail['statut']}")
    else:
        print(f"  (Aucun travail)")

    # Test 13: Test avec utilisateur lecteur
    print_header("TEST 13: Connexion avec utilisateur 'lecteur'")
    client2 = GestiBatAPIClient()
    client2.login("lecteur", "lect123")
    lecteur_sites = client2.get_sites()
    print(f"✅ Lecteur peut accéder à {lecteur_sites['count']} sites")

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
