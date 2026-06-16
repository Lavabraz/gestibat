from datetime import date, timedelta

from django.db.models import Max
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from energie.models import Compteur
from patrimoine.models import Batiment
from users.models import Agent
from users.permissions import IsAdminUser

from .models import Investissement, Travaux
from .serializers import InvestissementSerializer, TravauxDetailSerializer, TravauxListSerializer
from .pagination import StandardResultsPagination


class TravauxViewSet(viewsets.ModelViewSet):
    queryset = Travaux.objects.select_related("batiment", "investissement", "service_demandeur", "responsable_interne")
    pagination_class = StandardResultsPagination

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = self.queryset
        statut = self.request.query_params.get("statut")
        batiment = self.request.query_params.get("batiment")
        domaine_metier = self.request.query_params.get("domaine_metier")

        if statut:
            statut_normalise = statut.replace("_", "").replace(" ", "").lower()
            if statut_normalise == "encours":
                statut = "En cours"
            queryset = queryset.filter(statut__iexact=statut)
        if batiment:
            queryset = queryset.filter(batiment_id=batiment)
        if domaine_metier:
            queryset = queryset.filter(domaine_metier__iexact=domaine_metier)
        return queryset.order_by("-date_demande")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TravauxDetailSerializer
        if self.action == "list":
            return TravauxListSerializer
        return TravauxDetailSerializer

    @action(detail=True, methods=["post"])
    def cloturer(self, request, pk=None):
        travaux = self.get_object()
        travaux.statut = "Terminé"
        travaux.date_fin_reelle = date.today()
        travaux.save(update_fields=["statut", "date_fin_reelle"])
        return Response(self.get_serializer(travaux).data, status=status.HTTP_200_OK)


class InvestissementViewSet(viewsets.ModelViewSet):
    serializer_class = InvestissementSerializer
    queryset = Investissement.objects.select_related("batiment", "service_pilote").all()
    pagination_class = StandardResultsPagination

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = self.queryset
        statut = self.request.query_params.get("statut")
        annee = self.request.query_params.get("annee_programmation")
        if statut:
            queryset = queryset.filter(statut__iexact=statut)
        if annee:
            queryset = queryset.filter(annee_programmation=annee)
        return queryset.order_by("-annee_programmation", "-id_investissement")


class DashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_batiments = Batiment.objects.count()
        total_agents_actifs = Agent.objects.exclude(statut=Agent.Statut.VACATAIRE).count()
        agents_remplacants = Agent.objects.filter(statut=Agent.Statut.REMPLACANT).count()
        total_travaux_en_cours = Travaux.objects.filter(statut__iexact="En cours").count()
        total_investissements_valides = Investissement.objects.filter(statut=Investissement.Statut.VALIDE).count()

        alertes = []
        urgent_without_end = Travaux.objects.filter(
            type_travaux=Travaux.TypeTravaux.URGENCE, date_fin_previsionnelle__isnull=True
        ).count()
        if urgent_without_end:
            alertes.append(
                {
                    "type": "danger",
                    "titre": "Travaux urgents sans date de fin",
                    "detail": f"{urgent_without_end} travaux urgents n'ont pas de date de fin previsionnelle.",
                    "date": date.today().isoformat(),
                }
            )

        cutoff = date.today() - timedelta(days=30)
        stale_compteurs = (
            Compteur.objects.annotate(last_releve=Max("consommations__periode_mensuelle"))
            .filter(last_releve__lt=cutoff)
            .count()
        )
        never_releve = Compteur.objects.annotate(last_releve=Max("consommations__periode_mensuelle")).filter(
            last_releve__isnull=True
        ).count()
        stale_total = stale_compteurs + never_releve
        if stale_total:
            alertes.append(
                {
                    "type": "warning",
                    "titre": "Compteurs sans releve recent",
                    "detail": f"{stale_total} compteurs sans releve depuis plus de 30 jours.",
                    "date": date.today().isoformat(),
                }
            )

        old_engaged = Investissement.objects.filter(
            statut=Investissement.Statut.ENGAGE,
            annee_programmation__lte=date.today().year - 1,
        ).count()
        if old_engaged:
            alertes.append(
                {
                    "type": "warning",
                    "titre": "Investissements engages anciens",
                    "detail": f"{old_engaged} investissements engages depuis plus d'un an sans cloture.",
                    "date": date.today().isoformat(),
                }
            )

        if not alertes:
            alertes.append(
                {
                    "type": "success",
                    "titre": "Aucune alerte bloquante",
                    "detail": "Les indicateurs critiques sont au vert.",
                    "date": date.today().isoformat(),
                }
            )

        activite = []
        recent_travaux = Travaux.objects.select_related("responsable_interne", "batiment").order_by("-date_demande")[:5]
        for t in recent_travaux:
            activite.append(
                {
                    "auteur": t.responsable_interne.nom_complet if t.responsable_interne else "Systeme",
                    "action": f"Travaux '{t.titre_travaux}' ({t.statut}) sur {t.batiment.nom_batiment}",
                    "timestamp": t.date_demande.isoformat(),
                }
            )

        recent_invest = Investissement.objects.select_related("service_pilote").order_by("-id_investissement")[:5]
        for inv in recent_invest:
            activite.append(
                {
                    "auteur": inv.service_pilote.nom_service,
                    "action": f"Investissement '{inv.titre_projet}' ({inv.statut})",
                    "timestamp": date(inv.annee_programmation, 1, 1).isoformat(),
                }
            )

        activite = sorted(activite, key=lambda x: x["timestamp"], reverse=True)[:10]

        return Response(
            {
                "kpis": {
                    "total_batiments": total_batiments,
                    "total_agents_actifs": total_agents_actifs,
                    "agents_remplacants": agents_remplacants,
                    "total_travaux_en_cours": total_travaux_en_cours,
                    "total_investissements_valides": total_investissements_valides,
                },
                "alertes": alertes,
                "activite_recente": activite,
            }
        )