# Generated by Django 5.0.7 on 2024-10-06 19:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0005_coursegrade_courseregistration_course_grade"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="coursegrade",
            options={"ordering": ("created",)},
        ),
        migrations.AddField(
            model_name="courseregistration",
            name="exam_score",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="courseregistration",
            name="course_grade",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="course_registrations",
                to="portal.coursegrade",
            ),
        ),
    ]
