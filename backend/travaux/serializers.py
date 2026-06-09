from rest_framework import serializers

from .models import Investissement, Travaux


class InvestissementSerializer(serializers.ModelSerializer):
    batiment_nom = serializers.CharField(source="batiment.nom_batiment", read_only=True)
    service_pilote_nom = serializers.CharField(source="service_pilote.nom_service", read_only=True)

    class Meta:
        model = Investissement
        fields = "__all__"


class TravauxListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="id_travaux", read_only=True)
    batiment_nom = serializers.CharField(source="batiment.nom_batiment", read_only=True)

    class Meta:
        model = Travaux
        fields = (
            "id",
            "titre_travaux",
            "statut",
            "priorite",
            "batiment_nom",
            "date_demande",
            "date_fin_previsionnelle",
            "type_travaux",
        )


class TravauxDetailSerializer(serializers.ModelSerializer):
    batiment_nom = serializers.CharField(source="batiment.nom_batiment", read_only=True)
    investissement_detail = InvestissementSerializer(source="investissement", read_only=True)

    class Meta:
        model = Travaux
        fields = "__all__"
