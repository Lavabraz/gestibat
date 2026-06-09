from django.contrib import admin

from .models import Investissement, Travaux


@admin.register(Investissement)
class InvestissementAdmin(admin.ModelAdmin):
    list_display = (
        "id_investissement",
        "titre_projet",
        "batiment",
        "service_pilote",
        "annee_programmation",
        "budget_estime",
        "cout_reel",
        "statut",
        "priorite_strategique",
    )
    search_fields = ("titre_projet", "batiment__nom_batiment", "service_pilote__nom_service", "type_investissement")
    list_filter = ("statut", "annee_programmation", "service_pilote")


@admin.register(Travaux)
class TravauxAdmin(admin.ModelAdmin):
    list_display = (
        "id_travaux",
        "titre_travaux",
        "batiment",
        "service_demandeur",
        "domaine_metier",
        "type_travaux",
        "priorite",
        "date_demande",
        "statut",
    )
    search_fields = (
        "titre_travaux",
        "batiment__nom_batiment",
        "service_demandeur__nom_service",
        "intervenant_externe",
        "responsable_interne__nom_complet",
    )
    list_filter = ("domaine_metier", "type_travaux", "statut", "service_demandeur")
