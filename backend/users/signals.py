"""
Signaux Django pour l'audit logging automatique
Logs automatiquement les POST/PUT/DELETE sur les modèles principaux
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import AuditLog

User = get_user_model()


def create_audit_log(sender, user, action, object_id, object_display="", description=""):
    """
    Fonction utilitaire pour créer un log audit
    Utilisée par les signaux et autres parties du code
    """
    if user and hasattr(user, 'id'):
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=sender.__name__,
            object_id=str(object_id),
            object_display=object_display or str(object_id),
            description=description
        )


# Enregistrement des signaux pour les modèles principaux
def register_audit_signals():
    """
    Enregistre les signaux d'audit pour les modèles Django
    Appelée dans apps.py
    """
    from patrimoine.models import Site, Batiment
    from travaux.models import Travaux, Investissement
    from energie.models import Compteur
    from .models import Agent, Pole, Service
    
    # Les signaux seront connectés via les imports ci-dessous
    pass


# Signal pour créer les logs audit via les vues DRF
# (Plus tard, nous connecterons les signaux spécifiques par vue)


@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    """Log les créations/modifications d'utilisateurs"""
    # Ne pas logger les changements de token ou autres propriétés internes
    if hasattr(instance, '_do_not_audit'):
        return
    
    # Récupérer l'utilisateur depuis le contexte de la requête
    # (sera passé via middleware/request)
    pass


@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    """Log les suppressions d'utilisateurs"""
    pass
