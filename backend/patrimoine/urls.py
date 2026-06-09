from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BatimentViewSet, PatrimoineStatsAPIView, SiteViewSet

router = DefaultRouter()
router.register("sites", SiteViewSet, basename="sites")
router.register("batiments", BatimentViewSet, basename="batiments")

urlpatterns = [
    path("", include(router.urls)),
    path("stats/", PatrimoineStatsAPIView.as_view(), name="patrimoine-stats"),
]
