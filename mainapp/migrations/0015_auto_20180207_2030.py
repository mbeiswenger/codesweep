# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-08 02:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20180207_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]