"""
Mixin pour l'audit logging automatique dans les ViewSets DRF
Logs automatiquement les POST/PUT/DELETE sur les instances
"""

from rest_framework.response import Response
from .models import AuditLog


class AuditLogMixin:
    """
    Mixin pour ajouter l'audit logging automatique aux ViewSets
    
    Usage:
        class MonViewSet(AuditLogMixin, ModelViewSet):
            ...
    """
    
    def get_audit_user(self):
        """Récupère l'utilisateur depuis la requête"""
        return self.request.user if self.request and self.request.user.is_authenticated else None
    
    def get_object_display(self, instance):
        """Retourne une représentation lisible de l'objet"""
        if hasattr(instance, 'nom_batiment'):
            return f"{instance.nom_batiment} ({instance.code_patrimoine})"
        elif hasattr(instance, 'titre_travaux'):
            return instance.titre_travaux
        elif hasattr(instance, 'nom_pole'):
            return instance.nom_pole
        elif hasattr(instance, 'nom_service'):
            return instance.nom_service
        elif hasattr(instance, 'nom_complet'):
            return instance.nom_complet
        return str(instance)
    
    def create(self, request, *args, **kwargs):
        """Crée un objet et log l'audit"""
        response = super().create(request, *args, **kwargs)
        
        # Log la création
        if response.status_code in [201, 200]:
            user = self.get_audit_user()
            instance = self.get_object() if hasattr(self, 'get_object') else None
            
            # Récupérer l'ID depuis la réponse
            object_id = response.data.get('id') or response.data.get('id_agent') or response.data.get('id_travaux') or '?'
            object_display = self.get_object_display(instance) if instance else "Nouvel objet"
            
            AuditLog.objects.create(
                user=user,
                action="CREATE",
                model_name=self.queryset.model.__name__,
                object_id=str(object_id),
                object_display=object_display,
                description=f"Créé via API par {user.username if user else 'Anonyme'}"
            )
        
        return response
    
    def update(self, request, *args, **kwargs):
        """Met à jour un objet et log l'audit"""
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)
        
        # Log la modification
        if response.status_code in [200]:
            user = self.get_audit_user()
            object_display = self.get_object_display(instance)
            
            # Récupérer les champs modifiés
            modified_fields = list(request.data.keys())
            
            AuditLog.objects.create(
                user=user,
                action="UPDATE",
                model_name=self.queryset.model.__name__,
                object_id=str(instance.pk),
                object_display=object_display,
                description=f"Modifié: {', '.join(modified_fields[:3])}{'...' if len(modified_fields) > 3 else ''}"
            )
        
        return response
    
    def destroy(self, request, *args, **kwargs):
        """Supprime un objet et log l'audit"""
        instance = self.get_object()
        object_id = instance.pk
        object_display = self.get_object_display(instance)
        
        response = super().destroy(request, *args, **kwargs)
        
        # Log la suppression
        if response.status_code in [204, 200]:
            user = self.get_audit_user()
            
            AuditLog.objects.create(
                user=user,
                action="DELETE",
                model_name=self.queryset.model.__name__,
                object_id=str(object_id),
                object_display=object_display,
                description=f"Supprimé via API par {user.username if user else 'Anonyme'}"
            )
        
        return response
