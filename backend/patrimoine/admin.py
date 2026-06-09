from django.contrib import admin

from .models import Batiment, BatimentCaracteristiquesTech, BatimentService, Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("id_site", "nom_site", "ville", "adresse")
    search_fields = ("nom_site", "ville", "adresse")
    list_filter = ("ville",)


@admin.register(Batiment)
class BatimentAdmin(admin.ModelAdmin):
    list_display = ("id_batiment", "code_patrimoine", "nom_batiment", "site", "surface_m2", "annee_construction")
    search_fields = ("code_patrimoine", "nom_batiment", "site__nom_site")
    list_filter = ("site", "annee_construction")


@admin.register(BatimentCaracteristiquesTech)
class BatimentCaracteristiquesTechAdmin(admin.ModelAdmin):
    list_display = (
        "batiment",
        "type_usage",
        "est_classe",
        "reseau_chaleur",
        "etiquette_energetique",
        "derniere_renovation_date",
    )
    search_fields = ("batiment__nom_batiment", "architecte", "type_usage")
    list_filter = ("est_classe", "reseau_chaleur", "etiquette_energetique")


@admin.register(BatimentService)
class BatimentServiceAdmin(admin.ModelAdmin):
    list_display = ("batiment", "service", "pourcentage_occupation")
    search_fields = ("batiment__nom_batiment", "service__nom_service")
    list_filter = ("service", "batiment__site")
