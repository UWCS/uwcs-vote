# Generated by Django 3.1.6 on 2023-02-26 18:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("votes", "0003_election_archived"),
    ]

    operations = [
        migrations.AddField(
            model_name="stvresult",
            name="action_log",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
