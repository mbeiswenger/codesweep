# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-20 04:02
from __future__ import unicode_literals

from django.db import migrations, models
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0025_auto_20180219_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='inputs',
            field=models.FileField(upload_to="inputs"),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='outputs',
            field=models.FileField(upload_to='expectedoutputs'),
        ),
    ]