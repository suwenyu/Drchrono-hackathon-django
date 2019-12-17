# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-16 19:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('scheduled_time', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('exam_room', models.IntegerField()),
                ('scheduled_end_time', models.DateTimeField(null=True)),
                ('checkin_time', models.DateTimeField(null=True)),
                ('waiting_time', models.IntegerField(null=True)),
                ('start_appointment_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('social_security_number', models.CharField(max_length=20, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drchrono.Doctor')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drchrono.Doctor'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drchrono.Patient'),
        ),
    ]
