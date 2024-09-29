# Generated by Django 5.0.7 on 2024-07-11 10:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FAQ",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                ("question", models.CharField(max_length=255, unique=True)),
                ("answer", models.TextField()),
            ],
            options={
                "ordering": ("-created",),
                "abstract": False,
            },
        ),
    ]
