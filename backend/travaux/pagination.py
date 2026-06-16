"""
Pagination personnalisee pour retourner tous les resultats
quand aucun parametre de pagination n'est fourni.
Cela permet d'avoir un format cohérent : {"count": N, "results": [...]}
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    """
    Pagination qui retourne toujours un format standard avec count et results.
    Si aucun parametre de page n'est fourni, retourne tous les resultats.
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        """
        Retourne toujours un format standard avec count et results.
        """
        return Response({
            'count': self.page.paginator.count,
            'results': data
        })
