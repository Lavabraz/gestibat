from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Agent, AgentService, CustomUser, Pole, Service, AuditLog


@admin.register(Pole)
class PoleAdmin(admin.ModelAdmin):
    list_display = ("id_pole", "code_pole", "nom_pole", "responsable_pole")
    search_fields = ("code_pole", "nom_pole", "responsable_pole")
    list_filter = ("code_pole",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id_service", "nom_service", "pole")
    search_fields = ("nom_service", "pole__nom_pole", "pole__code_pole")
    list_filter = ("pole",)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("id_agent", "nom_complet", "email", "statut")
    search_fields = ("nom_complet", "email")
    list_filter = ("statut",)


@admin.register(AgentService)
class AgentServiceAdmin(admin.ModelAdmin):
    list_display = ("agent", "service", "role_dans_service")
    search_fields = ("agent__nom_complet", "service__nom_service")
    list_filter = ("service__pole",)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "agent", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "agent__nom_complet")
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Rôle & Agent', {'fields': ('role', 'agent')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action", "model_name", "object_display", "timestamp")
    list_filter = ("action", "model_name", "timestamp", "user")
    search_fields = ("user__username", "model_name", "object_display", "description")
    readonly_fields = ("user", "action", "model_name", "object_id", "object_display", "description", "timestamp")
    
    def has_add_permission(self, request):
        # Les logs ne peuvent être créés que automatiquement
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Les logs ne peuvent être supprimés que par les super_admin
        return request.user.is_superuser
