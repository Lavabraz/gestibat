from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model
from travaux.pagination import StandardResultsPagination
from .models import Agent, AuditLog
from .serializers import (
    LoginSerializer, 
    AgentListSerializer, 
    AgentDetailSerializer,
    UserProfileSerializer,
    ChangeRoleSerializer,
    AuditLogSerializer
)
from .permissions import IsAdminUser, IsSuperAdmin, RoleBasedPermission

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Le refresh token est requis."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"detail": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Déconnexion réussie."}, status=status.HTTP_200_OK)


class AgentViewSet(ModelViewSet):
    """
    ViewSet pour la gestion des agents
    - list avec search (nom_complet, email) et filtre statut
    - retrieve avec services associés
    - CRUD réservé aux admins
    """
    queryset = Agent.objects.prefetch_related("agent_services__service").all()
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["nom_complet", "email"]
    ordering_fields = ["nom_complet", "email", "statut"]
    ordering = ["nom_complet"]
    filterset_fields = ["statut"]
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    pagination_class = StandardResultsPagination
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return AgentDetailSerializer
        return AgentListSerializer


class UserMeView(APIView):
    """
    Endpoint /api/users/me/ : retourne le profil de l'utilisateur connecté
    { id, nom_complet, email, role, agent: {...} }
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeRoleView(APIView):
    """
    Endpoint /api/users/change-role/ (POST, super_admin only)
    Body: { user_id, new_role }
    Change le rôle d'un utilisateur
    """
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    
    def post(self, request):
        serializer = ChangeRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = serializer.validated_data["user_id"]
        new_role = serializer.validated_data["new_role"]
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "L'utilisateur n'existe pas."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        old_role = user.role
        user.role = new_role
        user.save()
        
        # Log audit
        AuditLog.objects.create(
            user=request.user,
            action="UPDATE",
            model_name="CustomUser",
            object_id=str(user_id),
            object_display=user.username,
            description=f"Rôle changé de {old_role} à {new_role}"
        )
        
        return Response(
            {
                "detail": f"Rôle de {user.username} changé à {new_role}",
                "user_id": user_id,
                "old_role": old_role,
                "new_role": new_role
            },
            status=status.HTTP_200_OK
        )


class AuditLogViewSet(ModelViewSet):
    """
    ViewSet pour les logs d'audit
    - list pour voir l'historique
    - retrieve pour détail d'un log
    - Lecture seule
    """
    queryset = AuditLog.objects.select_related("user").all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["timestamp", "action", "model_name", "user"]
    ordering = ["-timestamp"]
    filterset_fields = ["action", "model_name", "user"]
    pagination_class = StandardResultsPagination
    
    def get_permissions(self):
        """Admin peut voir les logs, editeur aussi mais ses logs seulement"""
        if self.request.method in ["GET"]:
            # Tous les utilisateurs authentifiés peuvent voir les logs
            return [IsAuthenticated()]
        # Seul admin et super_admin peuvent accéder aux logs en détail
        return [IsAuthenticated(), IsAdminUser()]
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def recent_activity(self, request):
        """
        Endpoint custom pour l'activité récente (utilisé par dashboard)
        /api/users/audit-logs/recent_activity/ - Retourne les 10 derniers logs
        """
        logs = AuditLog.objects.select_related("user").all()[:10]
        serializer = AuditLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)