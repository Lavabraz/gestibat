from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("patrimoine", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Compteur",
            fields=[
                ("id_compteur", models.AutoField(primary_key=True, serialize=False)),
                ("reference_fournisseur", models.CharField(max_length=120)),
                (
                    "type_fluide",
                    models.CharField(
                        choices=[
                            ("Électricité", "Électricité"),
                            ("Gaz", "Gaz"),
                            ("Eau", "Eau"),
                            ("Réseau de chaleur", "Réseau de chaleur"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "batiment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="compteurs",
                        to="patrimoine.batiment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ConsommationFluide",
            fields=[
                ("id_conso", models.AutoField(primary_key=True, serialize=False)),
                ("periode_mensuelle", models.DateField()),
                ("valeur_index", models.DecimalField(decimal_places=2, max_digits=12)),
                ("montant_ttc_facture", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                (
                    "compteur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="consommations",
                        to="energie.compteur",
                    ),
                ),
            ],
        ),
    ]
