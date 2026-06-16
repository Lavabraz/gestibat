"""
Middleware pour l'audit logging automatique.
Stocke l'utilisateur courant dans un thread-local storage pour que
les signaux puissent y accéder.
"""

import threading
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

_thread_locals = threading.local()


def get_current_user():
    """Recupere l'utilisateur courant depuis le thread-local storage"""
    return getattr(_thread_locals, 'user', None)


def set_current_user(user):
    """Stocke l'utilisateur courant dans le thread-local storage"""
    _thread_locals.user = user


class AuditLogMiddleware(MiddlewareMixin):
    """
    Middleware qui stocke l'utilisateur courant dans un thread-local storage.
    Cela permet aux signaux d'audit de savoir quel utilisateur a effectue l'action,
    meme en dehors du contexte de la requete.
    """

    def process_request(self, request):
        """Stocke l'utilisateur de la requete dans le thread-local"""
        if hasattr(request, 'user'):
            set_current_user(request.user)
        else:
            set_current_user(AnonymousUser())

    def process_response(self, request, response):
        """Nettoie le thread-local apres la requete"""
        return response

    def process_exception(self, request, exception):
        """Nettoie le thread-local en cas d'exception"""
        if hasattr(_thread_locals, 'user'):
            delattr(_thread_locals, 'user')
        return None

    def process_template_response(self, request, response):
        """Nettoie le thread-local apres le rendu du template"""
        if hasattr(_thread_locals, 'user'):
            delattr(_thread_locals, 'user')
        return response
