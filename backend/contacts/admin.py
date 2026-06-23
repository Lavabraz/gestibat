from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone', 'company', 'contact_type', 'is_active')
    list_filter = ('contact_type', 'is_active', 'city')
    search_fields = ('last_name', 'first_name', 'email', 'company', 'phone')
    list_editable = ('is_active',)
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Informations professionnelles', {
            'fields': ('role', 'company', 'address', 'city', 'postal_code', 'contact_type')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
