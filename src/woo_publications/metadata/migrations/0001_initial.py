# Generated by Django 4.2.16 on 2024-09-18 11:36

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
                        help_text="The unique IRI that identifies this category in the overheid.nl value list. For entries that have been added manually, an identifier is generated.",
                        max_length=255,
                        unique=True,
                        verbose_name="identifier",
                    ),
                ),
                (
                    "naam",
                    models.CharField(
                        help_text="The name of the category.",
                        max_length=80,
                        verbose_name="name",
                    ),
                ),
                (
                    "naam_meervoud",
                    models.CharField(
                        blank=True,
                        help_text="The plural name of the category.",
                        max_length=80,
                        verbose_name="name plural",
                    ),
                ),
                (
                    "definitie",
                    models.TextField(
                        blank=True,
                        help_text="The description of the category.",
                        verbose_name="definition",
                    ),
                ),
                (
                    "oorsprong",
                    models.CharField(
                        choices=[
                            ("waardelijst", "Value list"),
                            ("zelf_toegevoegd", "Custom entry"),
                        ],
                        default="zelf_toegevoegd",
                        help_text="Determines where the category is defined and sourced from, and how the identifier should be interpreted. If the value list is the origin, the category can not be modified or deleted.",
                        max_length=15,
                        verbose_name="origin",
                    ),
                ),
            ],
            options={
                "verbose_name": "information category",
                "verbose_name_plural": "information categories",
                "ordering": ("order",),
                "abstract": False,
            },
        ),
    ]