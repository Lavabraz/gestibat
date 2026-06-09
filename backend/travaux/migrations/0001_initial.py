from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("patrimoine", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Investissement",
            fields=[
                ("id_investissement", models.AutoField(primary_key=True, serialize=False)),
                ("titre_projet", models.CharField(max_length=200)),
                ("type_investissement", models.CharField(max_length=120)),
                ("annee_programmation", models.PositiveIntegerField()),
                ("budget_estime", models.DecimalField(decimal_places=2, max_digits=12)),
                ("cout_reel", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("Proposition", "Proposition"),
                            ("Validé", "Validé"),
                            ("Engagé", "Engagé"),
                            ("Terminé", "Terminé"),
                        ],
                        max_length=20,
                    ),
                ),
                ("priorite_strategique", models.CharField(max_length=120)),
                (
                    "batiment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="investissements",
                        to="patrimoine.batiment",
                    ),
                ),
                (
                    "service_pilote",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="investissements_pilotes",
                        to="users.service",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Travaux",
            fields=[
                ("id_travaux", models.AutoField(primary_key=True, serialize=False)),
                (
                    "domaine_metier",
                    models.CharField(
                        choices=[
                            ("Bâtiment", "Bâtiment"),
                            ("Espaces Verts", "Espaces Verts"),
                            ("Voirie", "Voirie"),
                            ("DSI", "DSI"),
                        ],
                        max_length=20,
                    ),
                ),
                ("titre_travaux", models.CharField(max_length=200)),
                (
                    "type_travaux",
                    models.CharField(
                        choices=[
                            ("Entretien", "Entretien"),
                            ("Amélioration", "Amélioration"),
                            ("Urgence", "Urgence"),
                        ],
                        max_length=20,
                    ),
                ),
                ("priorite", models.CharField(max_length=50)),
                ("date_demande", models.DateField()),
                ("date_fin_previsionnelle", models.DateField(blank=True, null=True)),
                ("date_fin_reelle", models.DateField(blank=True, null=True)),
                ("intervenant_externe", models.CharField(blank=True, max_length=120, null=True)),
                ("statut", models.CharField(max_length=50)),
                (
                    "batiment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="travaux",
                        to="patrimoine.batiment",
                    ),
                ),
                (
                    "investissement",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="travaux_associes",
                        to="travaux.investissement",
                    ),
                ),
                (
                    "responsable_interne",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="travaux_responsables",
                        to="users.agent",
                    ),
                ),
                (
                    "service_demandeur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="travaux_demandes",
                        to="users.service",
                    ),
                ),
            ],
        ),
    ]
