from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import Contact
from .serializers import ContactSerializer

class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.filter(is_active=True)
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by type if provided
        contact_type = self.request.query_params.get('type', None)
        if contact_type:
            queryset = queryset.filter(contact_type=contact_type)
        
        # Filter by search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(company__icontains=search) |
                Q(role__icontains=search)
            )
        
        return queryset.order_by('last_name', 'first_name')

    def perform_create(self, serializer):
        serializer.save()


class ContactRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
