from django.db import models

from users.models import Service


class Site(models.Model):
    id_site = models.AutoField(primary_key=True)
    nom_site = models.CharField(max_length=150)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.nom_site


class Batiment(models.Model):
    id_batiment = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, related_name="batiments")
    nom_batiment = models.CharField(max_length=150)
    code_patrimoine = models.CharField(max_length=50, unique=True)
    surface_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    annee_construction = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.code_patrimoine} - {self.nom_batiment}"


class BatimentCaracteristiquesTech(models.Model):
    batiment = models.OneToOneField(
        Batiment,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="caracteristiques_tech",
    )
    type_usage = models.CharField(max_length=120)
    est_classe = models.BooleanField(default=False)
    potentiel_photovoltaique = models.CharField(max_length=120)
    zone_dangereuse = models.CharField(max_length=120)
    reseau_chaleur = models.BooleanField(default=False)
    etiquette_energetique = models.CharField(max_length=1)
    architecte = models.CharField(max_length=120)
    derniere_renovation_date = models.DateField()

    def __str__(self) -> str:
        return f"Caractéristiques {self.batiment.nom_batiment}"


class BatimentService(models.Model):
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name="services_associes")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="batiments_associes")
    pourcentage_occupation = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("batiment", "service")

    def __str__(self) -> str:
        return f"{self.batiment.nom_batiment} - {self.service.nom_service}"
