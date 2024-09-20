# Generated by Django 4.2.16 on 2024-09-20 13:55

from django.db import migrations, models
import woo_publications.metadata.models


class Migration(migrations.Migration):

    dependencies = [
        ("metadata", "0002_alter_informationcategory_identifier"),
    ]

    operations = [
        migrations.CreateModel(
            name="Theme",
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
                ("path", models.CharField(max_length=255, unique=True)),
                ("depth", models.PositiveIntegerField()),
                ("numchild", models.PositiveIntegerField(default=0)),
                (
                    "identifier",
                    models.URLField(
                        default=woo_publications.metadata.models.get_default_theme_identifier,
                        editable=False,
                        help_text="The unique IRI that identifies this theme in the overheid.nl value list. For entries that have been added manually, an identifier is generated.",
                        max_length=255,
                        unique=True,
                        verbose_name="identifier",
                    ),
                ),
                ("naam", models.CharField(max_length=80, verbose_name="name")),
            ],
            options={
                "verbose_name": "theme",
                "verbose_name_plural": "themes",
            },
        ),
        migrations.AlterField(
            model_name="informationcategory",
            name="definitie",
            field=models.TextField(blank=True, verbose_name="definition"),
        ),
        migrations.AlterField(
            model_name="informationcategory",
            name="naam",
            field=models.CharField(max_length=80, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="informationcategory",
            name="naam_meervoud",
            field=models.CharField(
                blank=True, max_length=80, verbose_name="name plural"
            ),
        ),
    ]
