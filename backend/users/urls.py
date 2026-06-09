from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView, 
    LogoutView, 
    RefreshView, 
    UserMeView,
    ChangeRoleView,
    AgentViewSet,
    AuditLogViewSet
)

router = DefaultRouter()
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    # Auth endpoints
    path("login/", LoginView.as_view(), name="auth-login"),
    path("refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    
    # User endpoints
    path("me/", UserMeView.as_view(), name="user-profile"),
    path("change-role/", ChangeRoleView.as_view(), name="change-role"),
    
    # Router endpoints
    path("", include(router.urls)),
]

