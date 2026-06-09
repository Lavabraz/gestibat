from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Agent, AgentService, AuditLog, Service


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    identifiant = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifiant = attrs.get("identifiant")
        password = attrs.get("password")

        user = authenticate(username=identifiant, password=password)

        # Allow login with email as identifiant.
        if user is None:
            user_obj = User.objects.filter(email=identifiant).first()
            if user_obj:
                user = authenticate(username=user_obj.username, password=password)

        if user is None:
            raise serializers.ValidationError("Identifiants invalides.")

        refresh = RefreshToken.for_user(user)

        nom_complet = user.agent.nom_complet if getattr(user, "agent", None) else user.get_full_name() or user.username
        access = str(refresh.access_token)
        refresh_str = str(refresh)
        attrs["access"] = access
        attrs["refresh"] = refresh_str
        attrs["access_token"] = access
        attrs["refresh_token"] = refresh_str
        attrs["user"] = {
            "id": user.id,
            "nom_complet": nom_complet,
            "role": user.role,
            "email": user.email,
        }
        return attrs


class ServiceNestedSerializer(serializers.ModelSerializer):
    pole_nom = serializers.CharField(source="pole.nom_pole", read_only=True)
    
    class Meta:
        model = Service
        fields = ["id_service", "nom_service", "pole_nom"]


class AgentServiceSerializer(serializers.ModelSerializer):
    service_detail = ServiceNestedSerializer(source="service", read_only=True)
    
    class Meta:
        model = AgentService
        fields = ["service_detail", "role_dans_service"]


class AgentListSerializer(serializers.ModelSerializer):
    """Serializer léger pour liste des agents"""
    class Meta:
        model = Agent
        fields = ["id_agent", "nom_complet", "email", "statut"]


class AgentDetailSerializer(serializers.ModelSerializer):
    """Serializer complet pour détail agent avec services"""
    agent_services = AgentServiceSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_role = serializers.CharField(source="user.role", read_only=True)
    
    class Meta:
        model = Agent
        fields = ["id_agent", "nom_complet", "email", "statut", "user_id", "user_role", "agent_services"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil utilisateur connecté"""
    agent = AgentDetailSerializer(read_only=True)
    nom_complet = serializers.SerializerMethodField()
    
    def get_nom_complet(self, obj):
        if obj.agent:
            return obj.agent.nom_complet
        return obj.get_full_name() or obj.username
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "nom_complet", "role", "agent"]
        read_only_fields = ["id", "username", "role"]


class ChangeRoleSerializer(serializers.Serializer):
    """Serializer pour changer le rôle d'un utilisateur (super_admin only)"""
    user_id = serializers.IntegerField()
    new_role = serializers.ChoiceField(choices=["super_admin", "admin", "editeur", "lecteur"])
    
    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("L'utilisateur n'existe pas.")
        return value


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer pour les logs d'audit"""
    user_username = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ["id", "user_id", "user_username", "action", "model_name", "object_id", 
                  "object_display", "description", "timestamp"]
        read_only_fields = fields
