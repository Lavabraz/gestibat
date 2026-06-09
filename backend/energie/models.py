from django.db import models

from patrimoine.models import Batiment


class Compteur(models.Model):
    class TypeFluide(models.TextChoices):
        ELECTRICITE = "Électricité", "Électricité"
        GAZ = "Gaz", "Gaz"
        EAU = "Eau", "Eau"
        RESEAU_CHALEUR = "Réseau de chaleur", "Réseau de chaleur"

    id_compteur = models.AutoField(primary_key=True)
    batiment = models.ForeignKey(Batiment, on_delete=models.PROTECT, related_name="compteurs")
    reference_fournisseur = models.CharField(max_length=120)
    type_fluide = models.CharField(max_length=20, choices=TypeFluide.choices)

    def __str__(self) -> str:
        return f"{self.reference_fournisseur} ({self.type_fluide})"


class ConsommationFluide(models.Model):
    id_conso = models.AutoField(primary_key=True)
    compteur = models.ForeignKey(Compteur, on_delete=models.CASCADE, related_name="consommations")
    periode_mensuelle = models.DateField()
    valeur_index = models.DecimalField(max_digits=12, decimal_places=2)
    montant_ttc_facture = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.compteur.reference_fournisseur} - {self.periode_mensuelle:%Y-%m}"
