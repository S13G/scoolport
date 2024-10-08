# Generated by Django 5.0.7 on 2024-07-15 11:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_studentprofile_department_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentprofile",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
