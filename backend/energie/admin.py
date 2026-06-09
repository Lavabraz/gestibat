from django.contrib import admin

from .models import Compteur, ConsommationFluide


@admin.register(Compteur)
class CompteurAdmin(admin.ModelAdmin):
    list_display = ("id_compteur", "reference_fournisseur", "type_fluide", "batiment")
    search_fields = ("reference_fournisseur", "batiment__nom_batiment", "batiment__code_patrimoine")
    list_filter = ("type_fluide", "batiment__site")


@admin.register(ConsommationFluide)
class ConsommationFluideAdmin(admin.ModelAdmin):
    list_display = ("id_conso", "compteur", "periode_mensuelle", "valeur_index", "montant_ttc_facture")
    search_fields = ("compteur__reference_fournisseur", "compteur__batiment__nom_batiment")
    list_filter = ("periode_mensuelle", "compteur__type_fluide")
