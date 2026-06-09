from rest_framework import serializers

from energie.models import Compteur
from travaux.models import Travaux

from .models import Batiment, BatimentCaracteristiquesTech, BatimentService, Site


class BatimentCaracteristiquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatimentCaracteristiquesTech
        fields = "__all__"


class BatimentListSerializer(serializers.ModelSerializer):
    site_nom = serializers.CharField(source="site.nom_site", read_only=True)
    ville = serializers.CharField(source="site.ville", read_only=True)
    type_usage = serializers.CharField(source="caracteristiques_tech.type_usage", read_only=True)

    class Meta:
        model = Batiment
        fields = (
            "id_batiment",
            "nom_batiment",
            "code_patrimoine",
            "surface_m2",
            "site",
            "site_nom",
            "ville",
            "type_usage",
        )


class SiteBatimentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batiment
        fields = ("id_batiment", "nom_batiment", "code_patrimoine", "surface_m2", "annee_construction")


class SiteListSerializer(serializers.ModelSerializer):
    nombre_batiments = serializers.IntegerField(read_only=True)

    class Meta:
        model = Site
        fields = ("id_site", "nom_site", "adresse", "ville", "nombre_batiments")


class SiteDetailSerializer(serializers.ModelSerializer):
    batiments = SiteBatimentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = ("id_site", "nom_site", "adresse", "ville", "batiments")


class BatimentServiceNestedSerializer(serializers.ModelSerializer):
    service_nom = serializers.CharField(source="service.nom_service", read_only=True)
    service_id = serializers.IntegerField(source="service.id_service", read_only=True)

    class Meta:
        model = BatimentService
        fields = ("service_id", "service_nom", "pourcentage_occupation")


class CompteurNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compteur
        fields = ("id_compteur", "reference_fournisseur", "type_fluide")


class TravauxNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travaux
        fields = ("id_travaux", "titre_travaux", "statut", "date_demande", "date_fin_previsionnelle", "date_fin_reelle")


class BatimentDetailSerializer(serializers.ModelSerializer):
    site_nom = serializers.CharField(source="site.nom_site", read_only=True)
    ville = serializers.CharField(source="site.ville", read_only=True)
    caracteristiques_tech = BatimentCaracteristiquesSerializer(read_only=True)
    services_occupants = BatimentServiceNestedSerializer(source="services_associes", many=True, read_only=True)
    compteurs = CompteurNestedSerializer(many=True, read_only=True)
    derniers_travaux = serializers.SerializerMethodField()

    class Meta:
        model = Batiment
        fields = (
            "id_batiment",
            "site",
            "site_nom",
            "ville",
            "nom_batiment",
            "code_patrimoine",
            "surface_m2",
            "annee_construction",
            "caracteristiques_tech",
            "services_occupants",
            "compteurs",
            "derniers_travaux",
        )

    def get_derniers_travaux(self, obj):
        qs = obj.travaux.order_by("-date_demande")[:3]
        return TravauxNestedSerializer(qs, many=True).data
