# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-11 19:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_auto_20180211_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='instruction_file',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='mainapp.InstructionFile'),
            preserve_default=False,
        ),
    ]
