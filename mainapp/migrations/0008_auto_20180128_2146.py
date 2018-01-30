# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-29 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_assignment_instructions_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='inputs',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='instructions_file',
            field=models.FileField(blank=True, null=True, upload_to='instruction_files/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='points',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='time',
            field=models.TimeField(blank=True),
        ),
    ]