# Generated by Django 5.0.7 on 2024-10-06 19:35

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0004_alter_semester_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseGrade",
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
                (
                    "grade",
                    models.CharField(
                        choices=[
                            ("A", "A"),
                            ("B", "B"),
                            ("C", "C"),
                            ("D", "D"),
                            ("E", "E"),
                            ("F", "F"),
                        ],
                        max_length=1,
                    ),
                ),
                ("point", models.PositiveIntegerField()),
            ],
            options={
                "ordering": ("-created",),
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="courseregistration",
            name="course_grade",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="course_registrations",
                to="portal.coursegrade",
            ),
        ),
    ]
