from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Site",
            fields=[
                ("id_site", models.AutoField(primary_key=True, serialize=False)),
                ("nom_site", models.CharField(max_length=150)),
                ("adresse", models.CharField(max_length=255)),
                ("ville", models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name="Batiment",
            fields=[
                ("id_batiment", models.AutoField(primary_key=True, serialize=False)),
                ("nom_batiment", models.CharField(max_length=150)),
                ("code_patrimoine", models.CharField(max_length=50, unique=True)),
                ("surface_m2", models.DecimalField(decimal_places=2, max_digits=10)),
                ("annee_construction", models.PositiveIntegerField()),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="batiments",
                        to="patrimoine.site",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BatimentCaracteristiquesTech",
            fields=[
                ("type_usage", models.CharField(max_length=120)),
                ("est_classe", models.BooleanField(default=False)),
                ("potentiel_photovoltaique", models.CharField(max_length=120)),
                ("zone_dangereuse", models.CharField(max_length=120)),
                ("reseau_chaleur", models.BooleanField(default=False)),
                ("etiquette_energetique", models.CharField(max_length=1)),
                ("architecte", models.CharField(max_length=120)),
                ("derniere_renovation_date", models.DateField()),
                (
                    "batiment",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="caracteristiques_tech",
                        serialize=False,
                        to="patrimoine.batiment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BatimentService",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("pourcentage_occupation", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "batiment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services_associes",
                        to="patrimoine.batiment",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="batiments_associes",
                        to="users.service",
                    ),
                ),
            ],
            options={"unique_together": {("batiment", "service")}},
        ),
    ]
