# Generated by Django 4.2.16 on 2024-11-06 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("metadata", "0007_alter_organisation_is_actief"),
        ("publications", "0006_merge_20241101_1532"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="opsteller",
            field=models.ForeignKey(
                blank=True,
                help_text="The organisation which drafted the publication and it's content.",
                limit_choices_to={"is_actief": True},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="publication_drafters",
                to="metadata.organisation",
                verbose_name="drafter",
            ),
        ),
        migrations.AddField(
            model_name="publication",
            name="publisher",
            field=models.ForeignKey(
                default="",
                help_text="The organisation which publishes the publication.",
                limit_choices_to={"is_actief": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="publication_publishers",
                to="metadata.organisation",
                verbose_name="publisher",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="publication",
            name="verantwoordelijke",
            field=models.ForeignKey(
                blank=True,
                help_text="The organisation which is liable for the publication and it's contents.",
                limit_choices_to={"is_actief": True},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="publication_liable_organisations",
                to="metadata.organisation",
                verbose_name="liable organisation",
            ),
        ),
    ]