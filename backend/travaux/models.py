from django.db import models

from patrimoine.models import Batiment
from users.models import Agent, Service


class Investissement(models.Model):
    class Statut(models.TextChoices):
        PROPOSITION = "Proposition", "Proposition"
        VALIDE = "Validé", "Validé"
        ENGAGE = "Engagé", "Engagé"
        TERMINE = "Terminé", "Terminé"

    id_investissement = models.AutoField(primary_key=True)
    batiment = models.ForeignKey(Batiment, on_delete=models.PROTECT, related_name="investissements")
    service_pilote = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="investissements_pilotes")
    titre_projet = models.CharField(max_length=200)
    type_investissement = models.CharField(max_length=120)
    annee_programmation = models.PositiveIntegerField()
    budget_estime = models.DecimalField(max_digits=12, decimal_places=2)
    cout_reel = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=Statut.choices)
    priorite_strategique = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.titre_projet


class Travaux(models.Model):
    class DomaineMetier(models.TextChoices):
        BATIMENT = "Bâtiment", "Bâtiment"
        ESPACES_VERTS = "Espaces Verts", "Espaces Verts"
        VOIRIE = "Voirie", "Voirie"
        DSI = "DSI", "DSI"

    class TypeTravaux(models.TextChoices):
        ENTRETIEN = "Entretien", "Entretien"
        AMELIORATION = "Amélioration", "Amélioration"
        URGENCE = "Urgence", "Urgence"

    id_travaux = models.AutoField(primary_key=True)
    batiment = models.ForeignKey(Batiment, on_delete=models.PROTECT, related_name="travaux")
    service_demandeur = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="travaux_demandes")
    investissement = models.ForeignKey(
        Investissement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="travaux_associes",
    )
    domaine_metier = models.CharField(max_length=20, choices=DomaineMetier.choices)
    titre_travaux = models.CharField(max_length=200)
    type_travaux = models.CharField(max_length=20, choices=TypeTravaux.choices)
    priorite = models.CharField(max_length=50)
    date_demande = models.DateField()
    date_fin_previsionnelle = models.DateField(null=True, blank=True)
    date_fin_reelle = models.DateField(null=True, blank=True)
    responsable_interne = models.ForeignKey(
        Agent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="travaux_responsables",
    )
    intervenant_externe = models.CharField(max_length=120, null=True, blank=True)
    statut = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.titre_travaux
