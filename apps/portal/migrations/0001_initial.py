# Generated by Django 5.0.7 on 2024-07-11 10:06

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('course_code', models.CharField(max_length=10, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('unit', models.PositiveIntegerField(default=1)),
                ('course_level', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='courses', to='core.level')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='courses', to='core.department')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='registrations', to='portal.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='registrations', to='core.studentprofile')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('grade', models.CharField(max_length=2)),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=4)),
                ('cgpa', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('registration', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='result', to='portal.courseregistration')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sessions', to='portal.semester')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='courseregistration',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='registrations', to='portal.session'),
        ),
    ]
