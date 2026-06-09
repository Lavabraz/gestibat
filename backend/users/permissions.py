from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role in {"super_admin", "admin"})


class IsAdminUser(BasePermission):
    """Permission pour super_admin et admin"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in {"super_admin", "admin"})


class IsSuperAdmin(BasePermission):
    """Permission pour super_admin uniquement"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "super_admin")


class RoleBasedPermission(BasePermission):
    """
    Permission basée sur les rôles:
    - super_admin : accès total
    - admin : CRUD sur tout sauf changer les rôles
    - editeur : lecture + création/modification (pas de suppression)
    - lecteur : lecture seule
    """
    
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        
        # super_admin a accès à tout
        if user.role == "super_admin":
            return True
        
        # Pour les autres, lectures et modifications selon le rôle
        if request.method in SAFE_METHODS:
            # Tous les utilisateurs authentifiés peuvent lire
            return True
        
        # Écritures
        if user.role == "admin":
            # Admin peut faire POST, PUT, PATCH
            return request.method in ["POST", "PUT", "PATCH"]
        
        if user.role == "editeur":
            # Editeur peut faire POST, PUT, PATCH (création/modification)
            return request.method in ["POST", "PUT", "PATCH"]
        
        # lecteur ne peut pas créer/modifier
        return False
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # super_admin a accès total
        if user.role == "super_admin":
            return True
        
        # Lecture pour tous
        if request.method in SAFE_METHODS:
            return True
        
        # Suppression réservée à admin et super_admin
        if request.method == "DELETE":
            return user.role in ["admin", "super_admin"]
        
        # Modification (PUT, PATCH) pour admin et editeur
        if request.method in ["PUT", "PATCH"]:
            return user.role in ["admin", "editeur", "super_admin"]
        
        return False


class IsOwnerOrReadOnly(BasePermission):
    """Permission pour que l'utilisateur modifie son propre profil"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Modification du profil seulement si c'est soi-même ou super_admin
        return obj == request.user or request.user.role == "super_admin"


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in {"super_admin", "admin"})
