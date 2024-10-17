# Generated by Django 4.2.16 on 2024-10-09 15:13

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("timeline_logger", "0006_auto_20220413_0749"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimelineLogProxy",
            fields=[],
            options={
                "verbose_name": "(audit) log entry",
                "verbose_name_plural": "(audit) log entries",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("timeline_logger.timelinelog",),
        ),
    ]