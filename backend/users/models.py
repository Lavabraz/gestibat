from django.contrib.auth.models import AbstractUser
from django.db import models


class Pole(models.Model):
    id_pole = models.AutoField(primary_key=True)
    code_pole = models.CharField(max_length=20, unique=True)
    nom_pole = models.CharField(max_length=120)
    responsable_pole = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"{self.code_pole} - {self.nom_pole}"


class Service(models.Model):
    id_service = models.AutoField(primary_key=True) 
    pole = models.ForeignKey(Pole, on_delete=models.PROTECT, related_name="services")
    nom_service = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.nom_service


class Agent(models.Model):
    class Statut(models.TextChoices):
        TITULAIRE = "Titulaire", "Titulaire"
        REMPLACANT = "Remplaçant", "Remplaçant"
        VACATAIRE = "Vacataire", "Vacataire"

    id_agent = models.AutoField(primary_key=True)
    nom_complet = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    statut = models.CharField(max_length=20, choices=Statut.choices)

    def __str__(self) -> str:
        return self.nom_complet


class AgentService(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="agent_services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_agents")
    role_dans_service = models.CharField(max_length=120)

    class Meta:
        unique_together = ("agent", "service")

    def __str__(self) -> str:
        return f"{self.agent} - {self.service} ({self.role_dans_service})"


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "super_admin"
        ADMIN = "admin", "admin"
        EDITEUR = "editeur", "editeur"
        LECTEUR = "lecteur", "lecteur"

    agent = models.OneToOneField(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.LECTEUR)

    def __str__(self) -> str:
        return self.username


class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "CREATE", "Création"
        UPDATE = "UPDATE", "Modification"
        DELETE = "DELETE", "Suppression"
        READ = "READ", "Lecture"
        LOGIN = "LOGIN", "Connexion"

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action = models.CharField(max_length=10, choices=Action.choices)
    model_name = models.CharField(max_length=100)  # ex: "Batiment", "Travaux"
    object_id = models.CharField(max_length=100)
    object_display = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "-timestamp"]),
            models.Index(fields=["model_name", "-timestamp"]),
            models.Index(fields=["-timestamp"]),
        ]

    def __str__(self) -> str:
        return f"{self.action} {self.model_name} ({self.object_id}) by {self.user} at {self.timestamp}"
