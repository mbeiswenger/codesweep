# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-21 02:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0028_auto_20180220_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
