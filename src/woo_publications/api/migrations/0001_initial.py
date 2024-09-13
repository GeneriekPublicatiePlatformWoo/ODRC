# Generated by Django 4.2.16 on 2024-09-17 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="InformatieCategorie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                (
                    "identifier",
                    models.URLField(
                        max_length=255, unique=True, verbose_name="Identifier"
                    ),
                ),
                ("name", models.CharField(max_length=80, verbose_name="Name")),
                (
                    "name_plural",
                    models.CharField(max_length=80, verbose_name="Name plural"),
                ),
                ("definition", models.TextField(blank=True, verbose_name="Definition")),
                (
                    "origin",
                    models.CharField(
                        choices=[
                            ("waardelijst", "Waardelijst"),
                            ("zelf_toegevoegd", "Zelf toegevoegd"),
                        ],
                        max_length=15,
                        verbose_name="Origin",
                    ),
                ),
            ],
            options={
                "verbose_name": "informatie categorie",
                "verbose_name_plural": "informatie categorieën",
                "ordering": ("order",),
            },
        ),
    ]