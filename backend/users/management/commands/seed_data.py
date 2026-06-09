import random
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from energie.models import Compteur, ConsommationFluide
from patrimoine.models import Batiment, BatimentCaracteristiquesTech, BatimentService, Site
from travaux.models import Investissement, Travaux
from users.models import Agent, AgentService, Pole, Service


class Command(BaseCommand):
    help = "Peuple la base avec des donnees de test realistes pour GestiBat."

    def handle(self, *args, **options):
        fake = Faker("fr_FR")
        random.seed(42)
        Faker.seed(42)

        with transaction.atomic():
            self._clear_existing_data()

            poles = self._create_poles()
            services = self._create_services(poles)
            agents = self._create_agents(fake)
            self._create_agent_services(agents, services)
            sites = self._create_sites()
            batiments = self._create_batiments_and_tech(fake, sites, services)
            compteurs = self._create_compteurs(batiments)
            self._create_consommations(compteurs)
            investissements = self._create_investissements(fake, batiments, services)
            self._create_travaux(fake, batiments, services, agents, investissements)
            self._create_test_users(agents)

        self.stdout.write(self.style.SUCCESS("Seed termine avec succes."))

    def _clear_existing_data(self):
        ConsommationFluide.objects.all().delete()
        Compteur.objects.all().delete()
        Travaux.objects.all().delete()
        Investissement.objects.all().delete()
        BatimentService.objects.all().delete()
        BatimentCaracteristiquesTech.objects.all().delete()
        Batiment.objects.all().delete()
        Site.objects.all().delete()
        AgentService.objects.all().delete()

        User = get_user_model()
        User.objects.exclude(username="admin").exclude(username="editeur").exclude(username="lecteur").exclude(
            username="superadmin"
        ).delete()

        Agent.objects.all().delete()
        Service.objects.all().delete()
        Pole.objects.all().delete()

    def _create_poles(self):
        return [
            Pole.objects.create(
                code_pole="POLE_ADT",
                nom_pole="Administration",
                responsable_pole="Directeur Pole Administration",
            ),
            Pole.objects.create(
                code_pole="POLE_BAT",
                nom_pole="Batiment",
                responsable_pole="Directeur Pole Batiment",
            ),
            Pole.objects.create(
                code_pole="POLE_ENV",
                nom_pole="Environnement",
                responsable_pole="Directeur Pole Environnement",
            ),
        ]

    def _create_services(self, poles):
        service_names = {
            "POLE_ADT": ["Ressources Humaines", "Finances et Commande Publique"],
            "POLE_BAT": ["Patrimoine Bati", "Maintenance Technique"],
            "POLE_ENV": ["Transition Energetique", "Gestion de l'Eau et Dechets"],
        }
        services = []
        for pole in poles:
            for name in service_names[pole.code_pole]:
                services.append(Service.objects.create(pole=pole, nom_service=name))
        return services

    def _create_agents(self, fake):
        statuts = [choice[0] for choice in Agent.Statut.choices]
        agents = []
        for _ in range(15):
            first = fake.first_name()
            last = fake.last_name()
            nom_complet = f"{first} {last}"
            email = f"{first.lower()}.{last.lower()}@ccalf.local".replace(" ", "").replace("'", "")
            agents.append(
                Agent.objects.create(
                    nom_complet=nom_complet,
                    email=email,
                    statut=random.choice(statuts),
                )
            )
        return agents

    def _create_agent_services(self, agents, services):
        roles = [
            "Chef de service",
            "Charge de mission",
            "Gestionnaire",
            "Technicien",
            "Referent metier",
            "Coordinateur",
        ]
        for agent in agents:
            service = random.choice(services)
            AgentService.objects.create(
                agent=agent,
                service=service,
                role_dans_service=random.choice(roles),
            )

    def _create_sites(self):
        site_data = [
            ("Mairie Ambert", "Place Charles de Gaulle", "Ambert"),
            ("Centre Culturel", "12 Rue de la Liberte", "Ambert"),
            ("Piscine Ambert Livradois Forez", "Avenue des Sports", "Ambert"),
            ("Ecole Primaire", "8 Rue des Ecoles", "Ambert"),
            ("Mediatheque", "5 Place du Pontel", "Ambert"),
        ]
        return [Site.objects.create(nom_site=n, adresse=a, ville=v) for n, a, v in site_data]

    def _create_batiments_and_tech(self, fake, sites, services):
        usages = ["Administratif", "Scolaire", "Culturel", "Sportif", "Technique", "Mixte"]
        potentiels = ["Faible", "Moyen", "Eleve"]
        zones = ["Aucune", "Atelier", "Local technique", "Chaufferie"]
        etiquettes = ["A", "B", "C", "D", "E"]
        batiments = []

        for idx in range(1, 21):
            site = sites[(idx - 1) % len(sites)]
            batiment = Batiment.objects.create(
                site=site,
                nom_batiment=f"{site.nom_site} - Batiment {idx:02d}",
                code_patrimoine=f"CALF-BAT-{idx:03d}",
                surface_m2=Decimal(random.randint(250, 3500)) + Decimal("0.50"),
                annee_construction=random.randint(1965, 2022),
            )
            batiments.append(batiment)

            BatimentCaracteristiquesTech.objects.create(
                batiment=batiment,
                type_usage=random.choice(usages),
                est_classe=random.choice([True, False, False]),
                potentiel_photovoltaique=random.choice(potentiels),
                zone_dangereuse=random.choice(zones),
                reseau_chaleur=random.choice([True, False]),
                etiquette_energetique=random.choice(etiquettes),
                architecte=fake.name(),
                derniere_renovation_date=fake.date_between(start_date="-8y", end_date="today"),
            )

            occupied_services = random.sample(services, k=random.randint(1, 2))
            percentages = [Decimal("100.00")] if len(occupied_services) == 1 else [Decimal("60.00"), Decimal("40.00")]
            for service, pct in zip(occupied_services, percentages):
                BatimentService.objects.create(
                    batiment=batiment,
                    service=service,
                    pourcentage_occupation=pct,
                )

        return batiments

    def _create_compteurs(self, batiments):
        fluides = [Compteur.TypeFluide.ELECTRICITE, Compteur.TypeFluide.GAZ, Compteur.TypeFluide.EAU]
        compteurs = []
        for idx in range(1, 31):
            compteur = Compteur.objects.create(
                batiment=random.choice(batiments),
                reference_fournisseur=f"CPT-{10000 + idx}",
                type_fluide=random.choice(fluides),
            )
            compteurs.append(compteur)
        return compteurs

    def _create_consommations(self, compteurs):
        months = []
        cursor = date.today().replace(day=1)
        for _ in range(12):
            months.append(cursor)
            if cursor.month == 1:
                cursor = cursor.replace(year=cursor.year - 1, month=12)
            else:
                cursor = cursor.replace(month=cursor.month - 1)
        for idx in range(60):
            compteur = compteurs[idx % len(compteurs)]
            period = random.choice(months)
            value = Decimal(random.randint(100, 25000)) + Decimal("0.25")
            amount = (value * Decimal(random.uniform(0.05, 0.3))).quantize(Decimal("0.01"))
            ConsommationFluide.objects.create(
                compteur=compteur,
                periode_mensuelle=period,
                valeur_index=value,
                montant_ttc_facture=amount,
            )

    def _create_investissements(self, fake, batiments, services):
        statuts = [choice[0] for choice in Investissement.Statut.choices]
        types = ["Renovation energetique", "Mise aux normes", "Extension", "Rehabilitation", "Modernisation"]
        priorites = ["Haute", "Moyenne", "Basse", "Strategique"]
        investissements = []
        for idx in range(1, 6):
            budget = Decimal(random.randint(50000, 550000))
            has_real_cost = random.choice([True, False])
            cout_reel = (budget * Decimal(random.uniform(0.85, 1.15))).quantize(Decimal("0.01")) if has_real_cost else None
            investissements.append(
                Investissement.objects.create(
                    batiment=random.choice(batiments),
                    service_pilote=random.choice(services),
                    titre_projet=f"Programme {fake.word().capitalize()} {idx}",
                    type_investissement=random.choice(types),
                    annee_programmation=random.randint(date.today().year - 1, date.today().year + 2),
                    budget_estime=budget,
                    cout_reel=cout_reel,
                    statut=random.choice(statuts),
                    priorite_strategique=random.choice(priorites),
                )
            )
        return investissements

    def _create_travaux(self, fake, batiments, services, agents, investissements):
        domaines = [choice[0] for choice in Travaux.DomaineMetier.choices]
        types = [choice[0] for choice in Travaux.TypeTravaux.choices]
        statuts = ["Propose", "Valide", "En cours", "Planifie", "Termine", "Suspendu"]
        priorites = ["Basse", "Moyenne", "Haute", "Critique"]

        for idx in range(1, 11):
            date_demande = fake.date_between(start_date="-1y", end_date="today")
            end_prev = date_demande + timedelta(days=random.randint(30, 240))
            date_fin_reelle = end_prev + timedelta(days=random.randint(-20, 30)) if random.choice([True, False]) else None

            Travaux.objects.create(
                batiment=random.choice(batiments),
                service_demandeur=random.choice(services),
                investissement=random.choice(investissements + [None, None]),
                domaine_metier=random.choice(domaines),
                titre_travaux=f"Travaux {idx} - {fake.word().capitalize()}",
                type_travaux=random.choice(types),
                priorite=random.choice(priorites),
                date_demande=date_demande,
                date_fin_previsionnelle=end_prev,
                date_fin_reelle=date_fin_reelle,
                responsable_interne=random.choice(agents + [None]),
                intervenant_externe=fake.company() if random.choice([True, False]) else None,
                statut=random.choice(statuts),
            )

    def _create_test_users(self, agents):
        User = get_user_model()
        mapping = [
            ("admin", "admin123", "admin"),
            ("editeur", "edit123", "editeur"),
            ("lecteur", "lect123", "lecteur"),
            ("superadmin", "super123", "super_admin"),
        ]

        for idx, (username, password, role) in enumerate(mapping):
            user, _ = User.objects.get_or_create(username=username)
            user.email = f"{username}@ccalf.local"
            user.role = role
            user.agent = agents[idx % len(agents)]
            user.is_staff = role in {"admin", "super_admin"}
            user.is_superuser = role == "super_admin"
            user.set_password(password)
            user.save()
