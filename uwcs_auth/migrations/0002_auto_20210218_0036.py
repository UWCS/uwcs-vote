# Generated by Django 3.1.6 on 2021-02-18 00:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("uwcs_auth", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="warwickvoteuser",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="member",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
