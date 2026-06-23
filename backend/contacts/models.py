from django.db import models
from django.core.validators import EmailValidator, RegexValidator

class Contact(models.Model):
    CONTACT_TYPES = [
        ('entreprise', 'Entreprise'),
        ('artisan', 'Artisan'),
        ('fournisseur', 'Fournisseur'),
        ('autre', 'Autre'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Prenom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(
        max_length=255,
        verbose_name="Email",
        validators=[EmailValidator(message="Adresse email invalide")]
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Telephone",
        validators=[
            RegexValidator(
                regex='^[+]?[(]?[0-9]{3}[)]?[-s.]?[0-9]{3}[-s.]?[0-9]{4,6}$',
                message="Numero de telephone invalide"
            )
        ]
    )
    role = models.CharField(max_length=100, verbose_name="Role")
    company = models.CharField(max_length=255, verbose_name="Entreprise", blank=True, null=True)
    address = models.TextField(verbose_name="Adresse", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Ville", blank=True, null=True)
    postal_code = models.CharField(max_length=20, verbose_name="Code postal", blank=True, null=True)
    contact_type = models.CharField(
        max_length=20,
        choices=CONTACT_TYPES,
        default='autre',
        verbose_name="Type de contact"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise a jour")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.company or 'N/A'})"
