# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-05 12:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.IntegerField(null=True)),
                ('tabu_length', models.IntegerField(null=True)),
                ('iterations_without_improvement', models.IntegerField(null=True)),
                ('iterations', models.IntegerField(null=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('score', models.IntegerField(null=True)),
                ('File', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.File')),
                ('Student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.Student')),
            ],
        ),
    ]
