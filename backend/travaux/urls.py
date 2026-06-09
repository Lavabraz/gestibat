from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InvestissementViewSet, TravauxViewSet

router = DefaultRouter()
router.register("travaux", TravauxViewSet, basename="travaux")
router.register("investissements", InvestissementViewSet, basename="investissements")

urlpatterns = [
    path("", include(router.urls)),
]
