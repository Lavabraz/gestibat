from django.contrib import admin
from django.urls import include, path
from travaux.views import DashboardAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/users/", include("users.urls")),  # Également disponible sous /api/users/
    path("api/patrimoine/", include("patrimoine.urls")),
    path("api/travaux/", include("travaux.urls")),
    path("api/dashboard/", DashboardAPIView.as_view()),
]
