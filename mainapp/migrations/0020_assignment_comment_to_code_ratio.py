# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-09 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_auto_20180208_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='comment_to_code_ratio',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
