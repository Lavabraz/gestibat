from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from rest_framework import filters, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdminUser

from .models import Batiment, Site
from .serializers import (
    BatimentDetailSerializer,
    BatimentListSerializer,
    SiteDetailSerializer,
    SiteListSerializer,
)


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all().order_by("nom_site")
    filter_backends = [filters.SearchFilter]
    search_fields = ["nom_site"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = Site.objects.annotate(nombre_batiments=Count("batiments")).order_by("nom_site")
        ville = self.request.query_params.get("ville")
        if ville:
            queryset = queryset.filter(ville__iexact=ville)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SiteDetailSerializer
        return SiteListSerializer


class BatimentViewSet(viewsets.ModelViewSet):
    queryset = Batiment.objects.select_related("site", "caracteristiques_tech").all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nom_batiment", "code_patrimoine", "site__nom_site"]
    ordering_fields = ["nom_batiment", "surface_m2", "annee_construction", "code_patrimoine"]
    ordering = ["nom_batiment"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = (
            Batiment.objects.select_related("site", "caracteristiques_tech")
            .prefetch_related("services_associes__service", "compteurs", "travaux")
            .all()
        )
        site_id = self.request.query_params.get("site")
        type_usage = self.request.query_params.get("type_usage")
        ville = self.request.query_params.get("ville")

        if site_id:
            queryset = queryset.filter(site_id=site_id)
        if type_usage:
            queryset = queryset.filter(caracteristiques_tech__type_usage__iexact=type_usage)
        if ville:
            queryset = queryset.filter(site__ville__iexact=ville)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BatimentDetailSerializer
        return BatimentListSerializer


class PatrimoineStatsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        total_batiments = Batiment.objects.count()
        total_sites = Site.objects.count()
        total_surface = Batiment.objects.aggregate(total=Coalesce(Sum("surface_m2"), 0))["total"]

        by_type = (
            Batiment.objects.values("caracteristiques_tech__type_usage")
            .annotate(total=Count("id_batiment"))
            .order_by("caracteristiques_tech__type_usage")
        )
        by_ville = Batiment.objects.values("site__ville").annotate(total=Count("id_batiment")).order_by("site__ville")

        return Response(
            {
                "total_batiments": total_batiments,
                "total_sites": total_sites,
                "total_surface_m2": total_surface,
                "batiments_par_type_usage": {
                    item["caracteristiques_tech__type_usage"] or "Non renseigne": item["total"] for item in by_type
                },
                "batiments_par_ville": {item["site__ville"] or "Non renseignee": item["total"] for item in by_ville},
            }
        )
