# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-11 17:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='iterations',
            new_name='iterations_of_tabu',
        ),
    ]
