# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-08 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_auto_20180207_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='function_name',
            field=models.CharField(max_length=128),
        ),
    ]