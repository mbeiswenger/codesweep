# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-08 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_auto_20180207_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='outputs',
            field=models.TextField(blank=True),
        ),
    ]
